from py2neo import Graph
import json

db = Graph()


class Sensor:
    def __init__(self,georef,descript):
        self.georeference = georef
        self.description = descript


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
data = db.run(queryDevicesP00)
aux = []
print('-------------------------Dentro de bucle-----------------------------------')
for i in data:
    print(i)
    aux.append(i)
print('-------------------------Fuera de bucle------------------------------------')
dataResult = json.dumps(aux, sort_keys=True, indent=4, separators=(',', ': '))
print(dataResult)
sensorList = []
point = False
text = False
complete = False
textDescript = ""
latitude = ""
longitude = ""
resultParts = dataResult.split()
print(resultParts)
for i in resultParts:
    if i.find("(-") >= 0:
        latitude = i.replace("(", " ")
        point = True
    else:
        if point:
                text = True
                point = False
                longitude = i.replace(""")",""", " ")
        else:
            if text:
                if i.find(",") == -1:
                    textDescript = textDescript + " " + i
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

f = open("indexMap.html", 'r')
webread = f.read()
webread = webread.replace("geojsonNeo4j",
                      geojson)

f.close()

webwrite = open("indexMap2.html", 'w')
webwrite.write(webread)
webwrite.close()