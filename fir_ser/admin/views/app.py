#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project: 4月 
# author: liuyu
# date: 2021/4/11

from django.contrib import auth
from api.models import Token, AppReleaseInfo, Apps
from rest_framework.response import Response
from api.utils.auth import AdminTokenAuthentication
from api.utils.serializer import AdminAppsSerializer, AdminAppReleaseSerializer
from django.core.cache import cache
from rest_framework.views import APIView
import binascii
import os, datetime
from api.utils.utils import get_captcha, valid_captcha, get_choices_dict
from api.utils.response import BaseResponse
from fir_ser.settings import CACHE_KEY_TEMPLATE, LOGIN
from api.utils.storage.caches import login_auth_failed, del_cache_response_by_short
import logging
from api.utils.throttle import VisitRegister1Throttle, VisitRegister2Throttle
from rest_framework.pagination import PageNumberPagination

logger = logging.getLogger(__name__)


class AppsPageNumber(PageNumberPagination):
    page_size = 20  # 每页显示多少条
    page_size_query_param = 'limit'  # URL中每页显示条数的参数
    page_query_param = 'page'  # URL中页码的参数
    max_page_size = None  # 最大页码数限制


class AppInfoView(APIView):
    authentication_classes = [AdminTokenAuthentication, ]

    def get(self, request):
        res = BaseResponse()
        filter_data = {}
        filter_fields = ["id", "type", "name", "short", "bundle_id", "domain_name", "user_id", "status"]
        for filed in filter_fields:
            f_value = request.query_params.get(filed, None)
            if f_value:
                filter_data[filed] = f_value
        sort = request.query_params.get("sort", "-updated_time")
        page_obj = AppsPageNumber()
        obj_list = Apps.objects.filter(**filter_data).order_by(sort)
        page_serializer = page_obj.paginate_queryset(queryset=obj_list, request=request,
                                                     view=self)
        serializer_obj = AdminAppsSerializer(page_serializer, many=True)
        res.data = serializer_obj.data
        res.total = obj_list.count()
        return Response(res.dict)

    def put(self, request):
        res = BaseResponse()
        data = request.data
        id = data.get("id", None)
        if not id:
            res.code = 1003
            res.msg = "参数错误"
            return Response(res.dict)
        app_obj = Apps.objects.filter(id=id).first()
        if app_obj:
            data['pk'] = id
            serializer_obj = AdminAppsSerializer(app_obj, data=data, partial=True)
            if serializer_obj.is_valid():
                serializer_obj.save()
                res.data = serializer_obj.data
                del_cache_response_by_short(app_obj.app_id)
                return Response(res.dict)
        res.code = 1004
        res.msg = "数据校验失败"
        return Response(res.dict)


class AppReleaseInfoView(APIView):
    authentication_classes = [AdminTokenAuthentication, ]

    def get(self, request):
        res = BaseResponse()
        filter_data = {}
        filter_fields = ["id", "release_id"]
        for filed in filter_fields:
            f_value = request.query_params.get(filed, None)
            if f_value:
                filter_data[filed] = f_value
        sort = request.query_params.get("sort", "-created_time")
        page_obj = AppsPageNumber()
        obj_list = AppReleaseInfo.objects.filter(**filter_data).order_by(sort)
        page_serializer = page_obj.paginate_queryset(queryset=obj_list, request=request,
                                                     view=self)
        serializer_obj = AdminAppReleaseSerializer(page_serializer, many=True)
        res.data = serializer_obj.data
        res.total = obj_list.count()
        return Response(res.dict)

    def put(self, request):
        res = BaseResponse()
        data = request.data
        id = data.get("id", None)
        if not id:
            res.code = 1003
            res.msg = "参数错误"
            return Response(res.dict)
        app_obj = Apps.objects.filter(id=id).first()
        if app_obj:
            data['pk'] = id
            serializer_obj = AdminAppReleaseSerializer(app_obj, data=data, partial=True)
            if serializer_obj.is_valid():
                serializer_obj.save()
                res.data = serializer_obj.data
                del_cache_response_by_short(app_obj.app_id)
                return Response(res.dict)
        res.code = 1004
        res.msg = "数据校验失败"
        return Response(res.dict)