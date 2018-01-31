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
  }"""

def parseSensorCode():
    sensorCode4All = ""
    sensorCodeParsed =
    sensorCode4All = sensorCode4All + ',' + sensorCodeParsed
    return sensorCode4All

f = open("indexMap.html", 'r')
webread = f.read()
webread = webread.replace("geojsonNeo4j",
                      "sensorGeopoint")

f.close()

webwrite = open("indexMap2.html", 'w')
webwrite.write(webread)
webwrite.close()