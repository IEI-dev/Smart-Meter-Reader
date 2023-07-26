
import paho.mqtt.client as mqtt
client = mqtt.Client()
client.connect("localhost", 1883)
client.publish("hello/world", "test message")


import os
import psutil
 



#save json content, replace client timestamp(app) name to index
import subprocess
import sys
import json

command = ["sudo", "intel_gpu_top","-J"]


def parsejson(jsonstr):
    data = json.loads(jsonstr)

    ary = []
    for client in data["clients"]:
        ary.append(client)

    for i in range(0,len(data["clients"])):
        data["clients"][str(i)] = data["clients"][ary[i]]
        del data["clients"][ary[i]]
    
    return data
        
    

def cmd(command):




    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    jsonstr = ""
    for line in process.stdout:






        line_decode = line.decode(sys.stdout.encoding)


        if line_decode == "{\n":
            jsonstr = line_decode



        elif line_decode == "},\n":
            jsonstr = jsonstr + "}\n"

 

            try:
                data = parsejson(jsonstr)
                #print(data["clients"]["0"])
                #print(data["clients"]["0"]["name"])
                #print(data["clients"]["0"]["pid"])
                #print(data["clients"]["0"]["engine-classes"]["Render/3D"]["busy"])
                #print(data["clients"]["0"]["engine-classes"]["Blitter"]["busy"])
                #print(data["clients"]["0"]["engine-classes"]["Video"]["busy"])
                #print(data["clients"]["0"]["engine-classes"]["VideoEnhance"]["busy"])
                #print(data["clients"]["0"]["engine-classes"]["[unknown]"]["busy"])

                client.publish("meter/system/info/intel_gpu_top/clients/0/name", data["clients"]["0"]["name"])
                client.publish("meter/system/info/intel_gpu_top/clients/0/pid", data["clients"]["0"]["pid"])
                client.publish("meter/system/info/intel_gpu_top/clients/0/engine-classes/Render", data["clients"]["0"]["engine-classes"]["Render/3D"]["busy"])
                client.publish("meter/system/info/intel_gpu_top/clients/0/engine-classes/Blitter", data["clients"]["0"]["engine-classes"]["Blitter"]["busy"])
                client.publish("meter/system/info/intel_gpu_top/clients/0/engine-classes/Video", data["clients"]["0"]["engine-classes"]["Video"]["busy"])
                client.publish("meter/system/info/intel_gpu_top/clients/0/engine-classes/VideoEnhance", data["clients"]["0"]["engine-classes"]["VideoEnhance"]["busy"])
                client.publish("meter/system/info/intel_gpu_top/clients/0/engine-classes/Compute", data["clients"]["0"]["engine-classes"]["[unknown]"]["busy"])

                client.publish("meter/system/info/intel_gpu_top/clients/1/name", data["clients"]["1"]["name"])
                client.publish("meter/system/info/intel_gpu_top/clients/1/pid", data["clients"]["1"]["pid"])
                client.publish("meter/system/info/intel_gpu_top/clients/1/engine-classes/Render", data["clients"]["1"]["engine-classes"]["Render/3D"]["busy"])
                client.publish("meter/system/info/intel_gpu_top/clients/1/engine-classes/Blitter", data["clients"]["1"]["engine-classes"]["Blitter"]["busy"])
                client.publish("meter/system/info/intel_gpu_top/clients/1/engine-classes/Video", data["clients"]["1"]["engine-classes"]["Video"]["busy"])
                client.publish("meter/system/info/intel_gpu_top/clients/1/engine-classes/VideoEnhance", data["clients"]["1"]["engine-classes"]["VideoEnhance"]["busy"])
                client.publish("meter/system/info/intel_gpu_top/clients/1/engine-classes/Compute", data["clients"]["1"]["engine-classes"]["[unknown]"]["busy"])

                client.publish("meter/system/info/intel_gpu_top/clients/2/name", data["clients"]["2"]["name"])
                client.publish("meter/system/info/intel_gpu_top/clients/2/pid", data["clients"]["2"]["pid"])
                client.publish("meter/system/info/intel_gpu_top/clients/2/engine-classes/Render", data["clients"]["2"]["engine-classes"]["Render/3D"]["busy"])
                client.publish("meter/system/info/intel_gpu_top/clients/2/engine-classes/Blitter", data["clients"]["2"]["engine-classes"]["Blitter"]["busy"])
                client.publish("meter/system/info/intel_gpu_top/clients/2/engine-classes/Video", data["clients"]["2"]["engine-classes"]["Video"]["busy"])
                client.publish("meter/system/info/intel_gpu_top/clients/2/engine-classes/VideoEnhance", data["clients"]["2"]["engine-classes"]["VideoEnhance"]["busy"])
                client.publish("meter/system/info/intel_gpu_top/clients/2/engine-classes/Compute", data["clients"]["2"]["engine-classes"]["[unknown]"]["busy"])

                client.publish("meter/system/info/intel_gpu_top/clients/3/name", data["clients"]["3"]["name"])
                client.publish("meter/system/info/intel_gpu_top/clients/3/pid", data["clients"]["3"]["pid"])
                client.publish("meter/system/info/intel_gpu_top/clients/3/engine-classes/Render", data["clients"]["3"]["engine-classes"]["Render/3D"]["busy"])
                client.publish("meter/system/info/intel_gpu_top/clients/3/engine-classes/Blitter", data["clients"]["3"]["engine-classes"]["Blitter"]["busy"])
                client.publish("meter/system/info/intel_gpu_top/clients/3/engine-classes/Video", data["clients"]["3"]["engine-classes"]["Video"]["busy"])
                client.publish("meter/system/info/intel_gpu_top/clients/3/engine-classes/VideoEnhance", data["clients"]["3"]["engine-classes"]["VideoEnhance"]["busy"])
                client.publish("meter/system/info/intel_gpu_top/clients/3/engine-classes/Compute", data["clients"]["3"]["engine-classes"]["[unknown]"]["busy"])

                client.publish("meter/system/info/intel_gpu_top/clients/4/name", data["clients"]["4"]["name"])
                client.publish("meter/system/info/intel_gpu_top/clients/4/pid", data["clients"]["4"]["pid"])
                client.publish("meter/system/info/intel_gpu_top/clients/4/engine-classes/Render", data["clients"]["4"]["engine-classes"]["Render/3D"]["busy"])
                client.publish("meter/system/info/intel_gpu_top/clients/4/engine-classes/Blitter", data["clients"]["4"]["engine-classes"]["Blitter"]["busy"])
                client.publish("meter/system/info/intel_gpu_top/clients/4/engine-classes/Video", data["clients"]["4"]["engine-classes"]["Video"]["busy"])
                client.publish("meter/system/info/intel_gpu_top/clients/4/engine-classes/VideoEnhance", data["clients"]["4"]["engine-classes"]["VideoEnhance"]["busy"])
                client.publish("meter/system/info/intel_gpu_top/clients/4/engine-classes/Compute", data["clients"]["4"]["engine-classes"]["[unknown]"]["busy"])



                load1, load5, load15 = psutil.getloadavg()
                cpu_usage = (load1/os.cpu_count()) * 100
                #print("The CPU usage is : ", cpu_usage)
                client.publish("meter/system/info/cpu", cpu_usage)
                #print('RAM memory % used:', psutil.virtual_memory()[2])
                client.publish("meter/system/info/mem", psutil.virtual_memory()[2])








                #print(data["engines"]["Video/0"]["busy"])
                #print(data["engines"]["Render/3D/0"]["busy"])
                #print(data["engines"])
            except:
                pass





        else:
            jsonstr = jsonstr + line_decode






cmd(command)


