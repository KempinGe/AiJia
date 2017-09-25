from Base.BaseHandle import BaseHandle
import logging
from utils.imageStorge import storage

class AvatarHandle(BaseHandle):
    """用户上传头像 """
    def post(self, *args, **kwargs):
        try:
            key = self.request.files["avatar"][0]["body"]
        except Exception as e:
            #参数出错
            logging.error(e)
            return self.write("")

        try:
            # self.db.excute('update')
            #更新数据库
            pass
        except Exception as e:
            logging.error(e)

        return key + ""
