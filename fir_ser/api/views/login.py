from django.contrib import auth
from api.models import Token, UserInfo
from rest_framework.response import Response
from api.utils.serializer import UserInfoSerializer
from django.core.cache import cache
from rest_framework.views import APIView
import binascii
import os,datetime
from api.utils.TokenManager import DownloadToken,generateNumericTokenOfLength
from api.utils.auth import ExpiringTokenAuthentication
from api.utils.response import BaseResponse
from django.middleware import csrf
from fir_ser.settings import CACHE_KEY_TEMPLATE

def get_token(request):
    token = csrf.get_token(request)
    return {'csrf_token': token}
class LoginView(APIView):
    def generate_key(self):
        return binascii.hexlify(os.urandom(32)).decode()

    def post(self, request):
        response = BaseResponse()
        receive = request.data

        if request.method == 'POST':
            # print(receive)
            # is_valid = verify(receive)
            is_valid = True
            # print("is_valid", is_valid)
            if is_valid:
                username = receive.get("username")
                password = receive.get("password")
                user = auth.authenticate(username=username, password=password)
                print(username,password,user)
                if user is not None:
                    if user.is_active:

                        # update the token
                        key = self.generate_key()
                        now = datetime.datetime.now()
                        user_info = UserInfo.objects.get(pk=user.pk)

                        auth_key = "_".join([CACHE_KEY_TEMPLATE.get('user_auth_token_key'),key])
                        cache.set(auth_key,{'uid':user_info.uid,'username':user_info.username},3600*24*7)
                        Token.objects.create(user=user, **{"access_token": key, "created": now})

                        serializer = UserInfoSerializer(user_info,)
                        data = serializer.data
                        response.msg = "验证成功!"
                        response.userinfo = data
                        response.token = key
                    else:
                        response.msg = "用户被禁用"
                        response.code = 1002
                else:
                    try:
                        UserInfo.objects.get(username=username)
                        response.msg = "密码错误或者!"
                        response.code = 1002
                    except UserInfo.DoesNotExist:
                        response.msg = "用户不存在!"
                        response.code = 1003
            else:

                response.code = 1001
                response.msg = "请完成滑动验证!"

            return Response(response.dict)

    def get(self,request):
        response = BaseResponse()
        csrf=get_token(request)
        response.data=csrf
        return Response(response.dict)

class UserInfoView(APIView):
    authentication_classes = [ExpiringTokenAuthentication, ]

    def get(self,request):
        res = BaseResponse()
        serializer = UserInfoSerializer(request.user)
        res.data = serializer.data
        act =  request.query_params.get("act",None)
        if act and act == "sms":
            sms_token_obj=DownloadToken()
            sms_code=generateNumericTokenOfLength(6)
            sms_token=sms_token_obj.make_token([sms_code])
            res.data["sms_token"] = sms_token
            res.data["sms_code"] = sms_code

        return Response(res.dict)

    def put(self,request):
        res = BaseResponse()
        request.user.qq=request.data.get("qq",request.user.qq)
        request.user.job=request.data.get("job", request.user.job)
        request.user.first_name=request.data.get("first_name", request.user.first_name)

        oldpassword=request.data.get("oldpassword",None)
        surepassword=request.data.get("surepassword",None)
        if oldpassword and surepassword:
            user = auth.authenticate(username=request.user.username, password=oldpassword)
            if user is not None:
                user.set_password(surepassword)
                user.save()
                res.msg="密码修改成功"

                auth_token = request.auth
                for token_obj in Token.objects.filter(user=user):
                    if token_obj.access_token != auth_token:
                        cache.delete(token_obj.access_token)
                        token_obj.delete()

                return Response(res.dict)
            else:
                res.code = 1004
                res.msg = "老密码校验失败"
        else:

            sms_token = request.data.get("sms_token",None)
            if sms_token:
                sms_token_obj=DownloadToken()
                if sms_token_obj.verify_token(sms_token,request.data.get("sms_code",None)):
                    request.user.mobile=request.data.get("mobile", request.user.mobile)
            request.user.save()
            serializer = UserInfoSerializer(request.user)
            res.data = serializer.data
            return Response(res.dict)

        return Response(res.dict)

