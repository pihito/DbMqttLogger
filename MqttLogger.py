#TODO doc
#TODO License

import paho.mqtt.client as mqtt
import logging
import logging.config
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure,InvalidName
import json
import datetime

logging.config.fileConfig('logging.conf')

#TODO Gestion des erreurs au chargement du message MQTT
class NodeMsg : 
    
    HOME_STR = "home"
    ROOM_STR = "room"
    DATA_STR = "data"
    logger = logging.getLogger('nodeMsg')
    
    def __init__(self,home = "",piece = "",data=None) :
        self.home = home
        self.piece = piece
        self.home = piece
        self.data = data
        
    
    def toDicData(self,key) : 
        data = { self.HOME_STR : self.home,self.ROOM_STR : self.piece,self.DATA_STR : self.data[key]}
        return data
    
    def toDicData(self) : 
        data = { self.HOME_STR : self.home,self.ROOM_STR : self.piece,self.DATA_STR : self.data}
        return data
    
    def toString(self) : 
        return self.HOME_STR +":"+ self.home +" "+ self.ROOM_STR +":"+ self.piece+" "+ self.DATA_STR + str(self.data)
    
    def addData(self,key,v) : 
        self.data[key]=v
    
    def loadJSON(self,strJSON) :
        dictJson = json.loads(strJSON)
        self.home = dictJson[HOME_STR] 
        self.piece = dictJson[ROOM_STR]
        self.data = dictJson[DATA_STR]
        self.logger.debug(self.toString())
        
    def loadMQTTMsg(self,topic,bJSON) : 
        t = topic.split('/')
        self.home = t[0]
        self.piece = t[1]
        s = str(bJSON)
        s = s[2:len(s)-1]
        self.data = json.loads(s)
        self.data["date"] = datetime.datetime.utcnow()
        self.logger.debug(self.toString())
        
        
        
class MqttClient :

    client = mqtt.Client()
    logger = logging.getLogger('mqtt')
    
    def __init__(self,serveur="localhost",port=1883,dbStore=None) :
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(serveur, port, 60)
        self.dbStore = dbStore 

    def subscribe(self,channel) :
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.client.subscribe(channel)

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self,client, userdata, flags, rc):
        self.logger.info("Connected with result code "+str(rc))
        

    # The callback for when a PUBLISH message is received from the server.
    #TODO Ne pas enregistrer si le message n'est pas correctement chargé
    def on_message(self,client, userdata, msg):
        self.logger.debug(msg.topic+" "+str(msg.payload))
        nodeMsg = NodeMsg()
        nodeMsg.loadMQTTMsg(msg.topic,msg.payload)
        self.dbStore.addNodeMsg(nodeMsg)
        
        
    def mainLoop(self) : 
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        self.client.loop_forever()
 

class DbStore : 
    
    logger = logging.getLogger('db')
    
    def __init__(self,server='localhost:27017') : 
        try : 
            self.client = MongoClient(server)
            self.logger.info("db connnection ok")
        
        except ConnectionFailure as e:
            self.logger.error("db connection failure ")
        except Exception as e: 
            self.logger.error("db connection failure unknow exeception")

    
    def addNodeMsg(self,nodeMsg,dbNameParam=None,collecNameParam=None):
        db = None
        collec=None
        dbName = dbNameParam
        collecName = collecNameParam
        
        if dbName == None :
            dbName = nodeMsg.home
           
        if collecName == None :
            collecName = nodeMsg.piece
        
        self.logger.debug("db : " + dbName)      
        self.logger.debug("collec : " + collecName)
        
        try :
            db = self.client[dbName]
        except InvalidName as e: 
            self.logger.error("impossible d'ouvrir la db :" + dbName)
        
        try : 
             collec = db[collecName]   
        except InvalidName as e1: 
            self.logger.error("impossible d'ouvrir la collection :" + collecName)
        
        self.logger.debug("tentative d'insetion :")    
        sgId = collec.insert_one(nodeMsg.data).inserted_id
        self.logger.debug("message inserted id : " + str(sgId))
        self.logger.debug("insertion ok")

#    def get_country(db):
#        return db.countries.find_one()

if __name__ == '__main__' :    
    
    logger = logging.getLogger('root')
    logger.info("***starting to store MQTT msg to database")
    
    db = DbStore('192.168.1.30:27017')
    
    logger.info("***connecting to mqtt and subscribe")
    mqttClient = MqttClient("192.168.1.30", 1883,db)
    mqttClient.subscribe("SebHome/HugoRoom")
    
    logger.info("***Log message")
    mqttClient.mainLoop()
    

