import pymysql

from sql_w import sql_config


def removeChar(word1, letter1):
    new_string = ''
    for letter in word1:
        if (letter != letter1):
            new_string += letter
    return new_string


def tuple_to_str_query(t, start_and_end_of_word=""):
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
                host=sql_config.host,
                port=sql_config.port,
                user=sql_config.user,
                password=sql_config.password,
                database=sql_config.db_name,
                cursorclass=pymysql.cursors.DictCursor
            )
            print('Success!')

        except Exception as ex:
            print("Connection refused...")
            print(ex)

    def create_table(self, name, types):

        types_query = tuple_to_str_query(types)


        with self.connection.cursor() as cursor:
            create_table_query = "CREATE TABLE if not exists `{0}`({1}) ".format(name, types_query)

            cursor.execute(create_table_query)

    def select_table(self, name, column="*" , column_condition = "", value_condition = ""):
        with self.connection.cursor() as cursor:

            if column_condition != "" or value_condition != "":
                select_all_rows = "SELECT {1} FROM `{0}` WHERE {2} = '{3}';".format(name, column , column_condition ,value_condition )
            else:
                select_all_rows = "SELECT {1} FROM `{0}`".format(name,column)

            cursor.execute(select_all_rows)
            # cursor.execute("SELECT * FROM `users`")
            rows = cursor.fetchall()
            # for row in rows:
            #     print(row)
            # print("#" * 20)
            return rows

    def add_data(self, name, values, columns = [],  is_id_default=False):
        with self.connection.cursor() as cursor:
            # print("\n\n")
            if columns == []:
                rows = self.select_table(name)
                # print(rows)
                key_columns_list = (list(rows[0].keys()))
                print(key_columns_list)
            else:
                key_columns_list = columns
                print(key_columns_list)


            if is_id_default:
                key_columns_list.pop(0)


            key_columns_tuple = tuple(key_columns_list)

            key_columns_str = tuple_to_str_query(key_columns_tuple)

            # print(key_columns_str)

            values_str = tuple_to_str_query(values, "'")
            # print(values_str)
            insert_query = "INSERT INTO `{0}` ({1}) VALUES ({2});".format(name, key_columns_str, values_str)
            cursor.execute(insert_query)
            self.connection.commit()

    def update_data(self, name, column_set, value_set, column_condition, value_condition):
        with self.connection.cursor() as cursor:
            update_query = "UPDATE `{0}` SET {1} = '{2}' WHERE {3} = '{4}';".format(name, column_set, value_set,
                                                                                    column_condition, value_condition)
            cursor.execute(update_query)
            self.connection.commit()

    def user_select_query(self, query:str):
        with self.connection.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()

            return rows

#
if __name__ == "__main__":


    # id_teacher_query = Database().user_select_query('''select id_teacher from teachers where login = "vdf"''')[0]["id_teacher"]
    # print(id_teacher_query)

    a = Database()

    id_teacher_query = a.user_select_query( ''' select count(*) from quizzes where id_tests = '{0}' '''.format(int(14)))[0]["count(*)"]



    print(id_teacher_query)

    # quizzes_query =  Database().user_select_query(
    #     ''' select * from quizzes where id_tests =  '{0}' '''.format(14))
    #
    # print(quizzes_query)
    #
    # # quizzes_query = a.user_select_query(''' select * from quizzes where id_tests =  '{0}' '''.format(id_teacher_query))
    #
    # for i in quizzes_query:
    #     options = i["options"].split(";;;")
    #     print(i["chat_id"], i["question"],
    #                          options,
    #                         i["correct_option_id"])

    # tests = []
    # for i in tests_teacher_query:
    #     tests.append(i["name"])
    # print(tests)




    # my_quiz = await bot.send_poll(chat_id=quizzes_database[str(message.from_user.id)][0].chat_id, question=message.poll.question,
    #                     is_anonymous=False, options=tuple_list, type="quiz",
    #                     correct_option_id=message.poll.correct_option_id)

    # name = "students"
    #
    # types = (
    #     "id_quiz varchar(50)", "chat_id int NOT NUll", "question varchar(223) NOT NUll","options varchar(1000) NOT NUll", "correct_option_id int NOT NUll","id_tests int NOT NUll","FOREIGN KEY(id_tests) REFERENCES tests(id_test)" , "PRIMARY KEY(id_quiz)"
    #
    # )
    #
    # a.create_table(name, types)


    # name = "students"
    #
    # types = (
    #     "id_student int AUTO_INCREMENT", "name varchar(50) NOT NUll", "id_tests int NOT NUll", "count_right_answers int NOT NUll","FOREIGN KEY(id_tests) REFERENCES tests(id_test)" , "PRIMARY KEY(id_student)"
    #
    # )
    #
    # a.create_table(name, types)

    # types = (
    #  "id_polls int AUTO_INCREMENT", "question varchar(250) NOT NUll", "options nvarchar(250) NOT NUll", "id_main int NOT NUll" , "PRIMARY KEY(id_polls)" , "FOREIGN KEY(id_main) REFERENCES main(id)")
    #
    #
    # types = (
    #     "id_teacher int", "login varchar(50) NOT NUll", "password varchar(52) NOT NUll", "pin_cod varchar(52) NOT NUll", "PRIMARY KEY(id_teacher)"
    # )

    # name = "tests"
    #
    # types = (
    #     "id_test int AUTO_INCREMENT", "name varchar(50) NOT NUll", "id_teachers int NOT NUll","PRIMARY KEY(id_test)", "FOREIGN KEY(id_teachers) REFERENCES teachers(id_teacher)"
    # )
    # a.create_table(name, types)
    #
    # name = "tests"

    # types = (
    #  "id_polls int AUTO_INCREMENT", "question varchar(250) NOT NUll", "options nvarchar(250) NOT NUll", "id_main int NOT NUll" , "PRIMARY KEY(id_polls)" , "FOREIGN KEY(id_main) REFERENCES main(id)")
    #
    #
    # types = (
    #     "id_test int AUTO_INCREMENT", "name varchar(50) NOT NUll", "id_teachers int NOT NUll","PRIMARY KEY(id_test)", "FOREIGN KEY(id_teachers) REFERENCES teachers(id_teacher)"
    # )
    # a.create_table(name, types)
    #



    #





    # a.add_data("movieprofile", values=(8844, 'Jumanji' , 0,'Adventure, Fantasy, Family, ') , is_id_default=False)
    # a.add_data("main", values= ("admin" , "admin"))
    #
    # count = 0
    # errors_lines = []
    # for i in MovieProfile:
    #
    #     # print(values)
    #     try:
    #         values_to_add = list(i.values())
    #         values = (int(values_to_add[0]), str(values_to_add[1]), float(values_to_add[2]), values_to_add[3])
    #         count += 1
    #         a.add_data("movieprofile", values=values, is_id_default=False)
    #     except:
    #         errors_lines.append(i)
    #         print(count)
    #
    #
    # print(errors_lines)
