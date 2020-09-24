"""
Django settings for fir_ser project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j!g@^bc(z(a3*i&kp$_@bgb)bug&^#3=amch!3lz&1x&s6ss6t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api.apps.ApiConfig',
    'django_apscheduler',  # 定时执行任务
    'rest_framework',
    'captcha',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'api.utils.middlewares.CorsMiddleWare'
]

ROOT_URLCONF = 'fir_ser.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fir_ser.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # },
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'flyapp',
        'USER': 'flyuser',
        'PASSWORD': 'KGzKjZpWBp4R4RSa',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        # 设置MySQL的驱动
        # 'OPTIONS': {'init_command': 'SET storage_engine=INNODB'},
        'OPTIONS': {'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"', 'charset': 'utf8mb4'}
    }

}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}
# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

# Media配置
MEDIA_URL = "files/"
MEDIA_ROOT = os.path.join(BASE_DIR, "files")
# supersign配置
SUPER_SIGN_ROOT = os.path.join(BASE_DIR, "supersign")

AUTH_USER_MODEL = "api.UserInfo"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "PASSWORD": "nineven",
            "DECODE_RESPONSES": True
        }
    },
}

# DRF扩展缓存时间
REST_FRAMEWORK_EXTENSIONS = {
    # 缓存时间
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 3600,
    # 缓存存储
    'DEFAULT_USE_CACHE': 'default',
}

# 注册方式，如果启用sms或者email 需要配置 THIRD_PART_CONFIG.sender 信息
REGISTER = {
    "enable": True,
    "ways": {
        'sms': True,  # 短信注册
        'email': True,  # 邮件注册
        'code': False,  # 邀请码注册,邀请码必填写，需要和短信，邮件一起使用
    }
}

LOGIN = {
    "ways": [
        {'sms': False},  # 短信登录
        {'email': True},  # 邮件登录
        {'code': False},  # 密码登录
    ]
}

THIRD_PART_CONFIG = {
    # APP存储配置
    'storage': [
        {
            'name': 'local',
            'type': 0,
            'auth': {
                'domain_name': 'fly.harmonygames.cn',  # 正式环境需要填写正式的访问域名
                'is_https': True,
            },
            'active': True
        },
        {
            'name': 'aliyun',
            'type': 2,
            'auth': {
                'access_key': 'LTAI4FkbTR',
                'secret_key': '2iLIxy9',
                'bucket_name': 'fge',
                'sts_role_arn': 'ap-sage',
                'endpoint': 'oss-cn-beijing.aliyuncs.com',
                'is_https': True,
                'domain_name': 'aoud.xin'
            },
            'active': False
        },
        {
            'name': 'qiniuyun',
            'type': 1,
            'auth': {
                'access_key': 'mT4fiJ',
                'secret_key': '0G9fXfhYLynv',
                'bucket_name': 'fge',
                'is_https': False,
                'domain_name': 'foud.xin'
            },
            'active': False
        }
    ]

}
CACHE_KEY_TEMPLATE = {
    'download_times_key': 'app_download_times',
    'make_token_key': 'make_token',
    'download_short_key': 'download_short',
    'app_instance_key': 'app_instance',
    'download_url_key': 'download_url',
    'user_storage_key': 'storage_auth',
    'user_auth_token_key': 'user_auth_token',
    'download_today_times_key': 'download_today_times',
    'developer_auth_code_key': 'developer_auth_code',
    'upload_file_tmp_name_key': 'upload_file_tmp_name',
    'login_failed_try_times_key': 'login_failed_try_times',
}

DATA_DOWNLOAD_KEY = "d_token"
DATA_DOWNLOAD_KEY_OPEN = True  # 是否开启图片和应用下载token，只本地存储支持该操作
FILE_UPLOAD_TMP_KEY = ".tmp"

SYNC_CACHE_TO_DATABASE = {
    'download_times': 10,  # 下载次数同步时间
    'auto_clean_tmp_file_times': 60 * 30,  # 定时清理上传失误生成的临时文件
    'auto_clean_local_tmp_file_times': 60 * 30,  # 定时清理临时文件,现在包含超级签名描述临时文件
    'try_login_times': 5,  # 当天登录失败次数，超过该失败次数，锁定24小时
    'auto_clean_apscheduler_log': 100000,  # 定时清理定时任务执行的日志,该日志存在数据库中，该参数为日志保留的数量
    'clean_local_tmp_file_from_mtime': 60 * 60,  # 清理最后一次修改时间超过限制时间的临时文件,单位秒
}

SERVER_DOMAIN = {
    'IOS_PMFILE_DOWNLOAD_DOMAIN': {
        "domain_name": 'fly.harmonygames.cn',
        'is_https': True,
    },  # ios 描述文件和plist文件下载域名，该域名用于后端，一般为api访问域名
    'POST_UDID_DOMAIN': 'https://fly.harmonygames.cn',  # 超级签名 安装签名时 向该域名 发送udid数据，该域名用于后端，一般为 api 访问域名
    'REDIRECT_UDID_DOMAIN': 'https://fly.harmonygames.cn',  # 超级签名 安装完成之后，跳转域名，该域名为前端web访问域名，如果用户定义了自己的域名，则跳转用户域名
    'FILE_UPLOAD_DOMAIN': 'https://fly.harmonygames.cn',  # 本地文件上传域名，使用本地存储必须配置
}

MOBILECONFIG_SIGN_SSL = {
    # 描述文件是否签名，默认是关闭状态；如果开启，并且ssl_key_path 和 ssl_pem_path 正常，则使用填写的ssl进行签名,否则默认不签名
    'open': False,
    'ssl_key_path': '/data/cert/fly.harmonygames.cn.key',
    'ssl_pem_path': '/data/cert/fly.harmonygames.cn.pem'
}

DEFAULT_MOBILEPROVISION = {
    # 默认描述文件路径或者下载路径，用户企业签名或者超级签名 跳转 [设置 - 通用 - 描述文件|设备管理] 页面
    # 如果配置了path路径，则走路径，如果配置了url，则走URL，path 优先级大于url优先级
    'enterprise': {
        'path': os.path.join(MEDIA_ROOT, 'embedded.mobileprovision'),
        'url': 'https://ali-static.jappstore.com/embedded.mobileprovision'
    },
    'supersign': {
        # 超级签名，如果self 为True，则默认用自己的描述文件，否则同企业配置顺序一致
        'self': True,
        'path': os.path.join(MEDIA_ROOT, 'embedded.mobileprovision'),
        'url': 'https://ali-static.jappstore.com/embedded.mobileprovision'
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

CAPTCHA_TIMEOUT = 5  # Minutes
CAPTCHA_LENGTH = 6  # Chars

BASE_LOG_DIR = os.path.join(BASE_DIR, "logs")
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]'
                      '[%(levelname)s][%(message)s]'
        },
        'simple': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],  # 只有在Django debug为True时才在屏幕打印日志
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'TF': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',  # 保存到文件，根据时间自动切
            'filename': os.path.join(BASE_LOG_DIR, "flyapp_info.log"),  # 日志文件
            'backupCount': 10,  # 备份数为3  xx.log --> xx.log.2018-08-23_00-00-00 --> xx.log.2018-08-24_00-00-00 --> ...
            'when': 'D',  # 每天一切， 可选值有S/秒 M/分 H/小时 D/天 W0-W6/周(0=周一) midnight/如果没指定时间就默认在午夜
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "flyapp_err.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 50M
            'backupCount': 10,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        '': {  # 默认的logger应用如下配置
            'handlers': ['TF', 'console', 'error'],  # 上线之后可以把'console'移除
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
