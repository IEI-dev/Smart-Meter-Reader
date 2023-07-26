# Smart-Meter-Reader

install guide include below session  
you can prepare couple machines or install server and edge in a machine
- Server   
1. node-red  
2. influxdb  
3. grafana  
- Edge   
4. openvino (example: smart meter reader)   

    
## Server Installation(Host)
- pre-requirement  
nodejs   
link: https://tecadmin.net/install-latest-nodejs-npm-on-ubuntu/
   
```shell
sudo apt install -y curl 
curl -sL https://deb.nodesource.com/setup_18.x | sudo -E bash - 
sudo apt install -y nodejs 
```  
![image](./screenshot/1.png)
![image](/uploads/13c16209267fe8e32a239d57d6ef1c0b/image.png)
![image](/uploads/85ab2ed39c0b35c3fd9162a4eb904287/image.png)   
   

validate install  
```shell
node -v
#v18.16.1

npm -v 
#9.5.1
```   
![image](/uploads/6f2ff707f667fbaa77c1162ee10999ea/image.png)   
   
- node-red installation  
link: https://nodered.org/docs/getting-started/local
   
move to the node-red folder   
```shell
cd dev/meter-reader/server/nodered/
sudo npm install -g --unsafe-perm node-red
node-red
```
![image](/uploads/b9fe1ff165a73e23abecde646e53039c/image.png)
![image](/uploads/07b66955201322aecab9a13eaa139163/image.png)
   
You can then access the Node-RED editor by pointing your browser at http://localhost:1880.    
*we need to install some node in next config session.       
![image](/uploads/7da9113d50efaed5e709a9a83faa2507/image.png)
    
- influxdb installation   
link: https://linux.how2shout.com/how-to-install-influxdb-on-ubuntu-22-04-to-create-database/   
   
```shell
cd dev/meter-reader/server/influxdb
sudo apt update
wget -q https://repos.influxdata.com/influxdata-archive_compat.key
echo '393e8779c89ac8d958f81f942f9ad7fb82a25e133faddaf92e15b16e6ac9ce4c influxdata-archive_compat.key' | sha256sum -c && cat influxdata-archive_compat.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg > /dev/null
echo 'deb [signed-by=/etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg] https://repos.influxdata.com/debian stable main' | sudo tee /etc/apt/sources.list.d/influxdata.list
sudo apt update
sudo apt install influxdb2
sudo systemctl start influxdb
sudo systemctl enable influxdb
sudo systemctl status influxdb
```
![image](/uploads/3219c93320e4b591c24a547846025356/image.png)
![image](/uploads/3e4e0fc4d0dbdcce6a7ad3035eb7074c/image.png)
![image](/uploads/7f212b2c06fe3c223eedc51ae7c99ecb/image.png)
![image](/uploads/fafb4079592a244bdb594400ee9b0a74/image.png)
   
Open the browser and type: http://localhost:8086
![image](/uploads/1e39f75a3b8778c64b2331060a8c3771/image.png)
   
- grafana installation   
link: https://grafana.com/docs/grafana/latest/setup-grafana/installation/   
link: https://grafana.com/docs/grafana/latest/setup-grafana/start-restart-grafana/   
   
```shell
cd dev/meter-reader/server/grafana
sudo apt-get install -y apt-transport-https
sudo apt-get install -y software-properties-common wget
sudo wget -q -O /usr/share/keyrings/grafana.key https://apt.grafana.com/gpg.key
echo "deb [signed-by=/usr/share/keyrings/grafana.key] https://apt.grafana.com stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
echo "deb [signed-by=/usr/share/keyrings/grafana.key] https://apt.grafana.com beta main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
sudo apt-get update
# Installs the latest OSS release:
sudo apt-get install grafana

```   
![image](/uploads/fad1ffc11c33ece9496b3c66d7dc9b96/image.png)
![image](/uploads/fba58f45abca6c1d7300378a7e3d63dd/image.png)
![image](/uploads/987e6d1a635778b3c0bfa0c9753c3f2e/image.png)
![image](/uploads/478b95e9b48becb5bb40730c0fc5f207/image.png)
   
Open your web browser and go to http://localhost:3000/
![image](/uploads/f9aa2541ab30d9d9f4f69268a32112cc/image.png)
    

## Server Installation(Docker)   
- pre-requirement   
install docker and docker-compose  
you should be auto install it in EIV step  
if not, you can flow below link to install it.   
link: https://docs.docker.com/engine/install/ubuntu/ 
    
- docker build   
go to meter/server/docker folder, and run below command   
```shell
docker compose up -d
```
![image](/uploads/a4808b549f587ed944879ca08159b687/image.png)
   
- openvino(edge)      
edge meter sample files in ***/data***     
connect container   
```shell
docker exec -it iEi.openvino /bin/bash
cd /data
```
![image](/uploads/aa0c828e0993318957ee330c8571857f/image.png)
![image](/uploads/639e1f5bfe79a7f24f78eac2751b567a/image.png)
   
- config same as next session, only need to change below network setting(localhost->docker-ip)    
host: 10.0.10.1  
iEi.influxdb: 10.0.10.2  
iEi.grafana: 10.0.10.3   
iEi.nodered: 10.0.10.4  
iEi.openvino: 10.0.10.5      



# Server Config   
- influxdb:   
   
Let's setup influxdb first. because influxdb token is require in other setup.  
    
setup account/password.   
![image](/uploads/e69017732fe960f788fb78093e64e198/image.png)
![image](/uploads/1b144ed7989e2466af370aa521f56e9c/image.png)
   
copy and save this token. we will use it in other step   
![image](/uploads/51ff1e62937804fa8bb30869dffe0354/image.png)
![image](/uploads/e61da6fb757db06a3e53e97fee20d5b4/image.png)   
   
choose get started and then choose buckets   
![image](/uploads/1351f5ccf74ea6ecca59f797bd61bc54/image.png)
![image](/uploads/d49963d80663bd99c46eefb14027c3c2/image.png)
   
create buckets and name "**meter**"  
![image](/uploads/6eddc5c08b0e73b84dc7389deb9ee8fb/image.png)   
![image](/uploads/c2b98120c2d0caf2202ca141887d277d/image.png)
   
- node-red(pre-load flows.json)  
if you install and start host version in meter-reader/server/nodered ,it was pre-load flows.json   
we don't need to import flows.json again     
![image](/uploads/ff076b416f71637fa195fb9fcf0d60a6/image.png)
   
base on warning message, we need to install missing node.   
![image](/uploads/a71c878d32e7db8eb6bb1259d695ac38/image.png)
   
menu -> manage palette   
![image](/uploads/efc63903e4e8b1b65ba054144560579e/image.png)
   
search missing node and install it   
![image](/uploads/2b29efc4d179f8b8eb17ed56f73acdb4/image.png)
![image](/uploads/318058ee09e995d33894a82b00c45d07/image.png)
![image](/uploads/b831ca67244e5e8e321b9c7808c03881/image.png)
![image](/uploads/88b1a05ca6fa86a4067847884b3a89f5/image.png)
   
missing node full name   
![image](/uploads/442c1664898461458891a06cde76ba3d/image.png)
    
next step we will setup node-red influxdb node  
please double click one of influxdb node  
![image](/uploads/063b92c71472ac98acaaa1332ad44c87/image.png) 
   
edit server   
![image](/uploads/6a9254d236a2bc672ba0a82a17566d29/image.png)
   
copy and paste token, and update it, and done.   
![image](/uploads/967665e2a92bf09f9ecbd1d2457aa286/image.png)
![image](/uploads/7b7db47dc67adc54593bf97db6d1449d/image.png)
   
Deploy    
![image](/uploads/af8d06c9d0a9afa12dae9b52b98c9e31/image.png)
![image](/uploads/250e6cfe3d83064782b4c59f8fdef8c9/image.png)
    
- grafana   

setup username and password   
![image](/uploads/c055ca457c6d6e289555c1d45a2bad6e/image.png)
![image](/uploads/832d05f0ea92ba0f31011a793f3f4bf3/image.png)
    
setup data source   
![image](/uploads/2011b198924d5a869acd1c389bb3827c/image.png)
   
choose influxdb
![image](/uploads/2c446e8f7e9c546e8a76cbb8abb47d03/image.png)
   
quenry language choose Flux(1.8+)   
![image](/uploads/18239562980443ccb6fd8afb5c258c57/image.png)
![image](/uploads/4f6fb1375f34f0158c59526c45f9e01e/image.png)

type influxdb information as pre-step    
*HTTP(URL), Auth(Basic auth), Basic Auth Details(User/Password), InfluxDB Details(Organization/Token)   
![image](/uploads/da89fc53444d5a39dddb78fd49eba88a/image.png)
   
if influxdb is connecting, it will show "datasource is working. 4 buckets found" on buttom   
![image](/uploads/03ef1c3f640e86f5fdb8feca9f2f88b1/image.png)   
   
import dashboard  
![image](/uploads/c0e82a4d0f2417e68d487f7842dc9769/image.png)
![image](/uploads/29ec09519e40e26bd0528361318c4efc/image.png)
   
select influxdb data source and import     
![image](/uploads/f09f91e6fbe14d5093bd071d9febebd5/image.png)  
   
base on warning message, we need to install html-plugin   
link: https://gapit-htmlgraphics-panel.gapit.io/docs/installation/   
![image](/uploads/1fd3e358c244e23b632efd93a0b885c6/image.png)   
```shell
sudo mkdir /var/lib/grafana/plugins
sudo grafana-cli plugins install gapit-htmlgraphics-panel
sudo systemctl restart grafana-server
```   
![image](/uploads/105a95288633bb572d5458dc5238b018/image.png)   
   
refresh browser   
 ![image](/uploads/8ec59dc0742e9f1230ddc729dd083993/image.png)
   
# Edge Installation 
   
install openvino toolkit   
```shell
sudo apt install python3-dev python3-pip
pip3 install --upgrade pip
pip3 install openvino-dev[tensorflow2,onnx]
```
![image](/uploads/641328dc60b307be65ea0c719a638f7f/image.png)
![image](/uploads/fa7a0279031b11848870147b955dd2e3/image.png)
![image](/uploads/32dc16cd383e244eb2505ee100d0627b/image.png)
   
install other lib   
```shell
sudo apt install intel-gpu-tools 
pip3 install paho-mqtt  
pip3 install psutil
```
![image](/uploads/e74edf250f675adfaaa786246e9c33c9/image.png)
![image](/uploads/e0441a2f58da250ca0625f52d66beeda/image.png)
![image](/uploads/ca1d75797e538988a5d19912970bf58f/image.png)
    
run edge services
```shell
cd dev/meter-reader/edge/openvino
python3 ./systeminfo.py

#open another terminal
python3 ./meter.py
```
![image](/uploads/443e389e733751bb2f6f6900b5870928/image.png)
   
if edge and server not in the same machine, you only need to edit ip address   
![image](/uploads/2d30bd7cb86e562a39994a2abdcd1b35/image.png)
    
open browser and refresh grafana  
home->Dashboards->Demo   
![image](/uploads/f204a79fb0a4b2524748b09502fe10c3/image.png)
![image](/uploads/b0847d4193827644783edce68b4f66ca/image.png) 
   
finish   
![image](/uploads/6b6c616b7fffc5ad5573c7d7445b1eb6/image.png)
![image](/uploads/ebfd3a8f919f32cd0736d9582d29f3a5/image.png)
![image](/uploads/c14ddb9548d8772674584772219e9d53/image.png)
![image](/uploads/b4d2a42f276783e7b3fab547f0f104a0/image.png)
   
