import pymysql


class sqler:
    def __init__(self, info=None):
        if info != None:
            self.info = info
        else:
            self.info = {
                "host": "localhost",
                "user": "root",
                "password": "*******",
                "db": "TESTDB",
                "charset": "utf8"  # 一定要加上负责中文无法显示
            }

    def create_table(self, name, fields):
        self.table_name = name
        # 打开数据库链接
        db = pymysql.connect(**self.info)
        # 创建游标对象
        cursor = db.cursor()
        # 使用 execute() 方法执行 SQL，如果表存在则删除
        cursor.execute("DROP TABLE IF EXISTS {}".format(self.table_name))

        # 使用预处理语句创建表
        cursor.execute(fields)

        # 关闭数据库连接
        db.close()

    def insert_data(self, fields, content=None):
        # 链接数据库
        db = pymysql.connect(**self.info)
        # 创建游标对象
        cursor = db.cursor()
        # SQL 插入语句
        if isinstance(content,list):
            sql = fields % tuple(content)
        else:
            sql = fields % content
        cursor.execute(sql)
        db.commit()
        # try:
        #     # 执行sql语句
        #     cursor.execute(sql)
        #     # 提交到数据库执行,这一部很重要
        #     db.commit()
        # except:
        #     # 如果发生错误则回滚
        #     db.rollback()

        # 关闭数据库连接
        db.close()
    def query(self,filed=None):
        # 链接数据库
        db = pymysql.connect(**self.info)
        # 创建游标对象
        cursor = db.cursor()
        # SQL查询语句
        sql = "SELECT * FROM {}".format(self.table_name)
        # 执行sql语句
        try:
            cursor.execute(sql)
            res = cursor.fetchall()
            snames =res
        except:
            print("Error: cant fetch the data")
        else:
            return snames
        # 关闭数据库连接
        db.close()

    def create_database(self, database_name):
        self.database_name = database_name
        # 打开数据库链接
        db = pymysql.connect(**self.info)
        # 创建游标对象
        cursor = db.cursor()
        # 使用 execute() 方法执行 SQL，如果表存在则删除
        cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(self.database_name))
        # 关闭数据库连接
        db.close()
        # 增加self.info数据库信息
        self.info["db"] = self.database_name
        pass

    def add_new_field(self, param1,param2,param3):
        # 打开链接
        db = pymysql.connect(**self.info)
        # 创建游标对象
        cursor = db.cursor()
        # 执行语句
        try:
            sql_statement = "alter table students add  "+param1 + " " + param2 + " " + param3 + ";"
            cursor.execute(sql_statement)
        except:
            print("SQL语句出现问题，或者该字段在表中已经存在")
        # 关闭链接
        db.close()

    def update_data(self,field, value, value_id):
        # 打开链接
        db = pymysql.connect(**self.info)
        # 获得光标
        cursor = db.cursor()
        # SQL 查询语句
        sql = "update %s set %s=%d WHERE id = %d" % (self.table_name, field, value, value_id)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            error = "Error: unable to fetch data"
            print(error)

        # 关闭数据库连接
        db.close()
