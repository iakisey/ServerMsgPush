from . import BaseHandler, app


@app.route(r'/')
class MainHandler(BaseHandler):
    def get(self):
        1/0
