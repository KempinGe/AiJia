# -*- coding: utf-8 -*-
import logging
import cons
from Base.BaseHandle import BaseHandle
from utils.captcha import captcha

#tail -f log 命令实时查看log日志
class IndexHandle(BaseHandle):
    def get(self, *args, **kwargs):
        self.write('hello tornado')


class VerifyCodeImageHandle(BaseHandle):
    def get(self, *args, **kwargs):
        code_id = self.get_argument('cur','')
        pre_code_id = self.get_argument('pre','')
        if pre_code_id:
            try:
                 self.redis.delete('pre_code_%s',pre_code_id)
            except Exception as e:
                logging.error(e)

        # name 验证码图片名称
        # text 验证码
        # image 验证码图片的二进制文件
        name,text,image = captcha.Captcha().generate_captcha()
        try:
            self.redis.setex('image_code_%s' % code_id,cons.IMAGE_CODE_EXPIERES_SECONDS,text)
        except Exception as e:
            logging.error(e)
            self.write('')
        self.set_header('Content-Type','image/jpg')
        print(pre_code_id)
        self.write(image)

