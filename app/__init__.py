from configparser import ConfigParser

from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import parse_command_line
from tornado.web import Application, RequestHandler


class Application(Application):
    def __init__(self):
        settings = dict(
            autoreload=True,
            default_handler_class=BaseHandler
        )
        super().__init__(None, **settings)

    def route(self, url):
        def register(handler):
            self.add_handlers('.*$', [(url, handler)])
            return handler
        return register


class BaseHandler(RequestHandler):
    def write_error(self, status_code, **kwargs):
        output_wechat() if 'exc_info' in kwargs and \
            not str(status_code).startswith('4') else None
        self.finish('<html><title>{0}: {1}</title>'
                    '<body>{0}: {1}</body></html>'.format(
                        status_code, self._reason))


def main():
    global config, output_wechat, app
    config = ConfigParser()
    config.read('config')
    from .utility import output_wechat
    app = Application()

    parse_command_line()
    try:
        from .views import app
        http_server = HTTPServer(app)
        http_server.listen(config['base']['port'])
        IOLoop.current().start()
    except Exception as e:
        print(e)
    finally:
        with open('config', 'w') as f:
            config.write(f)
