# -*- coding: utf-8 -*-
import logging
import cons
from utils.response_code import RET
from Base.BaseHandle import BaseHandle
from utils.captcha import captcha
import random

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


class PhoneCodeHandle(BaseHandle):
    """手机验证码"""
    def prepare(self):
        #因为有post传参数 传的是Json数据 所以要解包
        pass
    def post(self, *args, **kwargs):
        #piccode:imageCode, piccode_id
        mobile = self.get_argument('mobile')
        image_code_id = self.get_argument('piccode_id')
        image_code_text = self.get_argument('piccode')

        if all((mobile,image_code_id,image_code_text,)):
            return self.write(dict(error=RET.PARAMERR,errmsg='参数错误'))

        try:
            real_image_code_text = self.redis.get('image_code_%s' % image_code_id)

        except Exception as e:
            return self.write(dict(error=RET.DBERR,errmsg='数据库连接失败'))


        if not real_image_code_text:
            return self.write(dict(error=RET.NODATA,errmsg='验证码过期.请点击刷新'))

        if real_image_code_text.lower() != image_code_text.lower():
            return self.write(dict(errro=RET.DATAERR,errmsg="验证码输入错误"))

        sms_code = '%4d' % random.randint(0,999999)
        print(sms_code)
        # 用第三方短信服务发送到客户端手机....

        try:
            self.redis.setex('sms_code_%s' % mobile,cons.SMS_CODE_EXPIERES_SECONDS,sms_code)

        except Exception as e:
            logging.error(e)
            return self.write(dict(error=RET.DBERR,errmsg='生成验证码错误'))





