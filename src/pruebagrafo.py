from py2neo import Graph
import json

db = Graph()


class Sensor:
    def __init__(self,georef,descript):
        self.georeference = georef
        self.description = descript

# Queries a utilizar para obtener los datos de los sensores, habitaciones y el edificio
# Match (d:Device)-[:BELONGS_TO]->(n:Room)-[:BELONGS_TO]->(f:Floor) where f.id="P00" return d
# Match (n:Room)-[:BELONGS_TO]->(f:Floor) where f.id="P00" return n
# match (n:Building) return n


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


def parseSensorCode():
    sensorCode4All = ""
    sensorCodeParsed = ""
    sensorCode4All = sensorCode4All + ',' + sensorCodeParsed
    return sensorCode4All


queryDevicesP00="""Match (d:Device)-[:BELONGS_TO]->(n:Room)-[:BELONGS_TO]->(f:Floor) where f.id="P00" 
return d.location as location, d.description as description"""

queryDevicesP01="""Match (d:Device)-[:BELONGS_TO]->(n:Room)-[:BELONGS_TO]->(f:Floor) where f.id="P01" 
return d.location as location, d.description as description"""


def generateDevicesP01():
    data = db.run(queryDevicesP01)
    aux = []
    for i in data:
        aux.append(i)
    dataResult = json.dumps(aux, sort_keys=True, indent=4, separators=(',', ': '))
    geojsonResult = generateSensorList(dataResult)
    insertCode(geojsonResult, 1)


def generateDevicesP00():
    data = db.run(queryDevicesP00)
    aux = []
    for i in data:
        aux.append(i)
    dataResult = json.dumps(aux, sort_keys=True, indent=4, separators=(',', ': '))
    geojsonResult = generateSensorList(dataResult)
    insertCode(geojsonResult, 0)


def generateSensorList(jsonresult):
    sensorList = []
    point = False
    text = False
    complete = False
    textDescript = ""
    latitude = ""
    longitude = ""
    resultParts = jsonresult.split()
    print(resultParts)
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
        print("Geopunto: "+i.georeference+", Descripcion: "+i.description)
        sensorCodeAux = sensorCode.replace("sensorPoint", i.georeference)
        sensorCodeAux = sensorCodeAux.replace("sensorDescription", i.description)
        if first:
            geojson = sensorCodeAux
            first = False
        else:
            geojson = geojson + ", " + sensorCodeAux
    print(geojson)
    return geojson


def insertCode(code, floor):
    if floor == 0:
        f = open("indexMap.html", 'r')
        webread = f.read()
        webread = webread.replace("geojsonNeo4jP00", code)
        f.close()
        webwrite = open("indexMap2.html", 'w')
        webwrite.write(webread)
        webwrite.close()
    else:
        f = open("indexMap2.html", 'r')
        webread = f.read()
        webread = webread.replace("geojsonNeo4jP01", code)
        f.close()
        webwrite = open("indexMap2.html", 'w')
        webwrite.write(webread)
        webwrite.close()


generateDevicesP00()
generateDevicesP01()