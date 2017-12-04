import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
from py2neo import Graph
import json


uri = "bolt://localhost:7687"
db = Graph()

# query = """
# MATCH (n:Device) WHERE n.id={id} RETURN n.description
# """
query2 = """
MATCH (n:Device) RETURN n
"""

# def executeQuery(_id):
#    data = db.run(query, id=_id)
#    for d in data:
#        print(d)
#    return data


def executeQuery():
    data = db.run(query2)
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
        result = json.dumps(executeQuery())
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


