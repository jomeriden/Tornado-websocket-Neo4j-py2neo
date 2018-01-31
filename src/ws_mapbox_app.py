import subprocess
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
from py2neo import Graph
import json

db = Graph()

sensorCode = """{
    type: 'Feature',
    geometry: {
      type: 'Point',
      coordinates: [sensorPoint]
    },
    properties: {
      title: 'Escuela Politécnica Cáceres - Edificio Informática',
      description: 'sensorDescription'
    }
  }]"""

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

def executeQuery4All():
    data = db.run(query4all)
    aux = []
    for d in data:
        aux.append(d)
    return aux

def executeQuery(_id, _type):
    if toCapitalize(_id) == "All":
        query = initialQueryList.replace("type", _type)
        data = db.run(query)
    else:
        query = initialQuery.replace("type", _type)
        data = db.run(query, id=_id.upper())
    aux = []
    for i in data:
        print(i)
        aux.append(i)
    return aux

def executeQueryAttribute(_id, _type):
    query = attributeQuery.replace("type", _type)
    head, sep, tail = _id.partition('.')
    query = query.replace("attribute", tail.lower())
    data = db.run(query, id=head.upper())
    aux = []
    for i in data:
        aux.append(i)
    return aux

def toCapitalize(data):
    low = data.lower()
    return low.capitalize()


def getType(message):
    type = message.rpartition(':')[0]
    print toCapitalize(type)
    return toCapitalize(type)


def getId(message):
    head, sep, tail = message.partition(':')
    print tail
    return tail


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
                dataResult = json.dumps(executeQueryAttribute(nodeId, nodeType), sort_keys=True, indent=4, separators=(',', ': '))
            else:
                dataResult = executeQueryCurl(nodeId, nodeType)
    return dataResult


def setMap():
    source = file(fileChange, 'r+')
    text = source.read()
    if (text.find(oldLine) >= 0):
        print 'la linea esta en el fichero'
        source.write(text.replace(oldLine, newLine))
    else:
        print 'la linea NO esta en el fichero'
        source.write(newLine)
    source.close()


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("indexMap.html")


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


