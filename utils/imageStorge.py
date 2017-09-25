from qiniu import Auth, put_file, etag, urlsafe_base64_encode,put_data
import qiniu.config
#需要填写你的 Access Key 和 Secret Key
access_key = 'QN2vfnKeHMgItXt4btFDEMTD7jqP0lXmhO4pBS6v'
secret_key = 'dxPsBk60jivWNAfIW7vwSjMSuiWXkla9CXpwSQnn'



def storage(image_data):
    if not image_data:
        return ''
    #构建鉴权对象
    q = Auth(access_key, secret_key)
    #要上传的空间
    bucket_name = 'gkbbuket'
    #上传到七牛后保存的文件名
    # key = 'my-python-logo.png';
    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, None, 3600)
    #要上传文件的本地路径
    # localfile = './sync/bbb.jpg'
    # ret, info = put_file(token, None, localfile)  #put_data 对应图片的数据
    ret, info = put_data(token,None,image_data)
    print(info)
    # assert ret['key'] #== key
    # assert ret['hash'] == etag(image_data)
    return ret['key']

if __name__ == '__main__':
    f = open('thephoenix.jpg','rb')
    data_f = f.read()
    print(data_f)
    name = storage(data_f)
    print(name)
    f.close()