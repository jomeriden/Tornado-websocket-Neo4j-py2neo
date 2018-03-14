[Documentación del proyecto WebSocket Neo4SP](https://drive.google.com/file/d/1sjUN3qvvmZtI6IyLHmxn5ABBPIjVHy87/view?usp=sharing)

# WebSocket Neo4SP

El motivo principal por el cual se ha desarrollado este proyecto es el de dotar a
la plataforma **SmartPolitech**, desarrollada en la **Escuela Politécnica de Cáceres**, de
un servicio que proporcione la información de la arquitectura, datos arquitectónicos,
georeferencias y datos de monitorización de diferentes variables relativas al contexto
de los edificios de dicha institución.
Esta información se encuentra almacenada en las bases de datos NoSql Neo4j,
para los datos arquitectónicos y georeferencias, y RethinkDB, para los datos de monitorizaci
ón.

  Al iniciar este proyecto con la idea de conseguir dicho servicio que proporcionase
la información que contenían las bases de datos y una aplicación que proporcionase
la información de forma visual e interactiva. Por lo tanto, los dos objetivos que se
querían conseguir eran:

  * Desarrollar una **API** que sirviera la información referente a los edificios, estancias,
  sensores y demás elementos que se encuentren en las bases de datos que se
  han comentado. Este servicio debe proporcionar una forma sencilla de acceder
  a los datos, es decir, facilitando las consultas y unificando el sistema de envío
  de peticiones al servidor mediante el envío de mensajes solicitando el dato concreto,
  algo que proporciona el Websocket, que más adelante se expondrá como
  se incorpora a estos objetivos.

  * Implementar una **aplicación Web** que ofrezca la información de las bases de
  datos en una plataforma que muestre dichos datos de forma gráfica y permita
  interactuar con el usuario. En este caso interviene el uso de tecnologías ya
  usadas por otros proyectos, es el caso de Mapbox, que proporciona la posibilidad
  de generar un mapa y posicionar elementos en el mapa, edificios y dispositivos
  almacenados en las bases de datos, así como ofrecer información sobre ellos al
  interactuar con ellos.

  De estos objetivos principales surgieron otros que también tienen importancia
para obtener un rendimiento mayor al software final. Estos son:

  * **Actualizar las estructuras de las bases de datos** Neo4j y RethinkDB para
  que contengan nuevos datos debido a las necesidades que producen diversas
  aplicaciones o plugins, como es el caso de Neo4j.spatial, el cual proporciona un
  sistema para el almacenamiento para representaciones geométricas, y obtener
  una versión modernizada y más compacta.

  * Implementar un **WebSocket** para la comunicación con el servicio ya que es un
  protocolo ligero, ofrece una comunicación bidireccional y Full-duplex a través
  de una sola conexión TCP, además de un envío de mensajes, entre él y el
  usuario, muy rápido.

  * Desarrollar un sistema de **consultas diseñadas** para facilitar la petición de
  los datos que nos ofrecen las bases de datos, con la funcionalidad de que el usuario
  pueda consultar dicha información de forma sencilla y no le lleve mucho tiempo
  construir la consulta para los datos requeridos o para que el desarrollador de
  aplicaciones que use la API, tenga un fácil acceso a los datos que desea procesar
  sin tener que poner una url.

  * Diseñar una **Web que muestre la información** de las bases de datos a
  través de la que cualquier usuario pueda consultar la información que necesite
  mediante el uso de envío de mensajes al WebSocket, dichos mensajes serán las
  consultas diseñadas que se han expuesto en el punto anterior, para probar de
  esta manera la API desarrollada y ofrecer tal servicio a cualquier usuario que
  quiera consulta la información o para un desarrollador que quiera probar el
  funcionamiento de este servicio.
  
## Estructura del proyecto
  
Este proyecto consta de una estructura muy simple, se compone de varios archivos
de distinta índole, como pueden ser Python, HTML, CSS e imágenes PNG.
Para poder desarrollar una mejora o simplemente ver su funcionamiento interno,
se necesita configurar el sistema para que permita el uso de Python y otras tecnologías. 

Para dicha instalación basta con consultar la [Documentación del proyecto WebSocket Neo4SP](https://drive.google.com/file/d/1sjUN3qvvmZtI6IyLHmxn5ABBPIjVHy87/view?usp=sharing) y 
seguir los pasos que ahí se describen.

En la organización del proyecto se puede observar un par de carpetas dentro del 
directorio src del proyecto. Estas carpetas tienen almacenan el estilo de la Web para
visualización de datos, en el caso de css, y las imágenes PNG que se muestran en ambas
aplicaciones en img.

El resto pertenece a los códigos de los WebSockets, uno para cada aplicación,
las Webs que sirven estos y la plantilla que se procesa para generar el mapa con
los sensores. Para tener un conocimiento más concreto de que función cumple cada
archivo se explicarán a continuación:

  * **ws_app.py**: este archivo contiene el código, escrito en Python, del WebSocket
  que sirve la Web para visualización de datos y que puede servir de API para
  futuras aplicaciones.
  
  * **ws_maobbox_app.py**: documento que encierra la implementación, también
  usando Python del Websocket que genera la Web para posicionamiento geográfico 
  de sensores y la sirve.
  
  * **graphGenerate.py**: engloba el procesamiento de la plantilla de la Web para
  posicionamiento geográfico de sensores para generar la versión final de esta.

  * **index.html**: contiene el código HTML y JavaScript que forma la Web para
  visualización de datos.
  
  * **indexMap.html**: plantilla de la Web para posicionamiento geográfico de sensores,
  la cual es utilizada para generar la aplicación final.
  
  * **indexMapFinal.html**: documento generado por el ws_maobbox_app.py, el
  cual lo servirá con todos los sensores almacenados en la base de datos Neo4j.
 
Por último, para diseñar el mapa que se muestra en la aplicación y sus capas
(plantas del edificio), solo habrá que seguir los pasos indicados en el anexos de la
[Documentación del proyecto](https://drive.google.com/file/d/1sjUN3qvvmZtI6IyLHmxn5ABBPIjVHy87/view?usp=sharing).
