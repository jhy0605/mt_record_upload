import pymysql
import datetime


# 数据库操作
class open_sql:
    def __init__(self):
        self.host = '10.10.100.81'
        self.port = 3306
        self.user = 'root'
        self.passwd = 'jinwan_88888'
        self.name = 'mt_record_upload'
        self.datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.mysqldb = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.passwd,
                                       database=self.name)  # 打开数据库链接
        self.curs = self.mysqldb.cursor()

    # 写入录音列表到数据库
    def logs(self, data_list):
        r = 0
        for data in data_list:
            sql_1 = "select count(*) from records where name = '{}'".format(data[0])
            self.curs.execute(sql_1)  # 执行sql语句
            fetchall = self.curs.fetchall()
            n = fetchall[0][0]
            if n == 0:
                sql_2 = "insert into records values(null, '{}', '{}', '{}', '{}', '{}', null, null, null , null)" \
                    .format(data[0], data[3].replace('\\', '\\\\'), data[1], data[2], data[4])
                # print(sql_2)
                self.curs.execute(sql_2)  # 执行sql语句
                r += 1
                self.mysqldb.commit()  # 提交修改（用于增、删、改）
        self.curs.close()  # 关闭游标对象
        self.mysqldb.close()  # 关闭链接
        print('写入数据：{}条'.format(r))

    # 查询未匹配案件的数据（case_id、mark为null的数据）
    def select_data(self, date):
        sql_1 = "select * from records where case_id is null and mark is null and date <= '{}'".format(date)
        # print(sql_1)
        self.curs.execute(sql_1)
        record_index_list = list(self.curs.fetchall())
        self.curs.close()  # 关闭游标对象
        self.mysqldb.close()  # 关闭链接
        return record_index_list

    # 查询需要上传的数据（case_id != null, upload_time为null）
    def select_up_data(self):
        sql_1 = "select * from records where case_id is not null and upload_time is null"
        # print(sql_1)
        self.curs.execute(sql_1)
        record_index_list = list(self.curs.fetchall())
        self.curs.close()  # 关闭游标对象
        self.mysqldb.close()  # 关闭链接
        return record_index_list

    # 根据ID修改数据库特定字段的值
    def update_table(self, field, value, id_value):
        sql_1 = "update records set {} = '{}' where id = {}".format(field, value, id_value)
        # print(sql_1)
        self.curs.execute(sql_1)  # 执行sql语句
        self.mysqldb.commit()  # 提交修改（用于增、删、改）
        self.curs.close()  # 关闭游标对象
        self.mysqldb.close()  # 关闭链接

    # 查询录音上传的成功率
    def select_success_rate(self, n):
        if n == 0:
            sql_1 = "SELECT count(*) as t from records WHERE date >= CURDATE() and date < DATE_ADD(CURDATE(), INTERVAL 1 DAY) " \
                    "UNION SELECT count(*) as t from records " \
                    "WHERE upload_time is not null and date >= CURDATE() and date < DATE_ADD(CURDATE(), INTERVAL 1 DAY);"

        elif n == 1:
            sql_1 = "SELECT count(*) as t from records WHERE date >= DATE_SUB(CURDATE(), INTERVAL 1 DAY) and date < CURDATE() " \
                    "UNION SELECT count(*) as t from records " \
                    "WHERE upload_time is not null and date >= DATE_SUB(CURDATE(), INTERVAL 1 DAY) and date < CURDATE();"
        else:
            sql_1 = ""
        self.curs.execute(sql_1)
        n_list = []
        for a in self.curs.fetchall():
            n_list.append(a[0])
        self.curs.close()  # 关闭游标对象
        self.mysqldb.close()  # 关闭链接
        return n_list
