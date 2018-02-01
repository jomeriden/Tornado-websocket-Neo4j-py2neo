import subprocess
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
from py2neo import Graph
import json

# Database connection
db = Graph()

# Sensor class, to save the info of each sensor and build the web app


class Sensor:
    def __init__(self,georef,descript):
        self.georeference = georef
        self.description = descript

# Queries a utilizar para obtener los datos de los sensores, habitaciones y el edificio
# Match (d:Device)-[:BELONGS_TO]->(n:Room)-[:BELONGS_TO]->(f:Floor) where f.id="P00" return d
# Match (n:Room)-[:BELONGS_TO]->(f:Floor) where f.id="P00" return n
# match (n:Building) return n

# Code to insert in the web app, here we introduce coordinates and description


sensorCode = """{
    type: 'Feature',
    geometry: {
      type: 'Point',
      coordinates: [sensorPoint]
    },
    properties: {
      title: 'Escuela Politecnica Caceres - Edificio Informatica',
      description: 'sensorDescription'
    }
  }"""

# Queries to get the sensors on each floor

queryDevicesP00 = """Match (d:Device)-[:BELONGS_TO]->(n:Room)-[:BELONGS_TO]->(f:Floor) where f.id="P00" 
return d.location as location, d.description as description"""

queryDevicesP01 = """Match (d:Device)-[:BELONGS_TO]->(n:Room)-[:BELONGS_TO]->(f:Floor) where f.id="P01" 
return d.location as location, d.description as description"""

# This methods generate the code of the sensors of each floor and insert them in the web app code


def generateDevicesP00():
    data = db.run(queryDevicesP00)
    aux = []
    for i in data:
        aux.append(i)
    dataResult = json.dumps(aux, sort_keys=True, indent=4, separators=(',', ': '))
    insertCode(generateSensorList(dataResult), 0)


def generateDevicesP01():
    data = db.run(queryDevicesP01)
    aux = []
    for i in data:
        aux.append(i)
    dataResult = json.dumps(aux, sort_keys=True, indent=4, separators=(',', ': '))
    insertCode(generateSensorList(dataResult), 1)

# this method implement the parser of the info received to generate a geojson with all the sensors
# using the sensorCode


def generateSensorList(jsonresult):
    sensorList = []
    point = False
    text = False
    complete = False
    textDescript = ""
    latitude = ""
    longitude = ""
    resultParts = jsonresult.split()
    for n in resultParts:
        if n.find("(-") >= 0:
            latitude = n.replace("(", " ")
            point = True
        else:
            if point:
                    text = True
                    point = False
                    longitude = n.replace(""")",""", " ")
            else:
                if text:
                    if n.find(",") == -1:
                        textDescript = textDescript + " " + n
                    else:
                        text = False
                        complete = True
        if complete:
            sensorList.append(Sensor(latitude + ", " + longitude, textDescript))
            textDescript = ""
            complete = False

    geojson = ""
    first = True
    for i in sensorList:
        sensorCodeAux = sensorCode.replace("sensorPoint", i.georeference)
        sensorCodeAux = sensorCodeAux.replace("sensorDescription", i.description)
        if first:
            geojson = sensorCodeAux
            first = False
        else:
            geojson = geojson + ", " + sensorCodeAux
    return geojson

# Insert the generated geojson code in the final web app


def insertCode(code, floor):
    if floor == 0:
        f = open("indexMap.html", 'r')
        webread = f.read()
        webread = webread.replace("geojsonNeo4jP00", code)
        f.close()
        webwrite = open("indexMapFinal.html", 'w')
        webwrite.write(webread)
        webwrite.close()
    else:
        f = open("indexMapFinal.html", 'r')
        webread = f.read()
        webread = webread.replace("geojsonNeo4jP01", code)
        f.close()
        webwrite = open("indexMapFinal.html", 'w')
        webwrite.write(webread)
        webwrite.close()

# Queries to get all the info stored in Neo4j


attributeQuery = """
 MATCH (n:type) WHERE n.id={id} RETURN n.attribute
 """

initialQuery = """
 MATCH (n:type) WHERE n.id={id} RETURN n
 """

curlQuery = """
 MATCH (n:type) WHERE n.id={id} RETURN n.query
 """

initialQueryList = """
 MATCH (n:type) RETURN n
 """

query4all = """
 MATCH (n) RETURN n
 """

# Method to consult the Neo4j database to consult the Rethink db datbase to get info about sensor data using CURL


def executeQueryCurl(_id, _type):
    query = curlQuery.replace("type", _type)
    head, sep, tail = _id.partition('.')
    data = db.run(query, id=head.upper())
    aux = []
    for i in data:
        aux.append(i)
    resultCurl = json.dumps(aux, sort_keys=True, indent=4, separators=(',', ': '))
    data = resultCurl.replace("[", "")
    data = data.replace("]", "")
    data = data.replace("\"c", "c")
    data = data.replace("h\\\"", "h")
    data = data.replace("\\", "")
    output = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE)
    result = output.stdout.read()
    return result.decode('ascii')

# Method that execute a query to receive every data in the DB


def executeQuery4All():
    data = db.run(query4all)
    aux = []
    for d in data:
        aux.append(d)
    return aux

# Method that execute a query to receive every node of a concrete type or only one by his ID


def executeQuery(_id, _type):
    if toCapitalize(_id) == "All":
        query = initialQueryList.replace("type", _type)
        data = db.run(query)
    else:
        query = initialQuery.replace("type", _type)
        data = db.run(query, id=_id.upper())
    aux = []
    for i in data:
        aux.append(i)
    return aux

# Method that execute a query to receive only one attribute of a node


def executeQueryAttribute(_id, _type):
    query = attributeQuery.replace("type", _type)
    head, sep, tail = _id.partition('.')
    query = query.replace("attribute", tail.lower())
    data = db.run(query, id=head.upper())
    aux = []
    for i in data:
        aux.append(i)
    return aux

# To capitalize the messages received


def toCapitalize(data):
    low = data.lower()
    return low.capitalize()

# return the type of the node


def getType(message):
    type = message.rpartition(':')[0]
    return toCapitalize(type)

# return the id of the node


def getId(message):
    head, sep, tail = message.partition(':')
    return tail

# this method select what kind of queries had sent by the user to use the correct queries and methods


def getJson(message):
    if toCapitalize(message) == "All":
        dataResult = json.dumps(executeQuery4All(), sort_keys=True, indent=4, separators=(',', ': '))
    else:
        nodeType = getType(message)
        nodeId = getId(message)
        if nodeId.find(".") == -1:
            dataResult = json.dumps(executeQuery(nodeId, nodeType), sort_keys=True, indent=4, separators=(',', ': '))
        else:
            if nodeId.find(".show") == -1:
                dataResult = json.dumps(executeQueryAttribute(nodeId, nodeType), sort_keys=True, indent=4,
                                        separators=(',', ': '))
            else:
                dataResult = executeQueryCurl(nodeId, nodeType)
    return dataResult

# Class that serve the web app to the users when them do a handshake to the API.


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        generateDevicesP00()
        generateDevicesP01()
        self.render("indexMapFinal.html")

# Class that implements the WebSocket


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = []

    def open(self):
        print 'new connection'
        WebSocketHandler.clients.append(self)

    def on_message(self, message):
        print 'message received: %s' % message
        result = getJson(message)
        print 'sending back message: %s' % result
        self.write_message(result)

    def on_close(self):
        print 'connection closed'
        WebSocketHandler.clients.remove(self)

    def check_origin(self, origin):
        return True

# Definitions of handlers nad files needed to serve the web app


application = tornado.web.Application([
            (r'/', IndexHandler),
            (r'/ws', WebSocketHandler),
            (r"/img/(.*)", tornado.web.StaticFileHandler, {"path": "./img"},),
            (r"/css/(style.\css)", tornado.web.StaticFileHandler, {"path": "./css"},),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()


