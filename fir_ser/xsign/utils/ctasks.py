#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project: 4月
# author: liuyu
# date: 2020/4/7

import logging
import os
import time

from django.template import loader

from common.core.sysconfig import Config
from fir_ser.settings import SUPER_SIGN_ROOT, SYNC_CACHE_TO_DATABASE
from xsign.models import UserInfo, AppIOSDeveloperInfo
from xsign.utils.supersignutils import IosUtils
from xsign.utils.utils import send_ios_developer_active_status

logger = logging.getLogger(__name__)


def auto_delete_ios_mobile_tmp_file():
    mobile_config_tmp_dir = os.path.join(SUPER_SIGN_ROOT, 'tmp', 'mobile_config')
    for root, dirs, files in os.walk(mobile_config_tmp_dir, topdown=False):
        now_time = time.time()
        for name in files:
            file_path = os.path.join(root, name)
            st_mtime = os.stat(file_path).st_mtime
            if now_time - st_mtime > SYNC_CACHE_TO_DATABASE.get('clean_local_tmp_file_from_mtime', 30 * 60):
                try:
                    os.remove(file_path)
                except Exception as e:
                    logger.error(f"auto_delete_tmp_file {file_path} Failed . Exception {e}")


def auto_check_ios_developer_active():
    all_ios_developer = AppIOSDeveloperInfo.objects.filter(status__in=Config.DEVELOPER_AUTO_CHECK_STATUS,
                                                           auto_check=True)
    error_issuer_id = {}
    for ios_developer in all_ios_developer:
        userinfo = ios_developer.user_id
        err_issuer_id = error_issuer_id.get(userinfo.uid, [])
        if userinfo.supersign_active:
            status, result = IosUtils.active_developer(ios_developer)
            msg = f"auto_check_ios_developer_active  user:{userinfo}  ios.developer:{ios_developer}  status:{status}  result:{result}"
            err_issuer_id.append(ios_developer)
            error_issuer_id[userinfo.uid] = list(set(err_issuer_id))

            if status:
                IosUtils.get_device_from_developer(ios_developer)
                logger.info(msg)
            else:
                logger.error(msg)

    for uid, developer_obj_list in error_issuer_id.items():
        userinfo = UserInfo.objects.filter(uid=uid).first()
        content = loader.render_to_string('check_developer.html',
                                          {'username': userinfo.first_name, 'developer_obj_list': developer_obj_list})
        send_ios_developer_active_status(userinfo, content)
