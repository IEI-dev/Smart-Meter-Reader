sudo apt install p7zip-full

cd ./meter/model/det/yolox
7z x ./model.zip
cd ../../../

cd ./meter
7z x ./image.zip
cd ../


cd ./server/docker/src/openvino/model/det/yolox
7z x ./model.zip
cd ../../../../../../../

cd ./server/docker/src/openvino
7z x ./image.zip
cd ../../../../

sudo chmod 777 . -R

echo "done!"
