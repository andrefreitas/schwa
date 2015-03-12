import cherrypy
import os
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('static'))
current_dir = os.path.dirname(os.path.abspath(__file__))


class Server:
    @staticmethod
    def run(analytics):
        cherrypy.config.update({'server.socket_port': 3456, 'engine.autoreload.on': False})
        conf = {
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': os.path.join(current_dir, 'static')
            }
        }
        cherrypy.quickstart(root=Sunburst(analytics), config=conf)


class Sunburst(object):
    def __init__(self, analytics):
        self.analytics = analytics

    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index.html')
        return tmpl.render()