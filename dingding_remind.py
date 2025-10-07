import os.path
import os.path
import urllib.parse
import hmac
import hashlib
import base64
import urllib.parse
import json
import requests
import time
import datetime


# 钉钉发错误消息
def Dingding_Warning(grade, information, details):
    project = '美团录音上传'
    w_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 警告时间
    timestamp = str(round(time.time() * 1000))  # 生成时间戳
    secret = 'SECe5e20972577ea603ec828831c53e0bfc2ac064c07c259216f72cb0c187915c30'  # 设置机器人模式为加签，此为秘钥

    # 对秘钥进行加密处理
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

    header = {'Content-Type': 'application/json;charset=utf-8'}
    url = 'https://oapi.dingtalk.com/robot/send?access_token=57f0183f439d5946ae2aa8173d9f8c8b2c9fc3ee28d5477e4a4433b22625c391&timestamp={}&sign={}'.format(
        timestamp, sign)
    json_text = {
        "msgtype": "text",
        "text": {"content": '告警项目：{}\n'
                            '告警时间：{}\n'
                            '告警等级：{}\n'  # 缺陷等级一般划分为四个等级：致命、严重、一般、低
                            '告警信息：{}\n'
                            '问题详情：{}'.format(project, w_datetime, grade, information, details)},
        "at": {"atMobiles": [""], "isAtAll": False}
    }
    requests.post(url, json.dumps(json_text), headers=header)


# 钉钉提醒功能
class DingTalkOAForwarder:
    def __init__(self):
        # 钉钉管理后台的配置
        self.app_key = "dingh6t5pywf1fna0wdq"
        self.app_secret = "9oXiMgPwWNxd6dA--Gq_runrQlRd2eT-IVxB6FnOysPXhMFDLi3TvJgkqkVW-hTR"
        self.agent_id = "2660808049"
        self.corp_id = "ding6b1cdba641e6f3a935c2f4657eb6378f"
        self.process_code = 'PROC-AD413253-31EF-4857-93CE-B8D5A99F3304'

        # 钉钉群机器人的配置
        self.get_file_url = 'https://oapi.dingtalk.com/media/upload?access_token='  # 上传文件的url
        self.url = 'https://api.dingtalk.com/v1.0/robot/groupMessages/send?x-acs-dingtalk-access-token='  # 发消息url

        # 群聊配置
        # self.openid = "cideNRWZ7L6xSe4dKbHEkZV/A=="  # 工作助手会话ID
        self.openid = "cidpkjg4Tyd1gm29NXYcdUCgg=="  # 互金群会话ID
        self.robotCode = "dingh6t5pywf1fna0wdq"  # 机器人ID

    # 获取access_token
    def get_access_token(self):
        url = f"https://oapi.dingtalk.com/gettoken?appkey={self.app_key}&appsecret={self.app_secret}"
        response = requests.get(url)
        if response.status_code == 200:
            access_token = response.json()["access_token"]
            return access_token

    # 上传文件,返回media_id
    def get_file(self, file_path):
        file_name = os.path.split(file_path)[1]
        access_token = DingTalkOAForwarder.get_access_token(self)  # 获取token
        print(access_token)
        url = self.get_file_url + "{}&type=file".format(access_token)
        params = {
            "type": "file",
        }
        files = {
            "media": open(file_path, "rb")
        }
        response = requests.post(url, json=params, files=files)
        data = response.json()
        media_id = data['media_id']
        return media_id, file_name

    # 发送text消息
    def ding_sampletext(self, text):
        access_token = DingTalkOAForwarder.get_access_token(self)  # 获取token
        url = self.url + access_token
        msgParam = {
            "content": text
        }
        params = {
            "msgParam": str(msgParam),
            "msgKey": "sampleText",
            "openConversationId": self.openid,
            "robotCode": self.robotCode,
        }
        response = requests.post(url, json=params)
        data = response.json()
        return data

    # 发送文件
    def ding_samplefile(self, mediaid, file_name):
        access_token = DingTalkOAForwarder.get_access_token(self)  # 获取token
        url = self.url + access_token
        msgParam = {"mediaId": mediaid, "fileName": os.path.split(file_name)[1], "fileType": "xlsx"}

        params = {
            "msgParam": str(msgParam),
            "msgKey": "sampleFile",
            "openConversationId": self.openid,
            "robotCode": self.robotCode,
        }
        response = requests.post(url, json=params)
        data = response.json()
        return data
