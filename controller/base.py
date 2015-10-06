#coding=utf-8
__author__='silver'
import tornado.web, json, time, re
import tornado.options
from tornado import gen

def error_process(obj, status_code, **kwargs):
    msgtext=str((kwargs['exc_info'][1]))
    if obj.settings.get("serve_traceback") and "exc_info" in kwargs:
        # in debug mode, try to send a traceback
        import traceback
        for line in traceback.format_exception(*kwargs["exc_info"]):
            obj.write(line)
    obj.set_status(status_code)
    obj.render("err.html", code=status_code, \
                            text=msgtext,\
                            domain=obj.opts.domain,\
                            port=obj.opts.port,\
                            path=obj.request.uri
                            )

class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        self.opts=tornado.options.options
        super(BaseHandler, self).__init__(*args, **kwargs)
    def write_error(self, status_code, **kwargs):
        error_process(self, status_code, **kwargs)

class NotFoundHandler(BaseHandler):
    def get(self, *args, **kwargs):
        raise tornado.web.HTTPError(504)

    def post(self, *args, **kwargs):
        self.get(*args, **kwargs)

class StaticBaseHandler(tornado.web.StaticFileHandler, BaseHandler):
    def write_error(self, status_code, **kwargs):
        error_process(self, status_code, **kwargs)
