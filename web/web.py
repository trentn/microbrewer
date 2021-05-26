from flask import Flask
import threading
from werkzeug.serving import make_server

class WebServer(threading.Thread):
    def __init__(self, system):
        self.system = system
        self.flask_app = Flask("Microbrewer")

        self.flask_app.add_url_rule("/", view_func=self.index)

        
        threading.Thread.__init__(self)
        self.srv = make_server('0.0.0.0', 5000, self.flask_app)
        self.ctx = self.flask_app.app_context()
        self.ctx.push()

    def run(self):
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()
    
    def index(self):
        return "This is working"