# -*- coding: utf-8 -*-

from playhouse.pool import PooledMySQLDatabase
from urls import urls
import settings
from tornado import ioloop ,httpserver,options
from tornado.web import Application
from tornado.options import options,define
import redis
import torndb

define("port",default=8008,type=int,help="")


class AiJiaApplication(Application):
    """"""
    def __init__(self,*args,**kwargs):
        super(AiJiaApplication,self).__init__(*args,**kwargs)
                #使用线程池连接mysql数据库
        # self.db = PooledMySQLDatabase(
        #     database = settings.MYSQL_SETTINGS['database'],
        #     max_connections = settings.MYSQL_SETTINGS['max_connections'],
        #     timeout = settings.MYSQL_SETTINGS['timeout'],
        #     host = settings.MYSQL_SETTINGS['host'],
        #     user = settings.MYSQL_SETTINGS['user'],
        #     password = settings.MYSQL_SETTINGS['password']
        # )
        self.db = torndb.Connection(**(settings.MYSQL_SETTINGS))
            # PooledMySQLDatabase(**(settings.MYSQL_SETTINGS))
        # self.redis = redis.StrictRedis(
        #     host = settings.REDIS_SETTINGS['host'],
        #     port = settings.REDIS_SETTINGS['port'],
        # )
        self.redis = redis.StrictRedis(**(settings.REDIS_SETTINGS))



def main():
    options.logging = settings.LOG_LEVAL
    options.log_file_prefix = settings.LOG_FILE
    options.parse_command_line()
    app = AiJiaApplication(urls,**(settings.app_settings))
    http_request = httpserver.HTTPServer(app)
    http_request.listen(options.port)
    ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()