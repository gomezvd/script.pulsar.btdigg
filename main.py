# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'site-packages'))
#librerias = xbmc.translatePath( os.path.join( config.get_runtime_path(), 'resources' ) )
#sys.path.append (librerias)
import json
import base64
import re
import urllib
import urllib2
import xbmc
import time
import xbmcaddon
import unicodedata 

API_KEY = "57983e31fb435df4df77afb854740ea9"
BASE_URL = "http://api.themoviedb.org/3"
IDIOMA = "es"
#pag_esp = "+%26+%28elitetorrent+%7C+divxtotal+%7C+divxatope+%7C+lokotorrent+%7C+newpct+%29"
pag_esp = u'+%26+%40*+%28+elitetorrent+%7C+newpct+%7C+divxatope+%7C+lokotorrent+%7C+castellano+%7C+spanish+%29'
screener = "+%21screener+%21CAM+%21camrip+%21TeleSync+%21TS+%21camlat"
no_ITA = "+%21ITA"
pag_ita = "+%40*+%28+italia+%7C+ITA+%29"
pag_rus = "+%40*+%28+rus+%29"
pag_fra = "+%40*+%28+french+%29"
HEADERS = {
    "Referer": BASE_URL,
}
PAYLOAD = json.loads(base64.b64decode(sys.argv[1]))

addon = xbmcaddon.Addon(id="script.pulsar.bitdgg")

idioma_xml = addon.getSetting("idioma_xml")
IDIOMA = idioma_xml
suf_idioma = ""


use_screener = addon.getSetting("use_screener")

def search(query):
    response = urllib2.urlopen("http://btdigg.org/search?info_hash=&q=%s" % urllib.quote_plus(query))
    data = response.read()
    if response.headers.get("Content-Encoding", "") == "gzip":
        import zlib
        data = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(data)
    return [{"uri": magnet} for magnet in re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data)]

def search_episode(imdb_id, tvdb_id, name, season, episode):
 #   xbmc.log('Victor: imdb: %s, tvdb: %s ' % (imdb_id,tvdb_id) , xbmc.LOGDEBUG)
    inicio_proceso = time.time()
    url_pelicula = "http://api.themoviedb.org/3/find/%s?api_key=57983e31fb435df4df77afb854740ea9&language=%s&external_source=imdb_id" % (imdb_id, IDIOMA)
 #   xbmc.log('Victor: %s' % url_pelicula, xbmc.LOGDEBUG)
    pelicula = urllib2.urlopen(url_pelicula)

    texto1 = json.loads(pelicula.read())
 #   xbmc.log('Victor: %s' % texto1.keys(), xbmc.LOGDEBUG)
    texto2 = texto1['tv_results']
    texto3 = texto2[0]

    nombre = texto3.get("name")
    if nombre == "24" and season == 9 and IDIOMA == 'es':
                 nombre = u"24 vive otro dia"
                 season = 1
    fin_proceso = time.time()
    tiempo_total = fin_proceso - inicio_proceso
    xbmc.log(' Victor Tiempo busqueda nombre espanol: %s' % tiempo_total, xbmc.LOGDEBUG)
 
    nombre = nombre.replace(u'á', "a")
    nombre = nombre.replace(u'é', "e")
    nombre = nombre.replace(u'í', "i")
    nombre = nombre.replace(u'ó', "o")
    nombre = nombre.replace(u'ú', "u")
    nombre = nombre.replace(":", " ")
 #   nombre = nombre.replace(" ", "+")
    temporada = "" 
    pag_bus = ""
    suf_idioma = ""
    if IDIOMA =='ru':
       suf_idioma = "+rus"
    if IDIOMA == 'it':
        suf_idioma = "+%28+ITA+%7C+italia+%29" 
    
    if nombre.lower() <> name.lower():
        nombre2 = '"' + name + '"' + suf_idioma
        nombre = '%40name+' + '%28+"' + nombre + '"+%7c+' + nombre2 + '+%29' 
  #      nombre =  '%28+"' + nombre + '"+%7c+' + nombre2 + '+%29'    
    else:    
        nombre = '%40name+"' + name + '"' + suf_idioma    
#    xbmc.log('Victor: %s %s%dX%02d%s%d%02d %s' % (nombre, "+%26+%28+",season, episode, "+%7c+", season, episode, pag_bus), xbmc.LOGDEBUG)
    busqueda = "%s %s%dX%02d%s%d%02d%s" % (nombre, "+%28+",season, episode, "+%7c+", season, episode, "+%29")
    busqueda = busqueda.replace(" ", "+")
    if IDIOMA == 'es':
            busqueda = busqueda + no_ITA

    xbmc.log('Victor: %s' % busqueda.encode('utf-8'), xbmc.LOGDEBUG)
    prue = urllib2.urlopen("http://btdigg.org/search?info_hash=&q=" + busqueda.encode('utf-8'))
    data_1 = prue.read()
    fin_proceso2 = time.time()
    tiempo_total = fin_proceso2 - fin_proceso
    xbmc.log(' Victor Tiempo busqueda inicial: %s' % tiempo_total, xbmc.LOGDEBUG)
    if "did not match any documents" in data_1:
             xbmc.log('Victor: no encuentra nada' , xbmc.LOGDEBUG)
             busqueda = ""
             nombre2 = '%40name+"' + name + '"' + suf_idioma
    #         nombre2 = '"' + name + '"' + suf_idioma 
             busqueda2 = "%s S%02dE%02d" % (nombre2, season, episode)
             busqueda2 = busqueda2.replace(" ", "+")
 #            xbmc.log('Victor: %s' %busqueda, xbmc.LOGDEBUG)
             prue2 = urllib2.urlopen("http://btdigg.org/search?info_hash=&q=" + busqueda.encode('utf-8'))
             data_1 = prue2.read()
             fin_proceso3 = time.time()
             tiempo_total = fin_proceso3 - inicio_proceso
             xbmc.log(' Victor Tiempo busqueda total: %s' % tiempo_total, xbmc.LOGDEBUG)
    if prue.headers.get("Content-Encoding", "") == "gzip":
        import zlib
        data = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(data_1)
    return [{"uri": magnet} for magnet in re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data_1)]
 

def search_movie(imdb_id, name, year):
 #   xbmc.log('Victor name: %s' % name, xbmc.LOGDEBUG)
    url_pelicula = "http://api.themoviedb.org/3/find/%s?api_key=57983e31fb435df4df77afb854740ea9&language=%s&external_source=imdb_id" % (imdb_id, IDIOMA)
 #   xbmc.log('Victor: %s' % url_pelicula, xbmc.LOGDEBUG)
    pelicula = urllib2.urlopen(url_pelicula)
    texto1 = json.loads(pelicula.read())
    texto2 = texto1['movie_results']
    texto3 = texto2[0]
    nombre = texto3.get("title")
    nombre = nombre.replace(u'á', "a")
    nombre = nombre.replace(u'é', "e")
    nombre = nombre.replace(u'í', "i")
    nombre = nombre.replace(u'ó', "o")
    nombre = nombre.replace(u'ú', "u")

 #   xbmc.log('Victor nombre: %s' % nombre, xbmc.LOGDEBUG)
 #   xbmc.log('Victor name: %s' % name, xbmc.LOGDEBUG)
    var_1 = "%s" % name
    var_2 = "%s" % nombre
    if var_1 == var_2: 
        if IDIOMA == 'es':
            nombre = nombre + pag_esp
        if IDIOMA == 'it':
            nombre = nombre + pag_ita
        if IDIOMA == 'ru':
            nombre = nombre + pag_rus       
    nombre = nombre.replace(":", " ")
    nombre = nombre.replace(" ", "+")         
    nombre = "%28%40name+" + nombre + "%29" 
 #   nombre = "%28+" + nombre + "%29"  
    if use_screener:
        nombre = nombre + screener
    xbmc.log('Victor: %s' % nombre.encode('utf-8'), xbmc.LOGDEBUG)     
    response = urllib2.urlopen("http://btdigg.org/search?info_hash=&q=" + nombre.encode('utf-8'))
    data = response.read()
 #   xbmc.log('Victor: %s' % data, xbmc.LOGDEBUG)
    if "did not match any documents" in data:
             xbmc.log('Victor: no encuentra nada' , xbmc.LOGDEBUG)
             busqueda = ""
   #          nombre = "%40name+" + name 
             nombre = name 
             nombre = nombre.replace(" ", "+") 

             prue2 = urllib2.urlopen("http://btdigg.org/search?info_hash=&q=" + nombre.encode('utf-8'))
             data = prue2.read()
    elif '<td class="selected"><a href="/search?q' in data:    
             response = urllib2.urlopen("http://btdigg.org/search?info_hash=&q=" + nombre.encode('utf-8') + "&p=1")
             data2 = response.read()   
             data = data + data2  

    if response.headers.get("Content-Encoding", "") == "gzip":
        import zlib
        data = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(data)
    return [{"uri": magnet} for magnet in re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data)]

urllib2.urlopen(
    PAYLOAD["callback_url"],
    data=json.dumps(globals()[PAYLOAD["method"]](*PAYLOAD["args"]))
)
