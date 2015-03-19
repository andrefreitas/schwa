from bottle import Bottle, run, static_file, template, response
import webbrowser

app = Bottle()

@app.route('/')
def index():
    return template('schwa/web/views/index')

@app.route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='schwa/web/static')

@app.route("/analytics")
def analytics():
    response.content_type = 'application/json'
    return Server.analytics.to_dict()


class Server(Bottle):
    @staticmethod
    def run(analytics):
        Server.analytics = analytics
        webbrowser.open_new("http://localhost:8081")
        run(app, host='localhost', port=8081)
