import pymysql
from sql_config import host, user, password, db_name, port

def removeChar(word1, letter1):
    new_string = ''
    for letter in word1:
        if (letter != letter1):
            new_string += letter
    return new_string

def tuple_to_str_query(t , start_and_end_of_word = ""):
    types_query = ""
    len_types = len(t)

    for i in range(len_types - 1):
        types_query += start_and_end_of_word
        types_query += str(t[i])
        types_query += start_and_end_of_word
        types_query += ","

    types_query += start_and_end_of_word
    types_query += str(t[len_types - 1])
    types_query += start_and_end_of_word

    return types_query



# noinspection PyUnusedLocal
class Database:
    def __init__(self):
        print("Try to connect to database")

        try:
            self.connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor
            )
            print('Success!')

        except Exception as ex:
            print("Connection refused...")
            print(ex)


    def create_table(self , name , types):

        types_query = tuple_to_str_query(types)

        ex = "(id int AUTO_INCREMENT , question varchar(200) NOT " \
                                 "NULL , right_answer varchar(200) NOT NULL , false_answer varchar(200) NOT NULL ," \
                                 "PRIMARY KEY (id));"
        print(ex)
        print("\n\n")

        print(types_query)
        with self.connection.cursor() as cursor:


            create_table_query = "CREATE TABLE `{0}`({1}) ".format(name , types_query)

            cursor.execute(create_table_query)

    def select_table(self , name ,column = "*"):
        with self.connection.cursor() as cursor:
            select_all_rows = "SELECT {1} FROM `{0}`".format(name , column)
            cursor.execute(select_all_rows)
            # cursor.execute("SELECT * FROM `users`")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            print("#" * 20)
            return rows

    def add_data(self , name ,values ,  is_id_default = True):
        with self.connection.cursor() as cursor:

            print("\n\n")
            rows = self.select_table(name)
            print(rows)


            key_columns_list = (list(rows[0].keys()))
            if is_id_default:
                key_columns_list.pop(0)

            key_columns_tuple = tuple(key_columns_list)

            key_columns_str = tuple_to_str_query(key_columns_tuple)

            print(key_columns_str)

            values_str = tuple_to_str_query(values , "'")
            print(values_str)
            insert_query = "INSERT INTO `{0}` ({1}) VALUES ({2});".format(name , key_columns_str  , values_str)
            cursor.execute(insert_query)
            self.connection.commit()

    def update_data(self , name ,column_set , value_set , column_condition ,value_condition ):
        with self.connection.cursor() as cursor:
            update_query = "UPDATE `{0}` SET {1} = '{2}' WHERE {3} = '{4}';".format(name ,column_set , value_set , column_condition ,value_condition)
            cursor.execute(update_query)
            self.connection.commit()

a = Database()
name = "a_11"

types = ("id int AUTO_INCREMENT", "name_of_test varchar(250) NOT NUll", "password varchar(250) NOT NUll" , "PRIMARY KEY (id)")

values = ('easy', '1234567890')

a.update_data(name ,"password" , "000" , "name_of_test" , "easy")