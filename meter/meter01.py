#from DetectSegScale-video04 for special demo case
#add combine 6-images, base64 to mqtt

import cv2
import numpy as np
from openvino.runtime import Core
import os
import base64
import paho.mqtt.client as mqtt
import time

client = mqtt.Client()
client.connect("localhost", 1883)


ie = Core()
model_xml_path = "./model/det/yolox/model.xml"
model = ie.read_model(model=model_xml_path)
compiled_model = ie.compile_model(model=model, device_name="CPU")
input_layer_ir = compiled_model.input(0)
N, C, H, W = input_layer_ir.shape

def convert_result_to_image(bgr_image, resized_image, boxes,confidence):
    colors = {"red": (255, 0, 0), "green": (0, 255, 0)}

    (real_y, real_x), (resized_y, resized_x) = bgr_image.shape[:2], resized_image.shape[:2]
    ratio_x, ratio_y = real_x / resized_x, real_y / resized_y
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

    filterlist=[]
    for i,box in enumerate(boxes):
        conf = box[-1]
        if conf > confidence:
            (x_min, y_min, x_max, y_max) = [
                int(max(corner_position * ratio_y, 10)) if idx % 2 
                else int(corner_position * ratio_x)
                for idx, corner_position in enumerate(box[:-1])
            ]
            rgb_image = cv2.rectangle(rgb_image, (x_min, y_min), (x_max, y_max), colors["green"], 3)


            #------  customize for get inference detail ------
            index = i
            label = name[labels[i]]
            conf=conf
            xy=[x_min,y_min,x_max,y_max]
            xysize = (x_max-x_min)*(y_max-y_min)
            filter = [index,label,conf,xy,xysize]
            filterlist.append(filter)

    return rgb_image,filterlist

def point_next(origin,arrays):
    import math
    min = 10000
    pointnext=[]
    for array in arrays:
        xmin,ymin,xmax,ymax = array[3]
        p1 = [origin[0], origin[1]]
        p2 = [xmin, ymin]
        distance = math.dist([p1[0], p1[1]], [p2[0], p2[1]])

        if distance < min:
            min = distance
            pointnext=array

    #pop select point
    for i,array in enumerate(arrays):
        if array[0] ==pointnext[0]:
            arrays.pop(i)



    return pointnext,arrays

def draw_scalebox_repleat(origin_temp,text,image):

    yellow_color = (0, 255, 0) # BGR
    xmin,ymin,xmax,ymax = origin_temp[3]
    #print(origin_temp[3])
    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), yellow_color, 3, cv2.LINE_AA)
    cv2.putText(image, text, (xmax+5, ymax), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1, cv2.LINE_AA)

    return image

def image2base64(topic,image):
    retval, buffer = cv2.imencode('.jpg', image)
    b64_str = base64.b64encode(buffer)
    b64_str= str(b64_str).replace("b'","").replace("'","")
    client.publish(topic, b64_str)


while True:
    f = open("log","w")
    dir_path = "./image/2segment"
    dirs = os.listdir(dir_path)
    dirs.sort()
    for framename in dirs:
        client.publish("meter/service", "on")
        client.publish("meter/image/input/name", framename)
        #detection scale
        frame_path = os.path.join(dir_path, framename)
        image = cv2.imread(frame_path)
        print(frame_path)
        f.writelines("\n"+frame_path+"\n")    

        resized_image = cv2.resize(image, (W, H))
        input_image = np.expand_dims(resized_image.transpose(2, 0, 1), 0)

        result = compiled_model([input_image])

        boxes = result["boxes"]
        name = ["scale","pointer"]
        labels = result["labels"]

        image_detection,filterlist = convert_result_to_image(image, resized_image, boxes,0.67)


        pointer = sorted(filterlist, key=lambda s: s[4])
        pointer = pointer[len(pointer)-1]

        scales=sorted(filterlist, key=lambda ary: ary[4])
        scales=scales[:-1]


        #calculate scale
        scales_temp = list(scales)
        origin = [0,512]
        origin_temp,scales_temp = point_next(origin,scales_temp)

        scales_value = []
        origin_temp = list(origin_temp)
        origin_temp.append(0)
        scales_value.append(origin_temp)


        image = cv2.imread(frame_path)
        image = draw_scalebox_repleat(origin_temp,"0",image)
        value = 0.5
        for i, scale in enumerate(scales_temp):
            scales_temp = list(scales_temp)
            origin_temp = origin_temp[3]
            origin_temp,scales_temp = point_next(origin_temp,scales_temp)
            image = draw_scalebox_repleat(origin_temp,str((i+1)*value),image)

            origin_temp = list(origin_temp)
            origin_temp.append((i+1)*value)
            scales_value.append(origin_temp)

        image_value = image
        


        xmin,ymin,xmax,ymax  = pointer[3]
        point_pointer = [ int((xmin+xmax)/2) , int((ymin+ymax)/2)  ]
        #image_result_seg = cv2.imread(frame_path) #remove all scale, new frame, only keep pointer
        #image_result_seg = image_value #not real copy, will continue work on pre-step
        image_result_seg = image_value.copy()
        image_result_seg = cv2.circle(image_result_seg,point_pointer, 10, (255, 0, 0), 3)


        scales_temp = list(scales_value)
        origin = point_pointer
        origin_temp,scales_temp = point_next(origin,scales_temp)
        print("scale value: ",origin_temp[5])
        f.writelines("scale value: "+str(origin_temp[5])+"\n")

        value = origin_temp[5]
        xmin,ymin,xmax,ymax  = origin_temp[3]

        image_result_seg = cv2.rectangle(image_result_seg, (xmin, ymin), (xmax, ymax), (255, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(image_result_seg, str(value), (xmax+5, ymax), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1, cv2.LINE_AA)

        frame_path_ini = frame_path.replace("2segment","1frame").replace("segment","frame")
        image_result = cv2.imread(frame_path_ini)
        image_result = cv2.rectangle(image_result, (xmin, ymin), (xmax, ymax), (0, 255, 0), 3, cv2.LINE_AA)
        cv2.putText(image_result, str(value), (xmax+5, ymax), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1, cv2.LINE_AA)


        f.writelines("pointer:"+str(pointer)+"\n")
        f.writelines("scale:"+str(scales)+"\n")
        if len(scales) != 21:
            print("error:scale")
            f.writelines("error:len(scale):"+str(len(scales))+"\n")
        else:
            folder = "./image/"

            image_frm = cv2.imread(frame_path.replace("2segment","1frame").replace("segment","frame"))
            #cv2.imwrite(folder+"/1frame/"+framename.replace("segment","frame"),image_frm)

            image_seg = cv2.imread(frame_path)
            #cv2.imwrite(folder+"/2segment/"+framename,image_seg)

            image_det = image_detection
            cv2.imwrite(folder+"/3detection/"+framename.replace("segment","detection"),image_det)

            image_val = image_value
            cv2.imwrite(folder+"/4value/"+framename.replace("segment","value"),image_val)

            image_relseg = image_result_seg
            cv2.imwrite(folder+"/5resultseg/"+framename.replace("segment","resultseg"),image_relseg)

            image_rel = image_result
            cv2.imwrite(folder+"/6result/"+framename.replace("segment","result"),image_rel)

            h1_img = cv2.hconcat([image_frm, image_seg, image_det])
            h2_img = cv2.hconcat([image_val, image_relseg, image_rel])
            v_img = cv2.vconcat([h1_img, h2_img])
            image_cmb = v_img
            cv2.imwrite(folder+"/7combine/"+framename.replace("segment","combine"),image_cmb)



            client.publish("meter/result/value", value)
            image2base64("meter/image/base64/frame",image_frm)
            image2base64("meter/image/base64/segment",image_seg)
            image2base64("meter/image/base64/detection",image_det)
            image2base64("meter/image/base64/value",image_val)
            image2base64("meter/image/base64/result_seg",image_relseg)
            image2base64("meter/image/base64/result",image_rel)
            image2base64("meter/image/base64/combine",image_cmb)



            #cv2.imshow('Result', image_rel)
            if cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
                break



            time.sleep(5)
            pass

    f.close()



    cv2.destroyAllWindows()






