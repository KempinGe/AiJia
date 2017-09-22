# -*- coding: utf-8 -*-

from tornado.web import RequestHandler
class BaseHandle(RequestHandler):

    @property
    def db(self):
        return self.application.db

    @property
    def redis(self):
        return self.application.redis

    def prepare(self):
        pass
    def get(self, *args, **kwargs):
        pass
    def post(self, *args, **kwargs):
        pass
    def write_error(self, status_code, **kwargs):
        pass
    def set_default_headers(self):
        pass
    def initialize(self):
        pass
    def on_finish(self):
        pass