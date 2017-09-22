# -*- coding: utf-8 -*-
import aijia
from tornado.web import StaticFileHandler
from settings import TEMPLATE_PATH
urls = [
    # (r"/",aijia.IndexHandle),
    (r'/api/VerifyCode',aijia.VerifyCodeImageHandle),
    (r'PhoneCode',aijia.PhoneCodeHandle),
    (r'/(.*)',StaticFileHandler,dict(path=TEMPLATE_PATH,default_filename='index.html'))
]