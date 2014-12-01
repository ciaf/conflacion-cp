conflacion-cp
=============
Scripts del proceso de conflación de *centros poblados centroide* (DANE) y *administrativo_punto* (IGAC)
El script conflacion_cp.py se encarga de tomar los archivos de las dos fuentes de información, recorrerlos y comparar los nombres empleando técnicas de *Procesamiento de Lenguaje Natural*. 
Se toma cada centro poblado centroide (DANE) contra cada uno de los registros de la capa administrativo_punto (IGAC) que se encuentran en el mismo municipio del centro poblado base. 
El script conflacion_cp.py se basa en varias librerías de software libre como la nltk (Natural Language Tool Kit), fiona (para leer los Shapefiles), unidecode y re, y produce como resultado 3 listados:
* **concuerdan.csv**: Listado de entidades coincidentes (dadas ciertas reglas de semejanza entre nombres). Puede haber duplicados, esto es, un CP del DANE corresponde a varios CP IGAC dentro del mismo municipio. En caso de duplicados, debe desambiguarse manualmente. Las reglas de semejanza hacen flexible la correspondencia entre dos nombres sin importar si difieren en tildes, en mayúsculas/minúsculas, en espacios en blanco (ej. PUNTA DE OCAIDO vs. Punta Deocaido), en guiones y paréntesis (ej. LA MARÍA - EL TRAPICHE vs. La María (El Trapiche)), en un artículo prefijo (ej. BAGRE vs. El Bagre), o en algunos sinónimos (ej. VEINTE DE JULIO vs. 20 de Julio o KILÓMETRO 32 vs. Km 32).
* **no_concuerdan_dane.csv**: Listado de centros poblados centroide del DANE que no concuerdan con ningún registro administrativo_punto IGAC. Es decir, los centros poblados de concuerdan.csv + los de no_councuerdan_dane.csv sumarían todos los centros poblados centroide del DANE (si no existieran duplicados en concuerdan.csv).
* **similares.csv**: Listado de entidades no coincidentes pero similares (ej. LA BARRIALOSA vs. La Barrilosa, TIPISCA vs. San Pedro de Tipisca, SAN MIGUEL DE FARALLONES vs. San Miguel De Los Farallones). Este listado es un insumo para desambiguar coincidencias no tan evidentes.
Cabe aclarar que las dos fuentes de información empleadas ofrecen sus datos a través de servicios OGC-WFS (Web Feature Service), que fueron descargados en noviembre de 2014 para la realización de este ejercicio de conflación. Las URLs de descarga de los datos originales son:
* Centros Poblados Centroide (DIVIPOLA, DANE): https://www.dane.gov.co/geoserver/divipola/ows?version=1.0.0&SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&TYPENAME=divipola:DIVIPOLA_CENTROS_POBLADOS_CENTROIDE&SRSNAME=EPSG:4326
* Administrativo_Punto (Cartografía, IGAC): http://geocarto.igac.gov.co:8082/geoservicios/cien_mil/wfs?request=GetFeature&version=1.0.0&service=wfs&typeName=cien_mil:Administrativo_Punto
Adicionalmente, el script hace uso de la capa de Municipios de la DIVIPOLA, DANE, con el fin de recorrer uno a uno los municipios del país. Dicha capa se encuentra en la dirección: 
https://www.dane.gov.co/geoserver/divipola/ows?version=1.0.0&SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&TYPENAME=divipola:DIVIPOLA_MUNICIPIOS&SRSNAME=EPSG:4326 
#### ¿Cómo ejecutar el script?
1. Instalar las dependencias del script: Python 2.x, fiona, nltk, re, unidecode.
2. Ajustar el prefijo de la ruta a los Shapefiles fuente (variable `prefix`, línea 6 del script).
3. Crear un directorio "listados" en la ruta asignada a la variable `prefix`, de tal manera que se pueda acceder a prefix + "listados".
3. Desde la carpeta asignada a la variable `prefix`, ejecutar desde la terminal de comandos: `python ./conflacion_cp.py`
Más información en el blog [http://servidor/x.html](http://igac.gov.co)
