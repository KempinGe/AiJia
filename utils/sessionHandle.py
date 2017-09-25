import uuid
import logging
import json
import cons
class GKBSession(object):
    """"""
    def __init__(self,request_handle):
        self.request_handle = request_handle
        self.session_id = self.request_handle.get_secure_cookie('session_id')

        if not self.session_id:
            #如果没有就生成一个全局唯一个session_id
           self.session_id = uuid.uuid4().get_gex()
           self.data = {}
        else:
            try:
                data = self.redis.get('sess_%s' % self.session_id)

            except Exception as e:
                logging.error(e)
                self.data = {}
            if not data:
                data = {}
            else:
                self.data = json.loads(data)

    def save(self):
        json_data = json.dumps(self.data)
        try:
            self.redis.setex('sess_%s' % self.session_id,cons.SESSION_EXPIERES_SECONDS,json_data)
        except Exception as e:
            logging.log(e)
            raise Exception("save session faild")

        else:
            self.request_handle.set_secure_cookie('session_id',self.session_id)


    def clear(self):
        self.request_handle.clear_cookie('session_id')
        try:
            self.redis.delete("sess_%s" % self.session_id)
        except Exception as e:
            logging.log(e)
