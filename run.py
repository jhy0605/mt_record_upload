from main_program import *
from record_download import *
import datetime


def main():
    # date = (datetime.datetime.strptime(str(input("请输入开始时间（格式：XXXX-XX-XX）默认下载开始时间-1天的录音")), '%Y-%m-%d')).strftime('%Y%m%d%H%M%S')
    date = (datetime.datetime.now() + datetime.timedelta(minutes=-30)).strftime('%Y%m%d%H%M%S')
    # data_path = r'D:\BaiduSyncdisk\python\develop\mt_record_upload'
    data_path = r'E:\mt_record_upload'
    download_path = r'\\10.10.100.203\recordings2\录音归集汇总\美团'

    # 下载录音
    record_download(date, download_path)

    # 录音匹配案件
    date_object = datetime.datetime.strptime(date, '%Y%m%d%H%M%S')  # 将字符串转换为datetime对象
    real_time_upload().mat_bank(date_object)

    # 上传录音
    UR = up_records()
    UR.data_path = data_path
    UR.str_time = date
    UR.run()  # 正常上传


# 打包命令：pyinstaller --name 'run直接运行' -F .\run.py .\db.py .\dingding_remind.py .\main_program.py .\record_download.py
if __name__ == '__main__':
    try:
        main()
    except Exception as k:
        Dingding_Warning('严重', '程序运行错误', str(k))

    # 运行监控，定时播报
    # try:
    #     status_check().run()
    # except Exception as k:
    #     Dingding_Warning('验证', '程序运行错误', str(k))

    # 非标准上传录音
    # UR = up_records()
    # UR.data_path = r'D:\BaiduSyncdisk\python\develop\mt_record_upload'
    # UR.str_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # UR.f_run()  # 非标准上传

    # 导出未匹配成功的录音
    # status_check().search_fail_record()
