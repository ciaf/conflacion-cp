conflacion-cp
=============

Scripts del proceso de conflación de *centros poblados centroide* (DANE) y *administrativo_punto* (IGAC)

El script x.py se encarga de tomar los archivos de las dos fuentes de información, recorrerlos y comparar los nombres empleando técnicas de *Procesamiento de Lenguaje Natural*. 

Se toma cada centro poblado centroide (DANE) contra cada uno de los registros de la capa administrativo_punto (IGAC) que se encuentran en el mismo municipio del centro poblado base. 

El script x.py se basa en varias librerías de software libre como la nltk (Natural Language Tool Kit), fiona (para leer los Shapefiles), unidecode y re, y produce como resultado 4 listados:

* **concuerdan.csv**: Listado de entidades coincidentes (dadas ciertas reglas de semejanza entre nombres). Puede haber duplicados, esto es, un CP del DANE corresponde a varios CP IGAC dentro del mismo municipio. En caso de duplicados, debe desambiguarse manualmente. Las reglas de semejanza hacen flexible la correspondencia entre dos nombres sin importar si difieren en tildes, en mayúsculas/minúsculas, en espacios en blanco, en guiones y paréntesis, o en un artículo prefijo (ej. Flores vs. Las Flores ).
* **no_concuerdan_dane.csv**: Listado de centros poblados centroide del DANE que no concuerdan con nungún registro administrativo_punto IGAC. Es decir, los centros poblados de concuerdan.csv + los de no_councuerdan_dane.csv sumarían todos los centros poblados centroide del DANE (si no existieran duplicados en concuerdan.csv).
* **similares.csv**: Listado de entidades no coincidentes pero similares (ej. LA BARRIALOSA vs. La Barrilosa, TIPISCA vs. San Pedro de Tipisca, SAN MIGUEL DE FARALLONES vs. San Miguel De Los Farallones). Este listado es un insumo para desambiguar coincidencias no tan evidentes.
* **no_concuerdan_carto.csv**: Listado de todas las entidades de cartografía.

Cabe aclarar que las dos fuentes de información empleadas ofrecen sus datos a través de servicios WFS, que fueron descargados en noviembre de 2014 para la realización de este ejercicio de conflación. Las URLs de descarga de los datos originales son:
* http://...
* http://...


Más información en el blog [http://servidor/x.html](http://igac.gov.co)
