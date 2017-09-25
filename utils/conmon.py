from utils.response_code import RET
import functools
def require_logined(func):
    @functools.wraps(func)   #这个装饰器 是保持被装饰的方法 不会被装饰器改名字
    def log_warpper(request_handle,*args,**kwargs):
        #如果get_current_user返回的不是一个孔子点  那么表示用户一金刚登陆过
        if not request_handle.get_current_user():
            func(request_handle,*args,**kwargs)
        else:
            #如果是空字典 那么表示用户未登录 没有保存用户的session数据
            request_handle.write(dict(error=RET.SESSIONERR,errmsg='用户未登录'))

    return log_warpper
