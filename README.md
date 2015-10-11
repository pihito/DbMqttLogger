# DbMqttLogger
Store MQTT Message to MongoDB

**Ce programme en python 3.4 stocke les message mqtt dans une base mongoDB**, chaque message est stoker dans la base donnée correspondant à sa racine et dans la collection corresponsant au second niveau.  
*example :* SebHome/HugoRoom est stoké dans la db sebhome du serveur et la collection HugoRoom

* **installation**  
*optionel :* créez un environnement virtuel python  
installer les modules python requis : *pip install -r requirements.txt* 
* **lancement**
usage: MqttLogger.py [-h] [--mqttServer MQTTSERVER] [--mqttPort MQTTPORT]
 [--dbServer DBSERVER] SUBCHANNEL
SUBCHANNEL : mon des channel à souscrire separer par un | ex :(SebHome/HugoRoom|SebHome/FloRoom)
 -h, --help            show this help message and exit
 --mqttServer MQTTSERVER adresse du server MQTT (default: 192.168.1.30)
--mqttPort MQTTPORT, -m MQTTPORT port du server MQTT (default: 1883)
--dbServer DBSERVER, -d DBSERVER adresse du serveur mongoDB (default: 192.168.1.30:27017)

* * *
**this is a python 3.4 command line program to subscribe a mqtt channel and store it a mongoDB**.<br>
Each message is record in db under, db and collection where db is the root of your subscription and collection are the child. 
*sample:*subscribe is : SebHome/HugoRoom, the program store in SebHome as database and HugoRoom as collection.

* **install**<br>
*optional: create a python virtualenv*
install python component: *pip install -r requirements.txt* 

* **run** <br>
usage: MqttLogger.py [-h] [--mqttServer MQTTSERVER] [--mqttPort MQTTPORT] [--dbServer DBSERVER] SUBCHANNEL [xxx/xxxx|xxx/Xxx]
SUBCHANNEL is the mqtt channel to subscribe separate by a |


