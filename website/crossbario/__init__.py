###############################################################################
##
##  Copyright 2013 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

import uuid
import os

import mimetypes

mimetypes.add_type('image/svg+xml', '.svg')
mimetypes.add_type('text/javascript', '.jgz')


from optparse import OptionParser

from flask import Flask, Request, request, session, g, url_for, \
     abort, render_template, flash

from flask_flatpages import FlatPages


app = Flask(__name__)
app.secret_key = str(uuid.uuid4())

app.config['FLATPAGES_AUTO_RELOAD'] = True
app.config['FLATPAGES_EXTENSION'] = '.md'
app.config['FLATPAGES_ROOT'] = '../wiki'

pages = FlatPages(app)


## generate Pygments CSS file for style:
## pygmentize -S default -f html > pygments.css
##

import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import json

class DocPageRenderer(mistune.Renderer):

   def block_code(self, code, lang):
      print "CODE", lang, len(code)

      lexer = None
      if lang:
         try:
            lexer = get_lexer_by_name(lang, stripall = True)
         except:
            print("failed to load lexer for language '{}'".format(lang))

      if not lexer:
         return "\n<pre><code>{}</code></pre>\n".format(mistune.escape(code))

      formatter = HtmlFormatter()
      return highlight(code, lexer, formatter)


renderer = DocPageRenderer()
app_md = mistune.Markdown(renderer = renderer)


## load Sphinx documentation inventory
##
# from sphinx.ext.intersphinx import read_inventory_v2
# from posixpath import join

# f = open("./_build/html/objects.inv", "rb")
# f.readline()
# res = read_inventory_v2(f, "http://example.com", join)


@app.before_request
def before_request():
   session["widgeturl"] = app.widgeturl

@app.route('/')
def page_home():
   session['tab_selected'] = 'page_home'
   return render_template('index.html')

## generic template for all doc pages
##
@app.route('/doc/<path:path>/')
def page_doc(path):
   page = pages.get_or_404(path)
   return render_template('page_t_doc_page.html', page = page)

@app.route('/doc2/<path:path>/')
def page_doc2(path):
   fn = os.path.abspath(os.path.join(app.config['FLATPAGES_ROOT'], "{}.md".format(path)))
   title = path.replace('-', ' ')
   print fn, title
   with open(fn, 'r') as f:
      source = f.read()
      contents = app_md.render(source)
      return render_template('page_t_doc_page2.html', contents = contents, title = title)


@app.route('/howitworks/')
def page_howitworks():
   session['tab_selected'] = 'page_howitworks'
   return render_template('page_t_howitworks.html')

@app.route('/gettingstarted/')
def page_gettingstarted():
   session['tab_selected'] = 'page_gettingstarted'
   return render_template('page_t_gettingstarted.html')

@app.route('/features/')
def page_features():
   session['tab_selected'] = 'page_features'
   return render_template('page_t_features.html')

@app.route('/roadmap/')
def page_roadmap():
   session['tab_selected'] = 'page_roadmap'
   return render_template('page_t_roadmap.html')

@app.route('/faq/')
def page_faq():
   session['tab_selected'] = 'page_faq'
   return render_template('page_t_faq.html')

@app.route('/reference/')
def page_reference():
   session['tab_selected'] = 'page_reference'
   return render_template('page_t_reference.html')

@app.route('/impressum/')
def page_impressum():
   session['tab_selected'] = 'page_impressum'
   return render_template('page_t_impressum.html')

@app.route('/contribute/')
def page_contribute():
   session['tab_selected'] = 'page_faq'
   return render_template('page_t_contribute.html')


if __name__ == "__main__":

   parser = OptionParser ()

   parser.add_option ("-d",
                      "--debug",
                      dest = "debug",
                      action = "store_true",
                      default = False,
                      help = "Enable debug mode for Flask")

   parser.add_option ("-f",
                      "--freeze",
                      dest = "freeze",
                      action = "store_true",
                      default = False,
                      help = "Freeze website using Frozen-Flask")

   parser.add_option ("-s",
                      "--socketserver",
                      dest = "socketserver",
                      action = "store_true",
                      default = False,
                      help = "Run Flask web app under standard Python SocketServer, instead of under Twisted")

   parser.add_option ("-p",
                      "--port",
                      dest = "port",
                      default = 8080,
                      help = "Listening port for Web server (i.e. 8090).")

   parser.add_option ("-w",
                      "--widgeturl",
                      dest = "widgeturl",
                      default = "https://demo.crossbar.io/clandeckwidget",
                      help = "WebClan widget base URL.")

   (options, args) = parser.parse_args ()

   app.widgeturl = str(options.widgeturl).strip()
   if len(app.widgeturl) == 0:
      app.widgeturl = None

   EXTRA_MIME_TYPES = {
      '.svg': 'image/svg+xml',
      '.jgz': 'text/javascript'
   }

   if options.freeze:

      from flask_frozen import Freezer
      freezer = Freezer(app)
      freezer.freeze()

      if options.debug:
         import sys, os
         from twisted.python import log
         log.startLogging(sys.stdout)

         from twisted.internet import reactor
         from twisted.web.server import Site
         from twisted.web.static import File

         resource = File(os.path.join(os.path.dirname(__file__), 'build'))
         resource.contentTypes.update(EXTRA_MIME_TYPES)
         site = Site(resource)
         reactor.listenTCP(int(options.port), site)
         reactor.run()

   else:
      if options.socketserver:
         print "Running Flask under standard Python SocketServer"
         app.run(host = "0.0.0.0", port = int(options.port), debug = options.debug)
      else:
         print "Running Flask under Twisted server"
         import sys
         from twisted.python import log
         from twisted.internet import reactor
         from twisted.web.server import Site
         from twisted.web.wsgi import WSGIResource

         app.debug = options.debug
         if options.debug:
            log.startLogging(sys.stdout)
         resource = WSGIResource(reactor, reactor.getThreadPool(), app)
         site = Site(resource)
         # FIXME (does not work)
         #site.contentTypes.update(EXTRA_MIME_TYPES)
         site.noisy = False
         site.log = lambda _: None

         reactor.listenTCP(int(options.port), site)
         reactor.run()
