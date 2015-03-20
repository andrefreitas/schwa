# Copyright (c) 2015 Faculty of Engineering of the University of Porto
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

""" Module for the Web Server with the Sunburst interface. """

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
    """ Server class.

    This class only have a static method that initiates a new Bottle Server.
    """

    @staticmethod
    def run(analytics):
        """ Runs a web server to display analytics.

        The analytics are displayed in an interactive Sunburst Chart.

        Args:
            analytics: A RepositoryAnalytics instance
        """
        Server.analytics = analytics
        webbrowser.open_new("http://localhost:8081")
        run(app, host='localhost', port=8081)
