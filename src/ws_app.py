import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
from py2neo import Graph
import json

db = Graph()

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


def executeQuery(_id, _type):
    if toCapitalize(_id) == "All":
        query = initialQueryList.replace("type", _type)
        data = db.run(query)
    else:
        if _id.find("show") == -1:
            query = initialQuery.replace("type", _type)
            data = db.run(query, id=_id.upper())
        else:
            query = curlQuery.replace("type", _type)
            head, sep, tail = _id.partition('.')
            print head + " " + tail
            data = db.run(query, id=head.upper())
            # resultCurl = json.dumps(aux, sort_keys=True, indent=4, separators=(',', ': '))
            # resultCurl = resultCurl.replace("[", "")
            # print resultCurl.replace("]", "")
    aux = []
    for i in data:
        print(i)
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
        dataResult = json.dumps(executeQuery(nodeId, nodeType), sort_keys=True, indent=4, separators=(',', ': '))
    return dataResult

def executeQuery4All():
    data = db.run(query4all)
    aux = []
    for d in data:
        print(d)
        aux.append(d)
    return aux


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'new connection'

    def on_message(self, message):
        print 'message received: %s' % message
        result = getJson(message)
        print 'sending back message: %s' % result
        self.write_message(result)

    def on_close(self):
        print 'connection closed'

    def check_origin(self, origin):
        return True


application = tornado.web.Application([
            (r'/ws', WebSocketHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


