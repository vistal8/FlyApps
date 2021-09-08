#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project: 4月
# author: liuyu
# date: 2020/4/24
import datetime

from api.utils.app.shellcmds import shell_command, use_user_pass
from api.utils.baseutils import get_format_time, format_apple_date
from fir_ser.settings import SUPER_SIGN_ROOT
import os
from api.utils.app.randomstrings import make_app_uuid
import logging
from api.utils.apple.appleapiv3 import AppStoreConnectApi
import base64
from OpenSSL.crypto import (load_pkcs12, dump_certificate_request, dump_privatekey, PKey, TYPE_RSA, X509Req,
                            dump_certificate, load_privatekey, load_certificate, PKCS12, FILETYPE_PEM, FILETYPE_ASN1)

logger = logging.getLogger(__name__)


def exec_shell(cmd, remote=False, timeout=None):
    if remote:
        host_ip = "10.66.6.66"
        port = 65534
        user = "root"
        passwd = "root"
        result = use_user_pass(host_ip, port, user, passwd, cmd)
        return result
    else:
        logger.info(f"exec_shell cmd:{cmd}")
        result = shell_command(cmd, timeout)
        logger.info(f"exec_shell cmd:{cmd}  result:{result}")
        if result.get("exit_code") != 0:
            err_info = result.get("err_info", None)
            if err_info:
                logger.error(f"exec_shell cmd:{cmd}  failed: {err_info}")
                result["err_info"] = "Unknown Error"
            return False, result
        return True, result


class ResignApp(object):

    def __init__(self, my_local_key, app_dev_pem, app_dev_p12):
        self.my_local_key = my_local_key
        self.app_dev_pem = app_dev_pem
        self.app_dev_p12 = app_dev_p12
        self.cmd = "zsign  -c '%s'  -k '%s' " % (self.app_dev_pem, self.my_local_key)

    @staticmethod
    def sign_mobile_config(mobile_config_path, sign_mobile_config_path, ssl_pem_path, ssl_key_path):
        """
        :param mobile_config_path:  描述文件绝对路径
        :param sign_mobile_config_path: 签名之后的文件绝对路径
        :param ssl_pem_path:    pem证书的绝对路径
        :param ssl_key_path:    key证书的绝对路径
        :return:
        """
        cmd = "openssl smime -sign -in %s -out %s -signer %s " \
              "-inkey %s -certfile %s -outform der -nodetach " % (
                  mobile_config_path, sign_mobile_config_path, ssl_pem_path, ssl_key_path, ssl_pem_path)
        return exec_shell(cmd)

    def make_p12_from_cert(self, password):
        result = {}
        try:
            certificate = load_certificate(FILETYPE_PEM, open(self.app_dev_pem, 'rb').read())
            private_key = load_privatekey(FILETYPE_PEM, open(self.my_local_key, 'rb').read())
            p12 = PKCS12()
            p12.set_certificate(certificate)
            p12.set_privatekey(private_key)
            with open(self.app_dev_p12, 'wb+') as f:
                f.write(p12.export(password))
            if password:
                with open(self.app_dev_p12 + '.pwd', 'w') as f:
                    f.write(password)
            return True, p12.get_friendlyname()
        except Exception as e:
            result["err_info"] = e
            return False, result

    def write_cert(self):
        for file in [self.app_dev_p12, self.app_dev_p12 + '.pwd', self.my_local_key, self.app_dev_pem]:
            if os.path.exists(file):
                os.rename(file, file + '.' + get_format_time() + '.bak')
            os.rename(file + '.bak', file)

    def make_cert_from_p12(self, password, p12_content=None):
        result = {}
        try:
            if p12_content:
                p12_content_list = p12_content.split('data:application/x-pkcs12;base64,')
                if len(p12_content_list) == 2:
                    with open(self.app_dev_p12 + '.bak', 'wb+') as f:
                        f.write(base64.b64decode(p12_content.split('data:application/x-pkcs12;base64,')[1]))
                    if password:
                        with open(self.app_dev_p12 + '.pwd.bak', 'w') as f:
                            f.write(password)
                else:
                    result["err_info"] = '非法p12证书文件，请检查'
                    return False, result
            else:
                result["err_info"] = '证书内容有误，请检查'
                return False, result
            p12 = load_pkcs12(open(self.app_dev_p12 + '.bak', 'rb').read(), password)
            cert = p12.get_certificate()
            if cert.has_expired():
                result["err_info"] = '证书已经过期'
                return False, result
            with open(self.my_local_key + '.bak', 'wb+') as f:
                f.write(dump_privatekey(FILETYPE_PEM, p12.get_privatekey()))
            with open(self.app_dev_pem + '.bak', 'wb+') as f:
                f.write(dump_certificate(FILETYPE_PEM, cert))
            return True, cert.get_version()
        except Exception as e:
            for file in [self.app_dev_p12, self.app_dev_p12 + '.pwd', self.my_local_key, self.app_dev_pem]:
                if os.path.exists(file + '.bak'):
                    os.remove(file + '.bak')
            result["err_info"] = e
            if 'mac verify failure' in str(e):
                result["err_info"] = 'p12 导入密码错误，请检查'
            return False, result

    def sign(self, new_profile, org_ipa, new_ipa, info_plist_properties=None):
        if info_plist_properties is None:
            info_plist_properties = {}
        properties = ""
        for k, v in info_plist_properties.items():
            properties += " %s '%s' " % (k, v)
        self.cmd = self.cmd + " %s -m '%s' -o '%s' -z 9 '%s'" % (properties, new_profile, new_ipa, org_ipa)
        return exec_shell(self.cmd)


def make_csr_content(csr_file_path, private_key_path):
    # create public/private key
    key = PKey()
    key.generate_key(TYPE_RSA, 2048)
    # Generate CSR
    req = X509Req()
    req.get_subject().CN = 'FLY APP'
    req.get_subject().O = 'FLY APP Inc'
    req.get_subject().OU = 'IT'
    req.get_subject().L = 'BJ'
    req.get_subject().ST = 'BJ'
    req.get_subject().C = 'CN'
    req.get_subject().emailAddress = 'flyapps@126.com'
    req.set_pubkey(key)
    req.sign(key, 'sha256')
    csr_content = dump_certificate_request(FILETYPE_PEM, req)
    with open(csr_file_path, 'wb+') as f:
        f.write(csr_content)
    with open(private_key_path, 'wb+') as f:
        f.write(dump_privatekey(FILETYPE_PEM, key))

    return csr_content


def make_pem(cer_content, pem_path):
    cert = load_certificate(FILETYPE_ASN1, cer_content)
    with open(pem_path, 'wb+') as f:
        f.write(dump_certificate(FILETYPE_PEM, cert))


class AppDeveloperApiV2(object):
    def __init__(self, issuer_id, private_key_id, p8key, cert_id):
        self.issuer_id = issuer_id
        self.private_key_id = private_key_id
        self.p8key = p8key
        self.cert_id = cert_id

    def active(self):
        result = {'data': []}
        try:
            apple_obj = AppStoreConnectApi(self.issuer_id, self.private_key_id, self.p8key)
            certificates = apple_obj.get_all_certificates()
            result['data'] = certificates
            logger.info(f"ios developer active result:{certificates}")
            if len(certificates) > 0:
                return True, result
        except Exception as e:
            logger.error(f"ios developer active Failed Exception:{e}")
            result['return_info'] = "%s" % e
        return False, result

    def file_format_path_name(self, user_obj):
        cert_dir_name = make_app_uuid(user_obj, self.issuer_id)
        cert_dir_path = os.path.join(SUPER_SIGN_ROOT, cert_dir_name)
        if not os.path.isdir(cert_dir_path):
            os.makedirs(cert_dir_path)
        return os.path.join(cert_dir_path, cert_dir_name)

    def create_cert(self, user_obj):
        result = {}
        try:
            apple_obj = AppStoreConnectApi(self.issuer_id, self.private_key_id, self.p8key)
            csr_path = self.file_format_path_name(user_obj)
            if not os.path.isdir(os.path.dirname(csr_path)):
                os.makedirs(os.path.dirname(csr_path))
            csr_content = make_csr_content(csr_path + ".csr", csr_path + ".key")
            certificates = apple_obj.create_certificate(csr_content.decode("utf-8"))
            if certificates:
                n = base64.b64decode(certificates.certificateContent)
                with open(csr_path + ".cer", 'wb') as f:
                    f.write(n)
                make_pem(n, csr_path + ".pem")
                logger.info(f"ios developer create cert result:{certificates.certificateContent}")
                return True, certificates
        except Exception as e:
            logger.error(f"ios developer create cert Failed Exception:{e}")
            result['return_info'] = "%s" % e
        return False, result

    def get_cert_obj_by_cid(self):
        result = {}
        try:
            apple_obj = AppStoreConnectApi(self.issuer_id, self.private_key_id, self.p8key)
            cert_obj = apple_obj.get_certificate_by_cid(self.cert_id)
            if cert_obj and cert_obj.id:
                return True, result
            else:
                logger.info(f"ios developer get cert {self.cert_id} failed")
                return False, result
        except Exception as e:
            logger.error(f"ios developer get cert {self.cert_id} Failed Exception:{e}")
            result['return_info'] = "%s" % e
        return False, result

    def revoke_cert(self):
        result = {}
        try:
            apple_obj = AppStoreConnectApi(self.issuer_id, self.private_key_id, self.p8key)
            cert_obj = apple_obj.get_certificate_by_cid(self.cert_id)
            if cert_obj:
                s_date = format_apple_date(cert_obj.expirationDate)
                if s_date.timestamp() - datetime.datetime.now().timestamp() < 3600 * 24 * 3:
                    if apple_obj.revoke_certificate(self.cert_id):
                        logger.info(f"ios developer cert {self.cert_id} revoke")
                        return True, result
                else:
                    logger.info(f"ios developer cert {self.cert_id} not revoke.because expire time < 3 day ")
                    return True, result
        except Exception as e:
            logger.error(f"ios developer cert {self.cert_id} revoke Failed Exception:{e}")
            result['return_info'] = "%s" % e
        return False, result

    def auto_set_certid_by_p12(self, app_dev_pem):
        result = {}
        try:
            cer = load_certificate(FILETYPE_PEM, open(app_dev_pem, 'rb').read())
            not_after = datetime.datetime.strptime(cer.get_notAfter().decode('utf-8'), "%Y%m%d%H%M%SZ")
            apple_obj = AppStoreConnectApi(self.issuer_id, self.private_key_id, self.p8key)
            certificates = apple_obj.get_all_certificates()
            for cert_obj in certificates:
                f_date = format_apple_date(cert_obj.expirationDate)
                logger.info(f"{cert_obj.id}-{not_after.timestamp()} - {f_date.timestamp()} ")
                if not_after.timestamp() == f_date.timestamp():
                    return True, cert_obj
            return False, result
        except Exception as e:
            logger.error(f"ios developer cert {app_dev_pem} auto get Failed Exception:{e}")
            result['return_info'] = "%s" % e
        return False, result

    def get_profile(self, app_obj, udid_info, provisionName, auth, developer_app_id,
                    device_id_list, err_callback):
        result = {}
        bundle_id = app_obj.bundle_id
        app_id = app_obj.app_id
        s_type = app_obj.supersign_type
        try:
            apple_obj = AppStoreConnectApi(self.issuer_id, self.private_key_id, self.p8key)
            if developer_app_id:
                pass
            else:
                if s_type == 0:
                    bundle_obj = apple_obj.register_bundle_id(app_id, bundle_id + app_id)
                else:
                    bundle_obj = apple_obj.register_bundle_id_enable_capability(app_id, bundle_id + app_id, s_type)
                developer_app_id = bundle_obj.id
                result['aid'] = developer_app_id
            if udid_info:
                device_udid = udid_info.get('udid')
                device_name = udid_info.get('product')
                device_obj = apple_obj.register_device(device_name, device_udid)
                if device_obj:
                    result['did'] = device_obj.id
                    device_id_list.append(device_obj.id)

            profile_obj = apple_obj.create_profile(developer_app_id, auth.get('cert_id'),
                                                   provisionName.split("/")[-1],
                                                   device_id_list)
            if profile_obj:
                n = base64.b64decode(profile_obj.profileContent)
                if not os.path.isdir(os.path.dirname(provisionName)):
                    os.makedirs(os.path.dirname(provisionName))
                with open(provisionName, 'wb') as f:
                    f.write(n)
                return True, result
        except Exception as e:
            logger.error(f"app_id {app_obj.app_id} ios developer make profile Failed Exception:{e}")
            result['return_info'] = "%s" % e
            if "There are no current ios devices" in str(e):
                err_callback()

            return False, result

    def del_profile(self, app_id):
        result = {}
        try:
            apple_obj = AppStoreConnectApi(self.issuer_id, self.private_key_id, self.p8key)
            profile_obj = apple_obj.list_profile_by_profile_name(app_id)
            if profile_obj:
                if apple_obj.delete_profile_by_id(profile_obj.id):
                    return True, profile_obj
        except Exception as e:
            logger.error(f"ios developer delete profile Failed Exception:{e}")
            result['return_info'] = "%s" % e
            return False, result

    def set_device_status(self, status, device_udid):
        result = {}
        try:
            apple_obj = AppStoreConnectApi(self.issuer_id, self.private_key_id, self.p8key)
            if status == "enable":
                device_obj = apple_obj.enabled_device(device_udid)
            else:
                device_obj = apple_obj.disabled_device(device_udid)
            logger.info("device_obj %s result:%s" % (device_obj, status))
            if device_obj and device_obj.id:
                return True, result
        except Exception as e:
            logger.error("ios developer set devices status Failed Exception:%s" % e)
            result['return_info'] = "%s" % e
        return False, result

    def get_device(self):
        result = {}
        try:
            apple_obj = AppStoreConnectApi(self.issuer_id, self.private_key_id, self.p8key)
            devices_obj_list = apple_obj.list_enabled_devices()
            if devices_obj_list is not None:
                return True, devices_obj_list
        except Exception as e:
            logger.error("ios developer get device Failed Exception:%s" % e)
            result['return_info'] = "%s" % e
            return False, result

    def del_app(self, bundleId, app_id):
        result = {}
        try:
            apple_obj = AppStoreConnectApi(self.issuer_id, self.private_key_id, self.p8key)
            if apple_obj.delete_bundle_by_identifier(bundleId + app_id):
                return True, {}

        except Exception as e:
            logger.error("ios developer delete app Failed Exception:%s" % e)
            result['return_info'] = "%s" % e
            return False, result

    # 该方法未使用
    def create_app(self, bundleId, app_id, s_type):
        result = {}
        try:
            apple_obj = AppStoreConnectApi(self.issuer_id, self.private_key_id, self.p8key)
            bundle_obj = apple_obj.register_bundle_id_enable_capability(app_id, bundleId + app_id, s_type)
            developer_app_id = bundle_obj.id
            result['aid'] = developer_app_id
            return True, result

        except Exception as e:
            logger.error("ios developer create app Failed Exception:%s" % e)
            result['return_info'] = "%s" % e
            return False, result

    def modify_capability(self, app_obj, developer_app_id):
        bundle_id = app_obj.bundle_id
        app_id = app_obj.app_id
        s_type = app_obj.supersign_type
        result = {}
        try:
            apple_obj = AppStoreConnectApi(self.issuer_id, self.private_key_id, self.p8key)
            if developer_app_id:
                if s_type == 0:
                    result['code'] = apple_obj.disable_capability_by_s_type(developer_app_id)
                else:
                    result['code'] = apple_obj.enable_capability_by_s_type(developer_app_id, s_type)
            else:
                if s_type == 0:
                    bundle_obj = apple_obj.register_bundle_id(app_id, bundle_id + app_id)
                else:
                    bundle_obj = apple_obj.register_bundle_id_enable_capability(app_id, bundle_id + app_id, s_type)
                developer_app_id = bundle_obj.id
                result['aid'] = developer_app_id
            return True, result
        except Exception as e:
            logger.error("ios developer modify_capability Failed Exception:%s" % e)
            result['return_info'] = "%s" % e
            return False, result
