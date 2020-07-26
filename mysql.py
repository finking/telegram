import pymysql

class sql_db:
    def __init__(self, db_connect):
        try:
            self.conn = pymysql.connect(*db_connect, use_unicode=True, charset='utf8')
        except pymysql.OperationalError:
            print("can't find base")
        try:
            self.cursor = self.conn.cursor()
        except pymysql.OperationalError:
            print("can't get cursor")


    def select_all(self):
        try:
            self.cursor.execute("SELECT * FROM line_answer")
        except pymysql.Error:
            print("can't select line_answer")
        result = self.cursor.fetchall()
        if len(result) <= 0:
            return False
        else:
            data = {}
            for i in result:
                # ключ - id в бд, значение список из имени, фамилии и возраста
                data.update({i[0]:[i[1], i[2], i[3]]})
            return data


    def insert_user(self, name, surname, age):
        try:
            query = "INSERT INTO line_answer (name, surname, age) values (%s, %s, %s)"
            t = [name, surname, age]
            self.cursor.execute(query, t)
        except pymysql.Error:
            print("can't insert info in line_answer")
        self.conn.commit()