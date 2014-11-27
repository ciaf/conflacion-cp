# -*- encoding:utf8 -*-

## Conflación Centros Poblados Centroides DANE - administrativo_punto IGAC
## Copyright (C) 2014 Germán Carrillo para el CIAF - IGAC
## E-mail:           geotux_tuxman@linuxmail.org 

## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program. If not, see <http://www.gnu.org/licenses>

import fiona, nltk, re
from unidecode import unidecode

# Abrir archivos de datos geográficos
prefix = '/docs/downloads/conflacion/'
adm_ptos = fiona.open(prefix+'derivados/carto_adm_pto_coddane_filtro.shp')
cpcs = fiona.open(prefix+'divipola_cpc.shp')
mpios = fiona.open(prefix+'divipola_mpio.shp')

# Variables a emplear en el script
tipos={'8305':'Cas','8307':'C','8323':'IP', '9999':'Otros'}
dane_non_match = {}
found = False
contador = 0

# Crear/Sobreescribir listados
file_conc = open(prefix+'listados/concuerdan.csv', 'w')
file_no_conc_dane = open(prefix+'listados/no_concuerdan_dane.csv', 'w')
file_simi = open(prefix+'listados/similares.csv', 'w')

# Encabezado de los listados
file_conc.write( ';'.join( [ 'cod_dane', 'nombre_dane', 'tipo_dane', 'nombre_carto', 'tipo_igac', 'pk_cue', 'lon', 'lat' ] ) )
file_no_conc_dane.write( ';'.join( ['cod_dane_mpio', 'nombre_dane' ] ) )
file_simi.write( ';'.join( ['cod_dane_mpio', 'nombre_dane', 'nombre_carto' ] ) )

# Funciones para Semejanza
def normalizar_basico( term ):
    # Remover tildes, volver todo a minúsculas
    return unidecode(term).lower()
    
def fuzzy_match( t1, t2, max_dist=2 ):
    return nltk.metrics.edit_distance( normalizar_basico(t1), normalizar_basico(t2) ) <= max_dist

def normalizar( term ):
    normalizado = normalizar_basico( term )
    r1 = re.compile('^caserio\s')
    r2 = re.compile('\s{2,}')  
    r3 = re.compile('^(la|el|los|las)\s')
    r4 = re.compile('\s*(\(|\)|-)\s*')  
    r5 = re.compile('\s{1,}')
    res = r5.sub('',r4.sub(' ',r3.sub(' ',r2.sub(' ',r1.sub('', normalizado ))))).strip() 
    variaciones = [ res ]
    sinonimos = [ ['kilometro','km'], ['veinte','20'] ]
    for sin in sinonimos:
        if sin[0] in res:
            variaciones.append( res.replace( sin[0], sin[1] ) )
    return variaciones

def extraer_ngrams( term ):
    stopwords = [ 'la', 'el', 'de', 'del', 'los', 'las', 'en', 'y', 'o', 'a', '-', 'san', 'puerto', 'santa', 'alto' ]
    tokens = nltk.word_tokenize( term.strip() )
    res = []
    for n in range( len(tokens), 1, -1 ):
        res.extend( [x for x in nltk.ngrams( tokens, n )] )
    res.extend( [tuple([t]) for t in tokens if not t.lower() in stopwords] )
    return [' '.join(t) for t in res]

def partial_contains( term1, term2 ):
    for t1 in extraer_ngrams( term1 ):
        for t2 in extraer_ngrams( term2 ):
            if len(t1) == 1 or len(t2) == 1: 
                # No comparar si el token es solo un caracter (ej. C, tomado de TOMÁS C MOSQUERA)
                continue
            nt1 = normalizar_basico( t1 )
            nt2 = normalizar_basico( t2 )
            if nt1 in nt2:
                if nt1 in nt2.split(' '): # Solo palabras completas contenidas en nt2 (ej. descartar ana-la planada)
                    return True
    return False

def determinar_semejanzas( dict1, dict2 ):
    fuzzy = []
    contains = []
    res = []
    for key1, term1 in dict1.iteritems():
        for key2, term2 in dict2.iteritems():
            if fuzzy_match( term1, term2 ):
                fuzzy.append( [key1, term1, key2, term2] )
            else:
                if partial_contains( term1, term2 ):
                    contains.append( [key1, term1, key2, term2] )
        if len( fuzzy ):
            res.extend( [ f for f in fuzzy ] )
            fuzzy = []
            contains = []
        else: # Solo si no hay fuzzy matches, devolver partial_contains
            if len( contains ):
                res.extend( [ c for c in contains ] )
                fuzzy = []
                contains = []
    return res

for mpio in mpios:
    contador += 1
    print contador
    #if mpio["properties"]["CODIGO_DPT"][:2] == '52': # Filtro por departamento
    #if mpio["properties"]["CODIGO_DPT"] == '91540': # Filtro por municipio
    for cpc in cpcs:
        if cpc["properties"]["CODIGO_DPT"] == mpio["properties"]["CODIGO_DPT"]:
            # Mpio y CP concuerdan 
            found = False
            for adm_pto in adm_ptos:                   
                if adm_pto["properties"]["cod_dane"] == mpio["properties"]["CODIGO_DPT"]:
                    # Mpio y adm_pto concuerdan
                    if adm_pto["properties"]["nombre_geo"]: 
                        # Solo considerar registros de adm_pto con nombre
                        if set( normalizar( cpc["properties"]["NOMBRE_CEN"] ) ).intersection( normalizar( adm_pto["properties"]["nombre_geo"] ) ):
                            file_conc.write( '\n'+';'.join([ cpc["properties"]["CODIGO_CEN"], \
                                cpc["properties"]["NOMBRE_CEN"], cpc["properties"]["CODIGO_TIP"], \
                                adm_pto["properties"]["nombre_geo"], \
                                tipos[adm_pto["properties"]["codigo_nom"]] if adm_pto["properties"]["codigo_nom"] in tipos else '', \
                                str(int(adm_pto["properties"]["pk_cue"])), str(adm_pto['geometry']['coordinates'][0][0]), \
                                str(adm_pto['geometry']['coordinates'][0][1]) ]).encode('utf-8') )
                            found = True
                        else:
                            # Agregar llave-valor a carto_non_match
                            pk_cue = str(int(adm_pto["properties"]["pk_cue"]))
                            key = pk_cue if len( pk_cue ) else adm_pto["properties"]["nombre_geo"]
                            if not carto_non_match.has_key(key): carto_non_match[key] = adm_pto["properties"]["nombre_geo"] 
            if not found: 
                # Agregar llave-valor a dane_non_match
                key = cpc["properties"]["CODIGO_CEN"]
                if not dane_non_match.has_key(key) : dane_non_match[key] = cpc["properties"]["NOMBRE_CEN"]
    #print "No concuerdan:", ', '.join(dane_non_match)," --> (", ', '.join(carto_non_match),")"
    for nm in dane_non_match.itervalues():
        file_no_conc_dane.write( ('\n' + mpio["properties"]["CODIGO_DPT"] + ';' + nm).encode('utf-8') ) 
    semejantes = determinar_semejanzas( dane_non_match, carto_non_match )
    for semejante in semejantes:
        file_simi.write( ('\n' + mpio["properties"]["CODIGO_DPT"] + ';' + ';'.join(semejante) ).encode('utf-8') )              
    dane_non_match = {}
    carto_non_match = {}

# Cerrar archivos de listados
file_conc.close()
file_no_conc_dane.close()
file_simi.close()

# Cerrar capas
mpios.close()
cpcs.close()
adm_ptos.close()

