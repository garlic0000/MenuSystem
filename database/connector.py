import pymysql


class Connector:
    # 初始化
    connection = None
    cursor = None

    def __init__(self):
        self.userName = 'root'
        self.password = 'root3306'
        self.databaseName = 'menu_db'
        self.port = 3306
        try:
            # 创建连接
            Connector.connection = pymysql.connect(host='localhost',
                                                   user=self.userName,
                                                   password=self.password,
                                                   database=self.databaseName,
                                                   port=self.port)
            # 获取当前游标
            Connector.cursor = Connector.connection.cursor()
        except:
            print("数据库配置错误")
            return

    @staticmethod
    def get_cursor():
        # 获取当前游标
        if Connector.connection is not None:
            Connector.connection.commit()
            Connector.cursor.close()
            Connector.connection.close()
        Connector()
        return Connector.cursor

    @staticmethod
    def get_connection():
        # 获取数据库连接
        if Connector.connection is not None:
            Connector.connection.commit()
            Connector.cursor.close()
            Connector.connection.close()
        Connector()
        return Connector.connection

    @staticmethod
    def close_connection():
        # 关闭数据库连接
        if Connector.cursor is not None:
            Connector.connection.close()
        Connector.connection = None
        Connector.cursor = None
