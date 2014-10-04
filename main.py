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
import xbmcgui
import time
import xbmcaddon
import unicodedata 

API_KEY = "57983e31fb435df4df77afb854740ea9"
BASE_URL = "http://api.themoviedb.org/3"
pag_esp = u'+%26+%40name+%28+elitetorrent+%7C+newpct+%7C+divxatope+%7C+lokotorrent+%7C+castellano+%7C+spanish+%7C+esp+%29'
screener = "+%21screener+%21CAM+%21Cam+%21camrip+%21TeleSync+%21TS+%21camlat"
sin_3d = "+%213D"
no_ITA = "+%21ITA"
alta_definicion = "+%28+720p+%7C+1080p+%7C+720+%7C+1080+%7C+microhd+%29"
pag_ita = "+%40name+%28+italia+%7C+ITA+%29"
pag_rus = "+%40name+%28+rus+%29"
pag_fra = "+%40name+%28+french+%29"
HEADERS = {
    "Referer": BASE_URL,
}
PAYLOAD = json.loads(base64.b64decode(sys.argv[1]))

addon = xbmcaddon.Addon(id="script.pulsar.bitdgg")
use_screener = addon.getSetting("use_screener")
use_3D = addon.getSetting("use_3D")
only_HD = addon.getSetting("only_HD")
idioma_xml = addon.getSetting("idioma_xml")
IDIOMA = idioma_xml
suf_idioma = ""
data = []



def search(nombre):
    # cambiamos a la busquedada con la API
    inicio_proceso = time.time()
    u = urllib2.urlopen('http://api.btdigg.org/api/public-8e9a50f8335b964f/s01?q=' + nombre.encode('utf-8') )
    
    try:
       for line in u:
         if line.startswith('#'):
             continue
         info_hash, name, files, size, dl, seen = line.strip().split('\t')[:6]
         res = dict(uri = 'magnet:?xt=urn:btih:%s' % (info_hash,) + '&amp;dn=' + '%s' % name.translate(None, '|') )

         data.append(res)
    #     xbmc.log(' Victor prueba: %s' % res, xbmc.LOGDEBUG)
    except urllib2.HTTPError as error_code:
            xbmc.log(' Victor error %s' % error_code, xbmc.LOGDEBUG)
    finally:
            u.close()
    fin_proceso = time.time()
    tiempo_total = fin_proceso - inicio_proceso
    xbmc.log(' Victor Tiempo busqueda api: %s' % tiempo_total, xbmc.LOGDEBUG)
    xbmc.log(' Victor prueba: %s' % data, xbmc.LOGDEBUG) 
    if data == []: 
       __addonname__   = addon.getAddonInfo('name')
       line1 = "No se encuentran torrents con la calidad e idioma especificados"
       xbmcgui.Dialog().ok(__addonname__, line1)
       
  #
  #   Busqueda de episodios  puede ser necesario buscar las series en tvdb en otra version
  #
  
def search_episode(imdb_id, tvdb_id, name, season, episode):
 
  # Busqueda de titulo en idioma de audio ------------------------ 
    if IDIOMA <> 'en':
         inicio_proceso = time.time()
         url_pelicula = "http://api.themoviedb.org/3/find/%s?api_key=57983e31fb435df4df77afb854740ea9&language=%s&external_source=imdb_id" % (imdb_id, IDIOMA)
         pelicula = urllib2.urlopen(url_pelicula)

         texto1 = json.loads(pelicula.read())
         texto2 = texto1['tv_results']
         texto3 = texto2[0]

         nombre = texto3.get("name")

  # -------------------------------------------------------------   
  #  Excepcion en español ----------------
         if nombre == "24" and season == 9 and IDIOMA == 'es':
                 nombre = u"24 vive otro dia"
                 season = 1
  # --------------------------------------              
         fin_proceso = time.time()
         tiempo_total = fin_proceso - inicio_proceso
         xbmc.log(' Victor Tiempo busqueda nombre espanol: %s' % tiempo_total, xbmc.LOGDEBUG)
 
         nombre = nombre.replace(u'á', "a")
         nombre = nombre.replace(u'é', "e")
         nombre = nombre.replace(u'í', "i")
         nombre = nombre.replace(u'ó', "o")
         nombre = nombre.replace(u'ú', "u")
    else:
         nombre = name       
            
    nombre = nombre.replace(":", " ")

    temporada = "" 
    pag_bus = ""
    suf_idioma = ""
    if IDIOMA == 'es':
            suf_idioma = pag_esp
    elif IDIOMA == 'it':
            suf_idioma = pag_ita
    elif IDIOMA == 'ru':
            suf_idioma = pag_rus 
    elif IDIOMA == 'fr':
            suf_idioma = pag_fra 
    
    if nombre.lower() <> name.lower():
        nombre2 = '"' + name + '"' + suf_idioma
        nombre = '%40name+' + '%28+"' + nombre + '"+%7c+' + nombre2 + '+%29' 
   
    else:    
        nombre = '%40name+"' + name + '"' + suf_idioma    

    busqueda = "%s %s%dX%02d%s%d%02d%sS%02dE%02d%s" % (nombre, "+%28+",season, episode, "+%7c+", season, episode, "+%7c+", season, episode, "+%29")
    busqueda = busqueda.replace(" ", "+")
    if IDIOMA == 'es':
            busqueda = busqueda + no_ITA

    xbmc.log('Victor: %s' % busqueda.encode('utf-8'), xbmc.LOGDEBUG)
    search(busqueda)
 
    
 
    return data
       
  #
  #   Busqueda de peliculas
  #
  
def search_movie(imdb_id, name, year):
  ### Pendiente de revisar porque necesito poner como local IDIOMA
    addon = xbmcaddon.Addon(id="script.pulsar.bitdgg")
    use_screener = addon.getSetting("use_screener")
    use_3D = addon.getSetting("use_3D")
    only_HD = addon.getSetting("only_HD")
    idioma_xml = addon.getSetting("idioma_xml")
    IDIOMA = idioma_xml 
  ###-------------------------------------------------------------
  
  # Busqueda de titulo en idioma de audio ------------------------ 
    if IDIOMA <> 'en':
      inicio_proceso = time.time()
      url_pelicula = "http://api.themoviedb.org/3/find/%s?api_key=57983e31fb435df4df77afb854740ea9&language=%s&external_source=imdb_id" % (imdb_id, IDIOMA)

      pelicula = urllib2.urlopen(url_pelicula)
      texto1 = json.loads(pelicula.read())
      fin_proceso = time.time()
      tiempo_total = fin_proceso - inicio_proceso
      xbmc.log(' Victor Tiempo busqueda nombre espanol: %s' % tiempo_total, xbmc.LOGDEBUG)

      
      texto2 = texto1['movie_results']
      texto3 = texto2[0]
      nombre = texto3.get("title")
      nombre = nombre.replace(u'á', "a")
      nombre = nombre.replace(u'é', "e")
      nombre = nombre.replace(u'í', "i")
      nombre = nombre.replace(u'ó', "o")
      nombre = nombre.replace(u'ú', "u")
    else:
      nombre = name  
  # -------------------------------------------------------------
    var_1 = "%s" % name
    var_2 = "%s" % nombre
    suf_idioma = ""
    if var_1 == var_2: 
          if IDIOMA == 'es':
            nombre = nombre + pag_esp
          if IDIOMA == 'it':
            nombre = nombre + pag_ita
          if IDIOMA == 'ru':
            nombre = nombre + pag_rus       
    if IDIOMA == 'es':
            suf_idioma = pag_esp
    elif IDIOMA == 'it':
            suf_idioma = pag_ita
    elif IDIOMA == 'ru':
            suf_idioma = pag_rus 
    elif IDIOMA == 'fr':
            suf_idioma = pag_fra         
    nombre2 = '%28"' + name + '"' + suf_idioma + '+%29'
    nombre = '%28%40name+' + '%28+"' + nombre + '"+%7c+' + nombre2 + '+%29' + "%29" 
    nombre = nombre.replace(":", " ")
    nombre = nombre.replace(" ", "+")   
    if only_HD == "true": 
             nombre = nombre + alta_definicion 
    else: 
        if use_screener == "true": 
          nombre = nombre + screener
          
    if use_3D == "true": 
         xbmc.log(' Victor Con 3D', xbmc.LOGDEBUG)   
    else:     
         nombre = nombre + sin_3d
         
    xbmc.log('Victor: %s' % nombre.encode('utf-8'), xbmc.LOGDEBUG)     
    
    search(nombre) 

 
    return data
 
urllib2.urlopen(
    PAYLOAD["callback_url"],
    data=json.dumps(globals()[PAYLOAD["method"]](*PAYLOAD["args"]))
)
