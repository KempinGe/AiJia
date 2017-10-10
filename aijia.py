
import logging
import cons
from utils.response_code import RET
from Base.BaseHandle import BaseHandle
from utils.captcha import captcha
import random
import json
from utils.conmon import require_logined

#tail -f log 命令实时查看log日志
class IndexHandle(BaseHandle):
    def prepare(self):
        pass
    def get_current_user(self):
        pass

    def get(self, *args, **kwargs):
        return  self.write({'title': 'text','data':"hello word"})


class VerifyCodeImageHandle(BaseHandle):
    @require_logined
    def get(self, *args, **kwargs):
        #self.xsrf_token
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
            self.redis.setex(name='image_code_%s' % code_id,time=cons.IMAGE_CODE_EXPIERES_SECONDS,value=text)
        except Exception as e:
            print('存储失败')
            logging.error(e)
            self.write('')
        self.set_header('Content-Type','image/jpg')
        print(pre_code_id)
        self.write(image)


class PhoneCodeHandle(BaseHandle):
    """手机验证码"""
    # def prepare(self):
    #     #因为有post传参数 传的是Json数据 所以要解包
    #     pass
    @require_logined
    def post(self, *args, **kwargs):
        #piccode:imageCode, piccode_id
        data_dic = json.loads(self.request.body)
        mobile = data_dic['mobile']
        image_code_id = data_dic['piccode_id']
        image_code_text = data_dic['piccode']
        print(mobile,image_code_id,image_code_text)
        if not all((mobile,image_code_id,image_code_text)):
            return self.write(dict(error=RET.PARAMERR,errmsg='参数错误'))

        try:
            real_image_code_text = self.redis.get('image_code_%s' % image_code_id)

        except Exception as e:
            return self.write(dict(error=RET.DBERR,errmsg='数据库连接失败'))


        if not real_image_code_text:
            return self.write(dict(error=RET.NODATA,errmsg='验证码过期.请点击刷新'))

        if real_image_code_text.decode('ascii').lower() != image_code_text.lower():
            return self.write(dict(errro=RET.DATAERR,errmsg="验证码输入错误"))

        sms_code = '%6d' % random.randint(0,999999)
        print(sms_code)
        # 用第三方短信服务发送到客户端手机....

        try:
            self.redis.setex('sms_code_%s' % mobile,cons.SMS_CODE_EXPIERES_SECONDS,sms_code)

        except Exception as e:
            logging.error(e)
            return self.write(dict(error=RET.DBERR,errmsg='生成验证码错误'))



class Register_Handle(BaseHandle):
    def post(self, *args, **kwargs):
        pass


