#!/usr/bin/python
# -*- coding: utf-8 -*-


from urllib.request import urlopen,Request
from urllib.parse import urlencode
import json

endpoint = "http://data.linkedmdb.org/sparql?"

lista = []
ithopoios = input ('dwste to mikro onoma tou ithopoiou: ')

sparqlq = """
 PREFIX movie: <http://data.linkedmdb.org/resource/movie/>
 PREFIX lmdba: <http://data.linkedmdb.org/resource/actor/>
 PREFIX lmdbf: <http://data.linkedmdb.org/resource/film/>
 PREFIX foaf: <http://xmlns.com/foaf/0.1/>

 SELECT ?actor ?aname WHERE {
  ?actor a movie:actor .
  ?actor movie:actor_name ?aname.
  FILTER (regex(?aname,"^""" + ithopoios + """","i"))
  	
}
"""

# params sent to server
params = { 'query': sparqlq }
# create appropriate param string
paramstr = urlencode(params)

# create GET http request object with params appended
req = Request(endpoint+paramstr)
# request specific content type
req.add_header('Accept','application/sparql-results+json')
# dispatch request
page = urlopen(req)
# get results and close
text = page.read().decode('utf-8')
page.close()

#print text

# convert to json object
jso = json.loads(text)

# iterate over results
for binding in jso['results']['bindings']:
	# for every column in binding
   lista.append ([binding['actor']['value'], binding['aname']['value']])

for i, item in enumerate(lista):
	print (i+1, item[1])

arithmos = int (input ('epilexte ton arithmo tou ithopoiou: ')) -1

sparqlq = """
PREFIX movie: <http://data.linkedmdb.org/resource/movie/>
PREFIX lmdba: <http://data.linkedmdb.org/resource/actor/>
PREFIX lmdbf: <http://data.linkedmdb.org/resource/film/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?actor ?film ?actorname ?moviename WHERE{
?film movie:actor <"""+lista[arithmos][0]+"""> .
?film movie:actor ?actor . 
?film rdfs:label ?moviename .
?actor movie:actor_name ?actorname .
FILTER (?actor != <"""+lista[arithmos][0]+"""> )
}
"""

# params sent to server
params = { 'query': sparqlq }
# create appropriate param string
paramstr = urlencode(params)

# create GET http request object with params appended
req = Request(endpoint+paramstr)
# request specific content type
req.add_header('Accept','application/sparql-results+json')
# dispatch request
page = urlopen(req)
# get results and close
text = page.read().decode('utf-8')
page.close()

#print text

# convert to json object
jso = json.loads(text)

# iterate over results
for binding in jso['results']['bindings']:
	# for every column in binding
	print  (binding['actorname']['value'], binding['moviename']['value'])
