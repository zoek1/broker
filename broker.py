#!/usr/bin/python2

from sessions.open_refine import  get_session, new_session

from flask import Flask, request, redirect
from urllib import urlencode, quote
from urlparse import urlparse

import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/")
def root():
    resource = request.args.get("resource", "") 
    
    ip = request.remote_addr
    logger.info("Verificando sesion activa a %s" % ip)
    active_session = get_session(ip)

    if not active_session:
        logger.info("Adquiriendo nueva sesion")
        active_session = new_session(ip)

    # Add resource parameter to existing query
    if resource != "":
      query = request.args.copy()
      
      for key, value in query.items():
        if key != "resource":
          query["resource"] += "&" + key + "=" + value
          del query[key]

      logger.info("Estableciendo query string")
      active_session = active_session + "?" + urlencode(query)

    logger.info("Redirijiendo")
    return redirect(active_session)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
