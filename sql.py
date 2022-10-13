import mysql.connector
from mysql.connector import Error

class SQL():
    def __init__(self):
        self.user_base = 'root'
        self.password = 'root'
        self.port = '3306'
        self.host = 'localhost'
        self.database = 'bot'
        self.table = 'telegram'

    def connector(self):
        #Подключение к БД
        config = {
            'user':self.user_base,
            'password':self.password,
            'host':self.host,
            'database':self.database
        }
        connection = None
        try:
            connection = mysql.connector.connect(**config)
        except Error as e:
            print('Error:' + e)
        return connection

    def request(self, connection, user_id):
        #Выгрузка данных клиента
        cursor = connection.cursor()
        result = None
        text = f'SELECT * FROM {self.table} WHERE id_telegram = {user_id}'
        try:
            cursor.execute(text)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(e)

    def add_sql(self, user_id,user_name, connection):
        #Добавление нового клиента
        cursor = connection.cursor()
        request = f"INSERT INTO {self.table} VALUES ({user_id}, '{user_name}', 0)"
        try:
            cursor.execute(request)
            connection.commit()
            print('Данные успешно добавлены')
        except Error as e:
            print(f'Error {e}')
#сделать сложение и добавление через питоновский код
    #позже сделать пополнение черехз базу данных sql через запрос
    def replenishment_balance(self,user_info,sum_replenishment, connection):
        # Пополнение баланса клиента
        user= user_info[0]#получаем кортеж
        user_id = user[0]#Номер id
        cursor = connection.cursor()
        request = f"UPDATE {self.table} SET balance=(balance+{sum_replenishment}) WHERE id_telegram = {user_id}"
        try:
            cursor.execute(request)
            connection.commit()
        except Error as e:
            print(e)
    def decrease_balance(self,user_info,sum_decrease, connection):
        # Уменьшение баланса клиента
        user= user_info[0]#получаем кортеж
        user_id = user[0]#Номер id
        balance = int(user[2])#Узнаем баланс
        new_balance = balance - int(sum_decrease)
        if new_balance >= 0:  #Проверяем, при уменьшении будет отрицательный баланс или нет
            cursor = connection.cursor()
            request = f"UPDATE {self.table} SET balance=(balance-{sum_decrease}) WHERE id_telegram = {user_id}"
            try:
                cursor.execute(request)
                connection.commit()
            except Error as e:
                print(e)
        else:
            return None
    def add_commentar(self, user_id, user_name, commentar, connection):
        #Добавление комментария пользователя
        cursor = connection.cursor()
        request = f"INSERT INTO commentar VALUES ({user_id}, '{user_name}', '{commentar}')"
        try:
            cursor.execute(request)
            connection.commit()
        except Error as e:
            print(f"Commentar Error: {e}")
    def unloading_commentar(self, connection):
        #Выгрузка комментариев
        cursor = connection.cursor()
        request = 'SELECT * FROM commentar'
        result = None
        try:
            cursor.execute(request)
            result = cursor.fetchall()
            return result[0]
        except Error as e:
            print(f"Commentar Error: {e}")

    def balance(self, user_id, connection):
        #Возращает баланс пользователя
        balance = self.request(connection, user_id)
        balance = balance[0]
        return balance[2]















