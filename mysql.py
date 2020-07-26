import pymysql

class sql_db:
    def __init__(self, host, user, password, db):
        try:
            self.conn = pymysql.connect(host, user, password, db, use_unicode=True, charset='utf8')
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
                data.update({i[1]:i[2]})
            return data


    def insert_user(self, name, surname, age):
        try:
            query = "INSERT INTO line_answer (name, surname, age) values (%s, %s, %s)"
            t = [name, surname, age]
            self.cursor.execute(query, t)
        except pymysql.Error:
            print("can't insert info in line_answer")
        self.conn.commit()


def main():
    sql = sql_db()
    # print(sql.select_all())
    # b = sql.select_all()
    # print(b.keys())
    # if 'ETC1' in b.keys():
        # print('da')


if __name__ == "__main__":
    main()