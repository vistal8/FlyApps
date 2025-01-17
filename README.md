### 用与应用分发，苹果超级签名
#### 部署前准备
- 备案域名【至少需要一个域名，以下可通过子域名部署】
  - API域名
  - 前端web域名
  - 下载页域名
    - 下载页域名可配置多个
  - 存储域名（使用阿里云oss存储）
- ssl证书
    - API域名证书
    - 存储域名证书（使用阿里云oss存储）
    - 前端web域名证书（可选）
- Centos8Stream 服务器
    - 如果使用oss存储，则带宽为1M,若使用本地存储，则带宽越大越好
    - 如果使用超级签，最低配置为2cpu 4G内存，若干不使用签名，则1cpu2G就行
- 阿里云短信或极光短信服务【可选一个，主要用与注册，重置密码】
  - 阿里云短信
  - 极光短信
- 邮箱服务【可选，用与注册，重置密码，通知信息】
- 阿里云OSS存储【可选】
    - [sts授权配置](https://help.aliyun.com/document_detail/100624.html)
- 阿里云CDN【可选，用与加速访问】
- 极验验证【可选，滑动验证服务】
- 微信公众号【可选，用与微信扫描登录】
- 阿里云支付【可选，用与购买下载次数】
- 微信支付【可选，用与购买下载次数】

#### 自用搭建建议
- 阿里云服务器需要1cpu 2G内存，无需系统盘，如果使用超级签，可以适当增加配置
- 需要阿里云OSS存储和阿里云CDN,并且OSS存储和阿里云服务器部署同一个地区
- 可以申请一个极验进行滑动验证，或者开启验证码验证
- 阿里云备案域名：api和前端可以使用一个域名，下载页单独域名

#### 部署必备资料
- 域名证书
  - web域名和证书
  - api域名和证书
  - 下载页域名（可配置证书）
  - 存储域名和证书
    - 本地存储，则该域名和证书可以和api域名证书一致
    - 阿里云oss存储
      - 开启cdn，需要新域名和证书
      - 不开启，无需域名和证书
- Centos8Stream 服务器

## 部署方式

### 1.[Docker 部署](./doc/docker.md) 【推荐】

### 2.[本地部署](./doc/local.md)

### 功能预览
![img_1.png](./doc/images/img_1.png)
![img_2.png](./doc/images/img_2.png)
![img_3.png](./doc/images/img_3.png)
![img_4.png](./doc/images/img_4.png)
![img_5.png](./doc/images/img_5.png)
![img_6.png](./doc/images/img_6.png)
![img_7.png](./doc/images/img_7.png)
![img_8.png](./doc/images/img_8.png)
![img_9.png](./doc/images/img_9.png)
![img_10.png](./doc/images/img_10.png)
![img_11.png](./doc/images/img_11.png)