import cv2
vidcap = cv2.VideoCapture('./meter_crop2.mp4')
success,image = vidcap.read()
count = 100
while success:
  image = cv2.resize(image, (512, 512), interpolation=cv2.INTER_AREA)
  cv2.imwrite("./1frame/frame%d.jpg" % count, image)     # save frame as JPEG file      
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1