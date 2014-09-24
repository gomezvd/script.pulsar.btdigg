import sys
import json
import base64
import re
import urllib
import urllib2
import xbmc
import xbmcaddon
import unicodedata 
API_KEY = "57983e31fb435df4df77afb854740ea9"
BASE_URL = "http://api.themoviedb.org/3"
IDIOMA = "es"
#pag_esp = "+%26+%28elitetorrent+%7C+divxtotal+%7C+divxatope+%7C+lokotorrent+%7C+newpct+%29"
pag_esp = "+%40content+%28elitetorrent+%7C+newpct+%29"
HEADERS = {
    "Referer": BASE_URL,
}
PAYLOAD = json.loads(base64.b64decode(sys.argv[1]))
__addon__ = xbmcaddon.Addon(str(sys.argv[0]))
addon_dir = xbmc.translatePath(__addon__.getAddonInfo('path'))
#sys.path.append(os.path.join(addon_dir, 'resources', 'lib' ))
idioma_xml = __addon__.getSetting("idioma_xml")
IDIOMA = idioma_xml
def search(query):
    response = urllib2.urlopen("http://btdigg.org/search?info_hash=&q=%s" % urllib.quote_plus(query))
    data = response.read()
    if response.headers.get("Content-Encoding", "") == "gzip":
        import zlib
        data = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(data)
    return [{"uri": magnet} for magnet in re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data)]

def search_episode(imdb_id, tvdb_id, name, season, episode):
    xbmc.log('Victor: imdb: %s, tvdb: %s ' % (imdb_id,tvdb_id) , xbmc.LOGDEBUG)
    url_pelicula = "http://api.themoviedb.org/3/find/%s?api_key=57983e31fb435df4df77afb854740ea9&language=%s&external_source=imdb_id" % (imdb_id, IDIOMA)
 #   xbmc.log('Victor: %s' % url_pelicula, xbmc.LOGDEBUG)
    pelicula = urllib2.urlopen(url_pelicula)
    texto = pelicula.read()
    texto = texto.replace("'", "\"")
    texto1 = json.loads(texto)
 #   xbmc.log('Victor: %s' % texto1.keys(), xbmc.LOGDEBUG)
    texto2 = texto1['tv_results']
    texto3 = texto2[0]
#    xbmc.log('Victor: %s' % texto3, xbmc.LOGDEBUG)

    
#    xbmc.log('Victor: %s' % texto3.keys(), xbmc.LOGDEBUG)
    nombre = texto3.get("name")
    nombre = elimina_tildes(nombre)
    nombre = nombre.replace(":", " ")
 #   nombre = nombre.replace(" ", "+")
    temporada = "" 
    pag_bus = ""
    if IDIOMA == 'es':
 #           nombre = nombre + pag_esp
            pag_bus = pag_esp
            temporada = "temporada"
    nombre = "%40name+" + nombre         
#    xbmc.log('Victor: %s %s%dX%02d%s%d%02d %s' % (nombre, "+%26+%28+",season, episode, "+%7c+", season, episode, pag_bus), xbmc.LOGDEBUG)
    return search('"%s" %s%dX%02d%s%d%02d %s' % (nombre, "+%26+%28+",season, episode, "+%7c+", season, episode, pag_bus))

def elimina_tildes(s): 
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')) 

def search_movie(imdb_id, name, year):
    url_pelicula = "http://api.themoviedb.org/3/find/%s?api_key=57983e31fb435df4df77afb854740ea9&language=%s&external_source=imdb_id" % (imdb_id, IDIOMA)
 #   xbmc.log('Victor: %s' % url_pelicula, xbmc.LOGDEBUG)
    pelicula = urllib2.urlopen(url_pelicula)
    texto = pelicula.read()
    texto = texto.replace("'", "\"")
    texto1 = json.loads(texto)
 #   xbmc.log('Victor: %s' % texto1.keys(), xbmc.LOGDEBUG)
    texto2 = texto1['movie_results']
    texto3 = texto2[0]
 #   xbmc.log('Victor: %s' % texto3, xbmc.LOGDEBUG)

    
 #   xbmc.log('Victor: %s' % texto3.keys(), xbmc.LOGDEBUG)
    nombre = texto3.get("title")
    nombre = elimina_tildes(nombre)
    nombre = nombre.replace(":", " ")
    nombre = nombre.replace(" ", "+")
 #   xbmc.log('Victor: %s' % nombre, xbmc.LOGDEBUG)
    if nombre == name:
        if IDIOMA == 'es':
            nombre = nombre + pag_esp
    nombre = "%40name+" + nombre        
    response = urllib2.urlopen("http://btdigg.org/search?info_hash=&q=" + nombre)
    data = response.read()
    if response.headers.get("Content-Encoding", "") == "gzip":
        import zlib
        data = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(data)
    return [{"uri": magnet} for magnet in re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data)]

urllib2.urlopen(
    PAYLOAD["callback_url"],
    data=json.dumps(globals()[PAYLOAD["method"]](*PAYLOAD["args"]))
)


