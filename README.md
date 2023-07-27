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
    
unzip large files    
```shell
sudo chmod +x ./extract.sh    
./extract.sh
```     
![image](./screenshot/0.png)    
    
nodejs   
link: https://tecadmin.net/install-latest-nodejs-npm-on-ubuntu/
   
```shell
sudo apt install -y curl 
curl -sL https://deb.nodesource.com/setup_18.x | sudo -E bash - 
sudo apt install -y nodejs 
```  
![image](./screenshot/1.png)
![image](./screenshot/2.png)
![image](./screenshot/3.png) 
   

validate install  
```shell
node -v
#v18.16.1

npm -v 
#9.5.1
```   
![image](./screenshot/4.png)    
   
- node-red installation  
link: https://nodered.org/docs/getting-started/local
   
move to the node-red folder   
```shell
cd dev/meter-reader/server/nodered/
sudo npm install -g --unsafe-perm node-red
node-red
```
![image](./screenshot/5.png)
![image](./screenshot/6.png)
   
You can then access the Node-RED editor by pointing your browser at http://localhost:1880.    
*we need to install some node in next config session.       
![image](./screenshot/7.png)
    
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
![image](./screenshot/8.png)
![image](./screenshot/9.png)
![image](./screenshot/10.png)
![image](./screenshot/11.png)
   
Open the browser and type: http://localhost:8086
![image](./screenshot/12.png)
   
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
![image](./screenshot/13.png)
![image](./screenshot/14.png)
![image](./screenshot/15.png)
![image](./screenshot/16.png)
   
Open your web browser and go to http://localhost:3000/
![image](./screenshot/17.png)
    

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
![image](./screenshot/18.png)
   
- openvino(edge)      
edge meter sample files in ***/data***     
connect container   
```shell
docker exec -it iEi.openvino /bin/bash
cd /data
```
![image](./screenshot/19.png)
![image](./screenshot/20.png)
   
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
![image](./screenshot/21.png)
![image](./screenshot/22.png)
   
copy and save this token. we will use it in other step   
![image](./screenshot/23.png)
![image](./screenshot/24.png)   
   
choose get started and then choose buckets   
![image](./screenshot/25.png)
![image](./screenshot/26.png)
   
create buckets and name "**meter**"  
![image](./screenshot/27.png)   
![image](./screenshot/28.png)
   
- node-red(pre-load flows.json)  
if you install and start host version in meter-reader/server/nodered ,it was pre-load flows.json   
we don't need to import flows.json again     
![image](./screenshot/29.png)
   
base on warning message, we need to install missing node.   
![image](./screenshot/30.png)
   
menu -> manage palette   
![image](./screenshot/31.png)
   
search missing node and install it   
![image](./screenshot/32.png)
![image](./screenshot/33.png)
![image](./screenshot/34.png)
![image](./screenshot/35.png)
   
missing node full name   
![image](./screenshot/36.png)
    
next step we will setup node-red influxdb node  
please double click one of influxdb node  
![image](./screenshot/37.png) 
   
edit server   
![image](./screenshot/38.png)
   
copy and paste token, and update it, and done.   
![image](./screenshot/39.png)
![image](./screenshot/40.png)
   
Deploy    
![image](./screenshot/41.png)
![image](./screenshot/42.png)
    
- grafana   

setup username and password   
![image](./screenshot/43.png)
![image](./screenshot/44.png)
    
setup data source   
![image](./screenshot/45.png)
   
choose influxdb
![image](./screenshot/46.png)
   
quenry language choose Flux(1.8+)   
![image](./screenshot/47.png)
![image](./screenshot/48.png)

type influxdb information as pre-step    
*HTTP(URL), Auth(Basic auth), Basic Auth Details(User/Password), InfluxDB Details(Organization/Token)   
![image](./screenshot/49.png)
   
if influxdb is connecting, it will show "datasource is working. 4 buckets found" on buttom   
![image](./screenshot/50.png)   
   
import dashboard  
![image](./screenshot/51.png)
![image](./screenshot/52.png)
   
select influxdb data source and import     
![image](./screenshot/53.png)  
   
base on warning message, we need to install html-plugin   
link: https://gapit-htmlgraphics-panel.gapit.io/docs/installation/   
![image](./screenshot/54.png)   
```shell
sudo mkdir /var/lib/grafana/plugins
sudo grafana-cli plugins install gapit-htmlgraphics-panel
sudo systemctl restart grafana-server
```   
![image](./screenshot/55.png)   
   
refresh browser   
![image](./screenshot/56.png)
   
# Edge Installation 
   
install openvino toolkit   
```shell
sudo apt install python3-dev python3-pip
pip3 install --upgrade pip
pip3 install openvino-dev[tensorflow2,onnx]
```
![image](./screenshot/57.png)
![image](./screenshot/58.png)
![image](./screenshot/59.png)
   
install other lib   
```shell
sudo apt install intel-gpu-tools 
pip3 install paho-mqtt  
pip3 install psutil
```
![image](./screenshot/60.png)
![image](./screenshot/61.png)
![image](./screenshot/62.png)
    
run edge services
```shell
cd dev/meter-reader/edge/openvino
python3 ./systeminfo.py

#open another terminal
python3 ./meter.py
```
![image](./screenshot/63.png)
   
if edge and server not in the same machine, you only need to edit ip address   
![image](./screenshot/64.png)
    
open browser and refresh grafana  
home->Dashboards->Demo   
![image](./screenshot/65.png)
![image](./screenshot/66.png) 
   
finish   
![image](./screenshot/67.png)
![image](./screenshot/68.png)
![image](./screenshot/69.png)
![image](./screenshot/70.png)
   
