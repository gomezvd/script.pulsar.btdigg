# -*- coding: utf-8 -*-
import sys
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
pag_esp = u"+%40content+%28+elitetorrent+%7C+newpct+%7C+divxatope+%7C+lokotorrent+%7C+castellano+%7C+spanish+%7C+espa%F1ol+%29"
screener = "+%40name+%21screener+%21CAM+%21camrip+%21TeleSync+%21TS+%21camlat"
no_ITA = "+%21ITA"
pag_ita = "+%40content+%28+italia+%7C+ITA+%29"
HEADERS = {
    "Referer": BASE_URL,
}
PAYLOAD = json.loads(base64.b64decode(sys.argv[1]))
__addon__ = xbmcaddon.Addon(str(sys.argv[0]))
addon_dir = xbmc.translatePath(__addon__.getAddonInfo('path'))
#sys.path.append(os.path.join(addon_dir, 'resources', 'lib' ))
idioma_xml = __addon__.getSetting("idioma_xml")
use_screener = __addon__.getSetting("use_screener")
IDIOMA = idioma_xml
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
 #   xbmc.log('Victor: %s' % pelicula.read() , xbmc.LOGDEBUG)
 #   texto = pelicula.read()
 #   texto = texto.replace("'s", "")
 #   texto = elimina_tildes(texto)
 #   xbmc.log('Victor: %s' % texto , xbmc.LOGDEBUG)
 #   texto1 = json.loads(texto)
    texto1 = json.loads(pelicula.read())
 #   xbmc.log('Victor: %s' % texto1.keys(), xbmc.LOGDEBUG)
    texto2 = texto1['tv_results']
    texto3 = texto2[0]

#    xbmc.log('Victor: %s' % texto3, xbmc.LOGDEBUG)

    
#    xbmc.log('Victor: %s' % texto3.keys(), xbmc.LOGDEBUG)
    nombre = texto3.get("name")
    if nombre == "24" and season == 9 and IDIOMA == 'es':
                 nombre = u"24 vive otro dia"
                 season = 1
    fin_proceso = time.time()
    tiempo_total = fin_proceso - inicio_proceso
    xbmc.log(' Victor Tiempo busqueda nombre espanol: %s' % tiempo_total, xbmc.LOGDEBUG)
    nombre = elimina_tildes(nombre)
    nombre = nombre.replace(":", " ")
 #   nombre = nombre.replace(" ", "+")
    temporada = "" 
    pag_bus = ""
    
    nombre = "%40name+" + nombre         
#    xbmc.log('Victor: %s %s%dX%02d%s%d%02d %s' % (nombre, "+%26+%28+",season, episode, "+%7c+", season, episode, pag_bus), xbmc.LOGDEBUG)
    busqueda = "%s %s%dX%02d%s%d%02d%s" % (nombre, "+%28",season, episode, "+%7c+", season, episode, "+%29")
    busqueda = busqueda.replace(" ", "+")
    if IDIOMA == 'es':
            busqueda = busqueda + no_ITA

 #   xbmc.log('Victor: %s' %busqueda, xbmc.LOGDEBUG)
    prue = urllib2.urlopen("http://btdigg.org/search?info_hash=&q=" + busqueda)
    data_1 = prue.read()
    fin_proceso2 = time.time()
    tiempo_total = fin_proceso2 - fin_proceso
    xbmc.log(' Victor Tiempo busqueda inicial: %s' % tiempo_total, xbmc.LOGDEBUG)
    if "did not match any documents" in data_1:
             xbmc.log('Victor: no encuentra nada' , xbmc.LOGDEBUG)
             busqueda = ""
             nombre = "%40name+" + name 
             busqueda = "%s %s%dX%02d%s%d%02d%s" % (nombre, "+%28",season, episode, "+%7c+", season, episode, "+%29")
             busqueda = busqueda.replace(" ", "+")
 #            xbmc.log('Victor: %s' %busqueda, xbmc.LOGDEBUG)
             prue2 = urllib2.urlopen("http://btdigg.org/search?info_hash=&q=" + busqueda)
             data_1 = prue2.read()
             fin_proceso3 = time.time()
             tiempo_total = fin_proceso3 - inicio_proceso
             xbmc.log(' Victor Tiempo busqueda total: %s' % tiempo_total, xbmc.LOGDEBUG)
    if prue.headers.get("Content-Encoding", "") == "gzip":
        import zlib
        data = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(data_1)
    return [{"uri": magnet} for magnet in re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data_1)]

def elimina_tildes(s): 
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')) 

def search_movie(imdb_id, name, year):
 #   xbmc.log('Victor name: %s' % name, xbmc.LOGDEBUG)
    url_pelicula = "http://api.themoviedb.org/3/find/%s?api_key=57983e31fb435df4df77afb854740ea9&language=%s&external_source=imdb_id" % (imdb_id, IDIOMA)
 #   xbmc.log('Victor: %s' % url_pelicula, xbmc.LOGDEBUG)
    pelicula = urllib2.urlopen(url_pelicula)
    texto1 = json.loads(pelicula.read())
    texto2 = texto1['movie_results']
    texto3 = texto2[0]
    nombre = texto3.get("title")
    nombre = elimina_tildes(nombre)

 #   xbmc.log('Victor nombre: %s' % nombre, xbmc.LOGDEBUG)
 #   xbmc.log('Victor name: %s' % name, xbmc.LOGDEBUG)
    var_1 = "%s" % name
    var_2 = "%s" % nombre
    if var_1 == var_2: 
        if IDIOMA == 'es':
            nombre = nombre + pag_esp
        if IDIOMA == 'it':
            nombre = nombre + pag_ita   
    nombre = nombre.replace(":", " ")
    nombre = nombre.replace(" ", "+")         
    nombre = "%40name+" + nombre   
    if use_screener:
        nombre = nombre + screener
    xbmc.log('Victor: %s' % nombre, xbmc.LOGDEBUG)     
    response = urllib2.urlopen("http://btdigg.org/search?info_hash=&q=" + nombre)
    data = response.read()
 #   xbmc.log('Victor: %s' % data, xbmc.LOGDEBUG)
    if "did not match any documents" in data:
             xbmc.log('Victor: no encuentra nada' , xbmc.LOGDEBUG)
             busqueda = ""
             nombre = "%40name+" + name 
             nombre = nombre.replace(" ", "+") 

             prue2 = urllib2.urlopen("http://btdigg.org/search?info_hash=&q=" + nombre)
             data = prue2.read()

    if response.headers.get("Content-Encoding", "") == "gzip":
        import zlib
        data = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(data)
    return [{"uri": magnet} for magnet in re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data)]

urllib2.urlopen(
    PAYLOAD["callback_url"],
    data=json.dumps(globals()[PAYLOAD["method"]](*PAYLOAD["args"]))
)
