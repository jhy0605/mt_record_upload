import os.path
import os.path
import shutil
import zipfile
import pymysql
import psycopg2
import json
import requests
import time
import datetime
from dingding_remind import Dingding_Warning, DingTalkOAForwarder
from db import open_sql
import win32cred


# 更新windows凭据
def add_windows_credential():
    voucher_disk = {'10.10.100.203': ['record_syn', 'Admin@1234'],
                    '10.10.100.204': ['jw\jianghongyu', 'Jw.dh@@@@2222'],
                    '10.10.100.83': ['record_syn', 'Admin@1234'],
                    '10.10.100.211': ['okccsmb', 'Admin@1234'],
                    '172.20.50.249': ['dhvoip', 'Admin@1234'],
                    '192.168.106.249': ['mfvoip', 'Admin@1234'],
                    '10.10.100.209': ['record_syn', 'Admin@1234'],
                    }

    for share in voucher_disk.keys():
        u_list = voucher_disk[share]
        username = u_list[0]
        password = u_list[1]
        # 准备凭证信息
        credential = {
            'TargetName': share,
            'Type': win32cred.CRED_TYPE_DOMAIN_PASSWORD,
            'UserName': username,
            'CredentialBlob': password,
            'Persist': win32cred.CRED_PERSIST_LOCAL_MACHINE  # 或者使用 win32cred.CRED_PERSIST_ENTERPRISE，根据需要选择
        }
        # 添加凭证
        try:
            win32cred.CredWrite(credential, 0)
            print('{}凭据添加成功'.format(share))
        except Exception as k:
            print('{}凭据添加失败'.format(share))


# 下载指掌易录音，时间周期为近三天上传到指掌易系统的录音
# class zhizhangyi_download:
#     def __init__(self):
#         self.download_path = os.path.join(r'C:\Users', os.getlogin(), 'Downloads')  # 录音下载位置
#         self.str_time = ''
#         self.record_path = ''  # 录音存放位置
#
#         # 指掌易web参数
#         self.web_url = 'https://10.10.100.209:9074/wld#/login'
#         self.web_user = 'record_syn'
#         self.web_passwd = 'Admin@1234'
#
#         # 错误日志
#         self.log_path = 'error.log'  # 指定日志文件路径
#
#     # 下载近三天的通话录音
#     def record_down(self):
#         # 先清空下载目录的多余文件
#         for dirs in os.listdir(self.download_path):
#             if dirs != 'desktop.ini':
#                 if os.path.isfile(os.path.join(self.download_path, dirs)):
#                     os.remove(os.path.join(self.download_path, dirs))
#                 else:
#                     shutil.rmtree(os.path.join(self.download_path, dirs))
#
#         record_path = os.path.join(self.download_path, self.str_time)
#
#         # 浏览器操作
#         '''
#         查找方式：
#             1、通过ID进行定位 browser.find_element(By.ID, 'details-button').click()
#             2、通过元素的 Name 属性进行定位  browser.find_element(By.TAG_NAME, 'aui-button').click()
#             3、通过Xpath定位元素，driver.find_element(By.XPATH, '//div[@class="example"]')
#             xpath定义方法，
#                 1、//* 选择文档中的所有元素
#                 2、//span 选择文档中的所有span元素
#                 3、//aui-button  选择文档中的所有aui-button元素
#                 4、[@class="toggle-title first-title can-open" and contains(text(), "报表管理")]
#                 5、@class="toggle-title first-title can-open"   class的值为：toggle-title first-title can-open
#                 6、contains(@acee, "308")  # acee属性包含字符串：'308'
#                 7、contains(text(), "报表管理")  # 文本包含报表管理
#                 8、text()="报表管理"  # 文本等于报表管理
#         '''
#         try:
#             browser = webdriver.Chrome()  # 打开浏览器
#             browser.maximize_window()  # 最大化窗口
#             # browser.minimize_window()  # 最小化窗口
#
#             browser.get(self.web_url)  # 访问相对应链接
#             time.sleep(3)
#             browser.find_element(By.ID, 'details-button').click()
#             time.sleep(3)
#             browser.find_element(By.ID, 'proceed-link').click()
#             time.sleep(3)
#
#             # 输入账号密码登录系统
#             browser.find_elements(By.TAG_NAME, 'input')[1].send_keys(self.web_user)
#             time.sleep(3)
#             browser.find_elements(By.TAG_NAME, 'input')[2].send_keys(self.web_passwd)
#             WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[text()="登录"]'))).click()
#             # 点击“业务智能分析”
#             time.sleep(10)
#             WebDriverWait(browser, 20).until(
#                 EC.visibility_of_element_located((By.XPATH, '//li[text()="业务智能分析"]'))).click()
#             # 点击“报表管理”
#             time.sleep(10)
#             WebDriverWait(browser, 20).until(
#                 EC.visibility_of_element_located((By.XPATH, '//span[text()="报表管理"]'))).click()
#             # 点击“创建报表”
#             time.sleep(10)
#             WebDriverWait(browser, 20).until(
#                 EC.visibility_of_element_located((By.XPATH, '//aui-button[text()="创建报表"]'))).click()
#
#             # 填写报表
#             # 选择报表名称
#             time.sleep(10)
#             # 将当前时间转换为纯数字字符串，作为报表名称
#             time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
#
#             WebDriverWait(browser, 20).until(
#                 EC.visibility_of_element_located(
#                     (By.XPATH, '//div[@class="aui-input-wrapper hackff" and @placeholder="请输入"]/input'))).send_keys(
#                 time_str)
#             # 点击选择部门
#             time.sleep(10)
#             WebDriverWait(browser, 20).until(
#                 EC.visibility_of_element_located(
#                     (By.XPATH, '//div[@class="aui-input-wrapper hackff" and @placeholder="请选择部门"]/input'))).click()
#             # 输入搜索部门
#             time.sleep(10)
#             WebDriverWait(browser, 20).until(
#                 EC.visibility_of_element_located(
#                     (By.XPATH,
#                      '//div[@class="aui-input-wrapper hackff suffix" and @placeholder="部门名称"]/input'))).send_keys(
#                 '美团')
#             # 点击选择美团项目
#             time.sleep(10)
#             WebDriverWait(browser, 20).until(
#                 EC.visibility_of_element_located(
#                     (By.XPATH,
#                      '//span[@title="美团(总部互金)"]'))).click()
#             # 点开日历
#             time.sleep(10)
#             WebDriverWait(browser, 20).until(
#                 EC.visibility_of_all_elements_located(
#                     (By.XPATH,
#                      '//div[@class="aui-input-wrapper hackff prefix" and @placeholder="开始时间 至 结束时间"]/input')))[
#                 1].click()
#
#             # 根据时间来判断是否翻页
#             time_1 = datetime.datetime.strptime(self.str_time, "%Y%m%d%H%M%S")
#             start_time = (time_1 - datetime.timedelta(days=3)).strftime("%Y%m%d")
#             end_time = time_1.strftime("%Y%m%d")
#             print(start_time, end_time)
#             day1 = int(start_time[6:8])
#             day2 = int(end_time[6:8])
#             print(day1, day2)
#
#             # 点击第一下
#             time.sleep(10)
#             WebDriverWait(browser, 20).until(
#                 EC.visibility_of_element_located(
#                     (By.XPATH,
#                      '//div[@class="calendar-daily calendar-daily-first"]/div[@scope="in" and @date="{}"]'.format(
#                          day2)))).click()
#
#             if day2 < 4:
#                 print('需要翻页')
#                 # 点击翻页
#                 time.sleep(10)
#                 WebDriverWait(browser, 20).until(
#                     EC.visibility_of_element_located(
#                         (By.XPATH,
#                          '//div[@class="calendar-header-left"]/i[@class="icon iconfont iconel-icon-arrow-left"]'))).click()
#
#             # 点击第二下
#             time.sleep(10)
#             WebDriverWait(browser, 20).until(
#                 EC.visibility_of_element_located(
#                     (By.XPATH,
#                      '//div[@class="calendar-daily calendar-daily-first"]/div[@scope="in" and @date="{}"]'.format(
#                          day1)))).click()
#
#             # 点击确定
#             time.sleep(10)
#             WebDriverWait(browser, 20).until(
#                 EC.visibility_of_element_located(
#                     (By.XPATH,
#                      '//aui-button[text()="确定"]'.format(
#                          day1)))).click()
#
#             while True:
#                 browser.refresh()
#                 time.sleep(10)
#                 # tag_name = browser.find_elements(By.TAG_NAME, 'aui-tag')[0].get_attribute("innerText")
#                 tag_name = WebDriverWait(browser, 20).until(
#                     EC.visibility_of_all_elements_located((By.XPATH, '//aui-tag')))[0].get_attribute("innerText")
#                 if tag_name == '报表无内容':
#                     print('数据为空')
#                     os.mkdir(record_path)
#                     # 关闭整个浏览器
#                     browser.quit()
#                     return 0
#                 elif tag_name == '报表已生成':
#                     browser.find_elements(By.TAG_NAME, "aui-checkbox")[1].click()
#                     time.sleep(3)
#                     browser.find_elements(By.TAG_NAME, "aui-button")[3].click()
#                     time.sleep(60)
#                     break
#             time.sleep(10)
#             # 关闭整个浏览器
#             browser.quit()
#         except Exception as k:
#             # 记录异常信息到日志
#             logging.basicConfig(filename=self.log_path, format='%(asctime)s [%(levelname)s] - %(message)s')
#             logging.error("An error occurred: %s", k)
#             logging.error(traceback.format_exc())
#             print(traceback.format_exc())
#             Dingding_Warning('严重', '下载录音失败', traceback.format_exc())
#             return None
#         return 1
#
#     # 解压录音,剔除不符合时间要求的录音,输出录音列表
#     def zip_record(self):
#         print('开始下载指掌易录音')
#         zzy_list_all = []
#         tmp_path = os.path.join(self.download_path, self.str_time)  # 解压的临时文件夹
#
#         # 判断有没有下载文件
#         d = zhizhangyi_download.record_down(self)
#         if d == 1:
#             # 如果有文件，解压文件到临时目录
#             path_file_a = os.path.join(self.download_path, os.listdir(self.download_path)[0])
#             z = zipfile.ZipFile(path_file_a, mode='r')
#             z.extractall(tmp_path)
#             z.close()
#             os.remove(path_file_a)  # 删除压缩包
#
#             # copy录音到指定文件夹
#             for root, dirs, files in os.walk(tmp_path):
#                 for file in files:
#                     file1 = file.replace('-', '_').replace('+86', '')
#                     file_path = os.path.join(root, file)
#                     name = os.path.splitext(file)[0]
#                     if ')' not in name:
#                         date = '{}-{}-{} {}:{}:{}'.format(name[-15:-11], name[-11:-9], name[-9:-7], name[-6:-4],
#                                                           name[-4:-2],
#                                                           name[-2:])
#                         date_l = date[0:10].replace('-', '')
#                         record_path = os.path.join(self.record_path, date_l[0:6], date_l[6:8])  # # 203中存放的目录
#                         phone = name.split('_', 3)[-2]
#                         if not os.path.exists(record_path):
#                             os.makedirs(record_path)
#                         if not os.path.exists(os.path.join(record_path, file1)):
#                             shutil.copy(file_path, os.path.join(record_path, file1))
#                             print('copy:{}'.format(os.path.join(record_path, file1)))
#                             zzy_list_all.append([file1, date, phone, record_path, 'zzy'])
#                         else:
#                             pass
#                             # print('{}文件已经存在。'.format(os.path.join(record_path, file)))
#             if os.path.exists(tmp_path):
#                 shutil.rmtree(tmp_path)  # 删除临时文件夹
#         return zzy_list_all


# 下载指掌易录音，时间周期为近三天上传到指掌易系统的录音
class zhizhangyi_download:
    def __init__(self):
        self.zzy_record_path = r'\\10.10.100.209\wld'
        self.download_path = ''
        self.str_time = ''

    # 下载近三天的通话录音
    def record_down(self):
        zzy_list_all = []
        # 计算最近三天的时间列表
        current_time = datetime.datetime.strptime(self.str_time, "%Y%m%d%H%M%S")
        last_three_days = [(current_time - datetime.timedelta(days=i)).strftime("%Y%m%d") for i in range(3)]
        # 部门列表
        dep_list = []

        if not os.path.exists(self.zzy_record_path):
            Dingding_Warning('严重', '录音下载错误', '指掌易服务器(100.209)录音读取失败')
        for dep_path in os.listdir(self.zzy_record_path):
            if '美团' in dep_path:
                dep_list.append(dep_path)

        for dep in dep_list:
            dep_dir = os.path.join(self.zzy_record_path, dep)
            for three_days in last_three_days:
                dep_file_path = os.path.join(dep_dir, three_days)
                print(dep_file_path)
                for root, dirs, files in os.walk(dep_file_path):
                    for file in files:
                        file1 = file.replace('-', '_').replace('+86', '')
                        file_path = os.path.join(root, file)
                        name = os.path.splitext(file1)[0]
                        if ')' not in name:
                            date = '{}-{}-{} {}:{}:{}'.format(name[-15:-11], name[-11:-9], name[-9:-7], name[-6:-4],
                                                              name[-4:-2],
                                                              name[-2:])
                            date_l = date[0:10].replace('-', '')
                            record_path = os.path.join(self.download_path, date_l[0:6], date_l[6:8])  # # 203中存放的目录
                            phone = name.split('_', 3)[-3]
                            # 筛选条件，去除无效号码
                            if len(phone) > 4:
                                if phone[0:3] != '100':
                                    # copy录音
                                    if not os.path.exists(record_path):
                                        os.makedirs(record_path)
                                    if not os.path.exists(os.path.join(record_path, file1)):
                                        shutil.copy(file_path, os.path.join(record_path, file1))
                                        print('copy:{}'.format(os.path.join(record_path, file1)))
                                        index = [file1, date, phone, record_path, 'zzy']
                                        # print(index)
                                        zzy_list_all.append(index)
        return zzy_list_all


# 下载枫软录音,时间周期为前3天的零点到当前时间
class fengruan_download:
    def __init__(self):
        # 文件存放信息
        self.down_path = None
        self.str_time = ''

        # 当前时间
        self.date_d = datetime.datetime.utcnow()
        self.date_x = self.date_d.strftime("%Y-%m-%d")
        self.time_x = self.date_d.strftime("%H:%M:%S")

        # 登录信息
        self.url = 'http://mscc.frsoft.com.cn/service/index.php?'
        self.name = '广州金湾'
        self.user = 'record_syn'
        self.passwd = '6889f104c45cc4c08a7255267bb1a5a6166098ecd6736b7085af1d46ceac1dc489ff72ce3c44e3414a060c9fb05f010615687367d7039d69570e221730b7251f'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/107.0.0.0 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self.my_data = {"userName": self.user, "password": self.passwd, "rememberMe": 'false',
                        "customerName": self.name, 'client': '2560*1440'}

    # 登录网页,获取cookie
    def login(self):
        # 模拟请求，获响应头
        try:
            res_cookie = requests.post(self.url + 'm=index&c=index&f=checkLogin', headers=self.headers)
        except Exception as k:
            print(k)
            Dingding_Warning('严重', '网络访问错误', k)
            return None
        if res_cookie.status_code != 200:
            print(res_cookie.text)
            Dingding_Warning('严重', '网络访问错误', res_cookie.text)
            return None
        else:
            login_cookie = res_cookie.headers.get("Set-Cookie").split(',')[1].replace(' ', '')
            # print(login_cookie)

            # 模拟请求获取 PHPSESSID
            res_ssid = requests.post(self.url + 'm=login&c=login', headers=self.headers)
            php_sessid = res_ssid.headers.get("Set-Cookie").split(';')[0].replace(' ', '')
            # print(php_sessid)

            # 模拟登录,获取最终cookie
            self.headers['Cookie'] = login_cookie + ';' + php_sessid
            res_login = requests.post(self.url + 'm=login&c=login&f=login', headers=self.headers, data=self.my_data)
            news = json.loads(res_login.text)['result']['error']
            if news == 0:
                print('枫软MSCC呼叫系统，用户登录成功')
                cookie = res_login.headers.get("Set-Cookie")
                # print(cookie)
                return cookie

            else:
                print('用户登录失败：{}'.format(res_login.text))
                Dingding_Warning('严重', '用户登录失败', res_login.text)
                return None

    # 按照日期搜索通话记录,输出搜索结果
    def search_record(self, cookie):
        call_list = []

        # 根据时间区间计算时间戳
        end_date = datetime.datetime.strptime(self.str_time, "%Y%m%d%H%M%S")

        yesterday = end_date - datetime.timedelta(days=3)
        start_date = datetime.datetime.strptime(yesterday.date().strftime('%Y-%m-%d ') + '00:00:00',
                                                "%Y-%m-%d %H:%M:%S")

        print('开始下载{} 至 {}的枫软录音'.format(start_date, end_date))

        start_time = int(time.mktime(start_date.timetuple()))
        end_time = int(time.mktime(end_date.timetuple()))

        # 搜索美团班组的录音
        query_data = 'p={"pagination":{"current":1,"pageSize":9999999},"sorter":{},' \
                     '"filter":{"employeeGroupID":"3686","employeeID":[],"caller":"","callee":"","CID":"","taskID":"",' \
                     '"timeLengthSetting":"4","hasAnswer":"0","qcStatus":"-1","Time":"5","qcTime":0,' \
                     '"startTime":"%s","endTime":"%s","qcStartTime":"","qcEndTime":"",' \
                     '"timestamp":"%s}T%s.367Z"}}' % (start_time, end_time, self.date_x, self.time_x)
        self.headers['Cookie'] = cookie
        res_query = requests.post(self.url + 'm=cdr&c=record&f=query', headers=self.headers, data=query_data)
        res_text = res_query.text  # 返回值
        dick_all = json.loads(res_text)  # 反序列化
        # print(dick_all)
        quantity = dick_all['data']['total']  # 录音数量
        print('搜索成功,录音数量：{}'.format(quantity))

        for call in dick_all['data']['rows']:
            print(call)
            key = call['key']
            date = call['startTime'].replace('-', '').replace(' ', '').replace(':', '')
            caller = call['caller']
            callerd = call['callee']
            start_stamp = call['startTime']
            end_stamp = call['endTime']
            duration = int(call['timeLength'])
            file = call['employeeID'].split(' - ')[0] + '_' + date[0:8] + '_' + date[
                                                                                8:] + '_' + callerd + '_' + caller + '.mp3'
            # print(file)
            path_dirs = os.path.join(self.down_path, date[0:6], date[6:8])

            download_value = [key, os.path.join(path_dirs, file)]
            # print(download_value)

            call_value = [start_stamp, caller, callerd, start_stamp, end_stamp, duration, path_dirs, file]
            # print(call_value)

            call_list.append([download_value, call_value])

        return call_list

    # 根据key值，进行录音下载
    def get_record(self, download_value):
        key = 'id=' + download_value[0]
        filepath = download_value[1]
        dir_path = os.path.split(filepath)[0]  # 录音存放目录
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        if not os.path.exists(filepath):
            res_download = requests.post(self.url + 'm=cdr&c=record&f=downloadOne', headers=self.headers,
                                         data=key)
            if res_download.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(res_download.content)
                    f.close()
                print('get:' + filepath)
                return True
            else:
                print(res_download.text)
                return None
        else:
            return True

    # 下载录音
    def run(self):
        fr_record_list = []
        cookie = fengruan_download.login(self)
        if cookie:
            call_list = fengruan_download.search_record(self, cookie)
            if len(call_list) > 0:
                for call in call_list:
                    if fengruan_download.get_record(self, call[0]):  # 下载录音
                        value = call[1]
                        if value[1][0] == '1':  # 判断哪个是客户号码
                            phone = value[1]
                        else:
                            phone = value[2]
                        # 特殊的手机号码处理
                        if len(phone) == 12 and phone[0:2] == '01':
                            phone = phone[1:]
                        fr_record_list.append([value[7], value[0], phone, value[6], 'fengr'])
        return fr_record_list


# 下载voip录音,时间周期为前3天的零点到当前时间
class voip_download:
    def __init__(self):
        self.str_time = ''
        self.down_path = None

        self.db = 'fusionpbx'
        self.user = 'postgres'
        self.password = '78kxtw'
        self.hosts = ['172.20.50.249', '192.168.106.249']  #
        self.port = '5432'
        self.table = 'v_xml_cdr'
        self.sip_tuple = ('4509', '4510', '4511', '4531', '4532', '4533', '4534', '9607')

    def select_record_list(self):
        list_all = []

        # 根据时间区间计算时间戳
        end_date = datetime.datetime.strptime(self.str_time, "%Y%m%d%H%M%S")
        yesterday = end_date - datetime.timedelta(days=3)
        start_date = datetime.datetime.strptime(yesterday.date().strftime('%Y-%m-%d ') + '00:00:00',
                                                "%Y-%m-%d %H:%M:%S")

        print('开始下载{} 至 {}的VOIP录音'.format(start_date, end_date))

        # 连接pgsql
        for host in self.hosts:
            conn = psycopg2.connect(database=self.db, user=self.user, password=self.password, host=host,
                                    port=self.port)
            curs = conn.cursor()
            #                   0分机号         1主叫号码        2被叫号码          3开始拨打时间  4结束时间   5录音路径    6录音名称
            sql_1 = "SELECT caller_id_name, caller_id_number,destination_number,start_stamp,end_stamp,record_path,record_name " \
                    "FROM {} WHERE start_stamp >= '{}' and start_stamp <'{}' and caller_id_name in {} ;" \
                .format(self.table, start_date, end_date, self.sip_tuple)
            curs.execute(sql_1)  # 查询表
            call_list = curs.fetchall()
            print('搜索成功,录音数量：{}'.format(len(call_list)))
            for call in call_list:
                call = list(call)
                if call[3] is not None and call[5] is not None:
                    # print(call)
                    # 判断客户号码是哪个
                    if call[0] == call[1]:
                        phone = call[2]
                    else:
                        phone = call[1]
                    # 特殊的手机号码处理
                    if len(phone) == 12 and phone[0:2] == '01':
                        phone = phone[1:]

                    date = call[4].strftime("%Y-%m-%d %H:%M:%S")
                    date_d = call[4].strftime("%Y%m%d")

                    file_path = call[5].replace("/var/lib/freeswitch/recordings/", '').replace('/', '\\')
                    if host == '172.20.50.249':
                        filepath = os.path.join(r'\\172.20.50.249\dhvoip', file_path)
                    else:
                        filepath = os.path.join(r'\\192.168.106.249\mfvoip', file_path)

                    d_path = os.path.join(self.down_path, date_d[0:6], date_d[6:8])
                    d_filepath = os.path.join(d_path, call[6])

                    if not os.path.exists(d_path):
                        os.makedirs(d_path)
                    if not os.path.exists(d_filepath):
                        shutil.copy(os.path.join(filepath, call[6]), d_filepath)
                        print('copy', d_filepath)
                        record_index = [call[6], date, phone, d_path, 'voip']
                        # print(record_index)
                        list_all.append(record_index)
            curs.close()
            conn.close()

        return list_all


# 读取共享盘里面的录音,时间不限
class shar_records:
    def __init__(self):
        self.shar_record_path = r'\\10.10.100.204\文件共享\互金\美团项目\技术部共享\手工录音上传\record'

    # 读取手动上传的录音文件
    def open_record(self):
        print('开始读取手工上传录音')
        shar_list_all = []
        er_record_list = []
        p = 0
        # 遍历文件夹，读取需要上传的录音
        for root, dirs, files in os.walk(self.shar_record_path):
            for file in files:
                file_l = os.path.splitext(file)
                if file_l[1] in ['.mp3', '.wav']:
                    try:
                        name = file_l[0]
                        if ')' not in name and '-' not in name and name.count('_') == 3:
                            # print(file)
                            list_l = name.split('_')
                            str_date = list_l[-2] + list_l[-1]
                            date = datetime.datetime.strptime(str_date, "%Y%m%d%H%M%S")  # 时间
                            phone = list_l[1]  # 手机号
                            index_list = [file, date, phone, root, 'shougong']
                            # print(index_list)
                            shar_list_all.append(index_list)
                        else:
                            er_record_list.append(file)
                            p += 1

                    except Exception as k:
                        er_record_list.append(file)
                        print(str(k))
                        p += 1

                else:
                    p += 1
                    er_record_list.append(file)

        # 如果有格式问题
        if p > 0:
            er_txt = '\n'.join(er_record_list)
            text = '手工录音上传文件夹中有{}个录音文件格式错误，无法上上传，请及时修正！\n{}'.format(p, er_txt)
            print(text)
            DingTalkOAForwarder().ding_sampletext(text)  # 钉钉群发送文字
        return shar_list_all


# 下载金湾呼叫系统中的录音，时间周期为前3天的零点到当前时间
class okcc_download:
    def __init__(self):
        self.str_time = ''
        self.down_path = None
        self.db = 'ccdata'
        self.user = 'mysql'
        self.password = 'Tianhe@okcc.2024'
        self.hosts = ['10.10.100.211', ]
        self.port = 3306
        self.mysqldb = pymysql.connect(host=self.hosts[0], port=self.port, user=self.user,
                                       password=self.password, database=self.db)  # 打开数据库链接
        self.curs = self.mysqldb.cursor()

    def select_record_list(self):
        list_all = []

        # 根据时间区间计算时间戳
        end_date = datetime.datetime.strptime(self.str_time, "%Y%m%d%H%M%S")
        yesterday = end_date - datetime.timedelta(days=3)
        start_date = datetime.datetime.strptime(yesterday.date().strftime('%Y-%m-%d ') + '00:00:00',
                                                "%Y-%m-%d %H:%M:%S")

        print('开始下载{} 至 {}的金湾呼叫系统录音'.format(start_date, end_date))

        # 美团项目的ID为10
        sql_1 = "SELECT customer_id,caller, callee, FROM_UNIXTIME(start_time) as start_time, " \
                "FROM_UNIXTIME(answer_time) as end_time, record_file, type from tbl_cdr_voice_nature " \
                "WHERE FROM_UNIXTIME(start_time) >= '{}' and  FROM_UNIXTIME(start_time) <= '{}' " \
                "and record_file != '' and customer_id = 10".format(start_date, end_date)

        self.curs.execute(sql_1)  # 查询表
        call_list = self.curs.fetchall()
        print('搜索成功,录音数量：{}'.format(len(call_list)))
        for call in call_list:
            call = list(call)
            # print(call)
            # 对呼叫类型进行判断，
            if call[6] == 2:  # 如果是呼入，被叫号码是callee
                phone = call[1]
            else:
                phone = call[2]
            # 特殊的手机号码处理
            if len(phone) == 12 and phone[0:2] == '01':
                phone = phone[1:]

            date = call[3].strftime("%Y-%m-%d %H:%M:%S")
            date_d = call[3].strftime("%Y%m%d")

            file_path = os.path.join(r'\\10.10.100.211\record', call[5] + '.mp3').replace('/', '\\')  # # 原文件路径
            file_name = os.path.split(file_path)[1]

            d_path = os.path.join(self.down_path, date_d[0:6], date_d[6:8])
            d_file_path = os.path.join(d_path, file_name.replace('-', '_'))  # 归集文件路径
            # print(file_path)  # 原文件路径
            # print(d_file_path)  # 归集文件路径

            # 拷贝文件
            if not os.path.exists(d_path):
                os.makedirs(d_path)
            if not os.path.exists(d_file_path):
                shutil.copy(file_path, d_file_path)
                print('copy', d_file_path)
                record_index = [file_name.replace('-', '_'), date, phone, d_path, '金湾呼叫系统']
                list_all.append(record_index)
        self.curs.close()
        self.mysqldb.close()

        return list_all


# 下载度言的录音，已停用
class duyan_download:
    def __init__(self):
        self.str_time = ''
        self.download_path = ''  # 录音下载位置

        # 度言参数
        self.apikey_disk = {
            # '昆山分公司': 'WMZ9dYwlrlAckBKBxhxyG839hA0IBKhH',
            # '总部互金': '3Gd1bvKSLdDI5vYZrFugXKhmIR2FcH8O',
            # '微众前手': 'Ql0vz389GB5u55yMhBpevzmmYzcJNGtg',
            '南京分公司': '40DkT8jszHrBN5MgGGTKrtPAZN4xd8vz',
            # '总部浦发': '2JbsC8StZ1SXacJLzvndj1ZZuccRdom7'
            '美团项目': 'CJ4GNh6dpZ7nQghyMz71duQyFpHHAct6'
        }
        self.call_log_url = "https://open.duyansoft.com/api/v2/call_log"  # 通话记录列表
        self.recording_url = "https://open.duyansoft.com/api/v1/call/recording"  # 录音地址列表

    # 下载录音到本地
    def down_load(self, uuid, filepath, key):
        data = {"apikey": key,
                "call_uuid": uuid}
        head = {"Accept": "application/json, text/plain, */*"}
        r = requests.get(self.recording_url, params=data, headers=head)
        if r.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(r.content)
                f.close()
                print('get:', filepath)
        else:
            print('下载失败，错误代码{}'.format(r.status_code))
            return 0
        return 1

    # 根据日期获取通话详单数据
    def get_call_list(self, ye, key):
        # 根据时间区间计算时间戳
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        start_date = datetime.datetime.strptime(yesterday.date().strftime('%Y-%m-%d ') + '00:00:00',
                                                "%Y-%m-%d %H:%M:%S")
        end_date = datetime.datetime.strptime(self.str_time, "%Y%m%d%H%M%S")
        print('开始下载{} 至 {}的度言录音'.format(start_date, end_date))

        start_time = int(time.mktime(start_date.timetuple())) * 1000
        end_time = int(time.mktime(end_date.timetuple())) * 1000

        data = {"apikey": key,
                "page_num": ye,
                "page_size": 100,
                "start_time": start_time,
                "end_time": end_time}

        head = {"Accept": "application/json, text/plain, */*"}

        r = requests.get(self.call_log_url, params=data, headers=head).json()
        return r

    # 下载录音
    def run(self):
        dy_list_all = []

        for apikey in self.apikey_disk:
            apikey_value = self.apikey_disk[apikey]  # apikey
            #  获取总页数
            date_all = duyan_download.get_call_list(self, 1, apikey_value)
            # print(date_all)
            el1 = date_all['data']['total_elements']  # 通话数量总数
            el2 = date_all['data']['total_pages']  # 页数
            print('{},通话记录数量：{},总页数{}'.format(apikey, el1, el2))

            # 遍历通话记录，下载录音
            for el in range(1, el2 + 1):
                time.sleep(0.5)
                list_k = duyan_download.get_call_list(self, el, apikey_value)['data']['call_logs']  # 获取其中一页数据
                for gol in list_k:
                    time.sleep(0.5)
                    # print(gol)
                    if gol['outcome'] == 'SUCCESS':
                        # if gol['duration'] < 180 and gol['team'] != '雪娟接电':
                        #
                        gol_id = gol['call_uuid']  # 录音标识ID
                        gol_type = gol['type'].replace("BOUND", "")  # 呼叫类型
                        gol_caller = gol['caller']  # 主叫号码
                        gol_callee = gol['callee']  # 被叫号码
                        gol_time = int(gol['call_time'] / 1000)  # 呼叫时间
                        # team = gol['team']  # 团队
                        if gol_type == 'IN':  # 如果是呼入，调换被叫号码
                            phone = str(gol_caller).replace('-', '')
                        else:
                            phone = str(gol_callee).replace('-', '')
                        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(gol_time))
                        date_d = time.strftime("%Y%m%d%H%M%S", time.localtime(gol_time))

                        # 录音文件名称
                        file_name = "{}_{}_{}_{}.mp3".format(str(gol_type), str(gol_caller), str(gol_callee), date_d)
                        file_dir = os.path.join(self.download_path, date_d[0:6], date_d[6:8])
                        file_path = os.path.join(file_dir, file_name)  # 录音存放路径

                        if not os.path.exists(file_dir):
                            os.makedirs(file_dir)

                        if not os.path.exists(file_path):
                            if duyan_download.down_load(self, gol_id, file_path, apikey_value) == 1:
                                dy_list_all.append([file_name, date, phone, file_dir, 'duyan'])
                                time.sleep(0.5)
        return dy_list_all


# 下载联通的录音,已停用
class line_download:
    def __init__(self):
        self.str_time = ''
        self.down_path = None

        self.host = '10.10.100.81'
        self.port = 3306
        self.user = 'root'
        self.passwd = 'jinwan_88888'
        self.name = 'line_phone_record'
        self.datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.mysqldb = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.passwd,
                                       database=self.name)  # 打开数据库链接
        self.curs = self.mysqldb.cursor()

    # 查询联通的通话记录
    def select_line_list(self):
        list_all = []
        # 使用 strptime 将字符串转换为 datetime 对象
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        start_date = datetime.datetime.strptime(yesterday.date().strftime('%Y-%m-%d ') + '00:00:00',
                                                "%Y-%m-%d %H:%M:%S")
        end_date = datetime.datetime.strptime(self.str_time, "%Y%m%d%H%M%S")
        print('开始下载{} 至 {}的联通录音'.format(start_date, end_date))

        log_my_sql = ['10.10.100.81', 3306, 'line_phone_record', 'root', 'jinwan_88888']
        mysqldb = pymysql.connect(host=log_my_sql[0], port=log_my_sql[1], user=log_my_sql[3],
                                  password=log_my_sql[4], database=log_my_sql[2])  # 打开数据库链接
        curs = mysqldb.cursor()
        sql_1 = "select * from line_record_download_record_list where start_time >= '{}' and start_time < '{}'".format(
            start_date, end_date)
        curs.execute(sql_1)  # 查询表
        call_list = curs.fetchall()
        print('搜索成功,录音数量：{}'.format(len(call_list)))
        for call in call_list:
            call = list(call)
            date = call[4].strftime('%Y-%m-%d %H:%M:%S')
            date_s = call[4].strftime('%Y%m%d')
            if call[1] == 'OUT':
                phone = call[3]
            else:
                phone = call[2]
            filename = os.path.split(call[8])[1]

            d_path = os.path.join(self.down_path, date_s[0:6], date_s[6:8])  # 录音存放文件夹
            if not os.path.exists(d_path):
                os.makedirs(d_path)
            d_filepath = os.path.join(d_path, filename)  # 录音的路径

            # 拷贝录音到文件夹中
            if not os.path.exists(d_filepath):
                shutil.copy(call[8], d_filepath)
                print('copy:', d_filepath)
                record_index = [filename, date, phone, d_path, 'line']
                # print(record_index)
                list_all.append(record_index)

        return list_all


# 下载录音，将记录插入数据库
def record_download(date, download_path):
    record_list = []

    # 更新windows smb 凭据
    add_windows_credential()

    # 指掌易
    zzy = zhizhangyi_download()
    zzy.download_path = os.path.join(download_path, '指掌易')  # 录音存放位置
    zzy.str_time = date  # 定义时间参数
    record_list += zzy.record_down()

    # 度言
    # dy = duyan_download()
    # dy.download_path = os.path.join(download_path, r'度言')  # 录音存放位置
    # dy.str_time = date  # 定义时间参数
    # record_list += dy.run()

    # 枫软
    # fr = fengruan_download()
    # fr.down_path = os.path.join(download_path, r'枫软')  # 录音存放位置
    # fr.str_time = date  # 定义时间参数
    # record_list += fr.run()

    # VOIP
    voip = voip_download()
    voip.down_path = os.path.join(download_path, r'VOIP')  # 录音存放位置
    voip.str_time = date  # 定义时间参数
    record_list += voip.select_record_list()

    # 读取金湾呼叫系统的录音
    okcc = okcc_download()
    okcc.down_path = os.path.join(download_path, r'金湾呼叫系统')  # 录音存放位置
    okcc.str_time = date  # 定义时间参数
    record_list += okcc.select_record_list()

    # 读取联通固话录音
    # line = line_download()
    # line.down_path = os.path.join(download_path, r'联通')  # 录音存放位置
    # line.str_time = date
    # record_list += line.select_line_list()

    # 读取共享盘里面的录音
    shar = shar_records()
    shar.date = date
    record_list += shar.open_record()

    # 将记录插入数据库
    open_sql().logs(record_list)

    return record_list

