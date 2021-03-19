import sys
import pandas as pd
import time
from SQLer import sqler
# 控制器
"""
作业上交情况检查器；
功能：自动生成每次学生上交作业的情况，检查漏交学生，返回姓名，所有数据储存在数据库中
使用工具：python + mysql
使用库：pandas pymysql
"""


def merge(table1, table2):
    data1 = pd.read_excel(table1)
    data2 = pd.read_excel(table2)
    names1, names2 = set(data1['姓名'].to_list()), set(data2['姓名'].to_list())
    class_name = list(names1 & names2)
    ## d打印这个班级在这个大班里共有多少人
    print(len(class_name))
    ## 将这些人加入数据库
    ### 创建数据库对象
    info = {
        "host":"localhost",
        "user":"root",
        "password":"haizeiwang",
        "charset":"utf8"
    }
    sql = sqler(info)
    ### 创建数据库HOMEWORK
    database_name = "HOMEWORK"
    sql.create_database(database_name)

    ### 创建数据表 Students
    table_name = "students"
    fields = """CREATE TABLE students (
                id INT AUTO_INCREMENT ,
                SNAME char(50) NULL ,
                PRIMARY KEY (`id`)  
    )"""
    sql.create_table(table_name,fields)

    ### 插入数据
    insert_sql = """INSERT INTO students(SNAME) VALUES ('%s')"""
    for i in class_name:
        sql.insert_data(insert_sql,i)


    pass


def file_name(path):
    import os
    return os.listdir(path)


def check(path):
    # 用数据库去in文件名，找到一个立即break，在对应长度的0列表下表填上1，最后将列表以新的字段加入表中
    ### 创建数据库对象
    info = {
        "host": "localhost",
        "user": "root",
        "password": "haizeiwang",
        "charset": "utf8"
    }
    sql = sqler(info)
    ### 创建数据库HOMEWORK
    database_name = "HOMEWORK"
    table_name = "students"
    sql.info['db'] = database_name
    sql.table_name = table_name
    query_lis = sql.query()
    is_lis = [0 for i in range(len(query_lis))]
    lis_weijiao = []
    ### 获得目录下文件列表
    file_list = file_name(path)
    ### 控制从数据库中查询出的列表的循环
    for i,j in enumerate(query_lis):
        ### 控制文件名的循环
        for k in file_list:
            if j[1] in k:
                ### 检查到一个文件里有名字就跳出，判断下一个名字
                is_lis[i] = 1
                break
    ### 将未交的名字找出来
    for i,j in enumerate(is_lis):
        if j != 1:
            lis_weijiao.append(query_lis[i])
    ### 统计未交的人数
    num = len(lis_weijiao)
    ### 返回未交人数，未交名字清单，要插入的0-1列表
    return (num,lis_weijiao,is_lis)

    pass


def update_table(path, times):
    num,lis_weijiao,lis_toinsert = check(path)
    ### 链接数据库
    info = {
        "host": "localhost",
        "user": "root",
        "password": "haizeiwang",
        "charset": "utf8"
    }
    sql = sqler(info)
    ### 创建数据库HOMEWORK
    database_name = "HOMEWORK"
    table_name = "students"
    sql.info['db'] = database_name
    sql.table_name = table_name
    ### 向数据库增加新字段
    sql.add_new_field(times,"TINYINT","null")
    ### 向该字段更新数据
    for i,j in enumerate(lis_toinsert):
        sql.update_data(times,j,i+1)

if __name__ == '__main__':
    ## 获取参数
    """
    --merge: 合并大班表以及小班表，后面必须跟大班与小班名字文件
    --check：返回未交学生姓名，人数，后面跟当前作业收集文件夹
    --update: 将本次作业收集情况加入数据库
    """
    try:
        str_list = sys.argv[1:]
        # str_list = ["--merge","./18大数据1班花名册.xlsx","./A1214025机器学习111人.xls"]
        # str_list = ["--check", "E:\机器学习作业\第一次"]
        # str_list = ["--update", "E:\机器学习作业\第一次", "第一次"]
        print(str_list)
        if str_list[0] == "--merge":
            print("正在合并数据表...")
            table1, table2 = str_list[1],str_list[2]
            merge(table1,table2)
            print("数据表合并完成！")
        elif str_list[0] == "--check":
            print("正在检查未交人员...")
            path = str_list[1]
            num,lis_weijiao,lis_toinsert = check(path)
            print("\n未交人数:{}\n人员名单:{}".format(num,lis_weijiao))
            print("\n检查完毕！")
        elif str_list[0] == "--update":
            print("正在更新数据库")
            path = str_list[1]
            times = str_list[2]
            update_table(path,times)
            print("数据库更新完毕！")
        else:
            print("请输入有效参数！")
    except ValueError:
        print("请输有效参数,或者在执行update前先check")