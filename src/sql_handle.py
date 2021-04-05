import pymysql


def set_sql_connection():
    # return pymysql.connect(host='localhost', user='user1', password='QWErty123!', db='ldsp_mgr')
    return pymysql.connect(host='192.168.142.4', port=33060, user='user1', password='password', db='ldsp_mgr')


def db_names_get():
    connection = set_sql_connection()
    with connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * from locsia')
        rows = cursor.fetchall()
        names = [row[1] for row in rows]
    return names


def db_get(fields='*', val=''):
    connection = set_sql_connection()

    with connection:
        cursor = connection.cursor()
        string = f'select {fields} from locsia where name like "%{val}%" or tabN like "%{val}%" or ' \
                 f'passN like "%{val}%" or job like "%{val}%" or job2 like "%{val}%"'
        cursor.execute(string)
        res = cursor.fetchall()
    return res


def db_get_all_aways():
    connection = set_sql_connection()

    with connection:
        cursor = connection.cursor()
        string = f'select * from locsia_away;'
        cursor.execute(string)
        res = cursor.fetchall()
    return res


def db_add_short_days(s_days=[], h_days=[]):
    connection = set_sql_connection()

    s_data = date_format(s_days)
    h_data = date_format(h_days)

    cursor = connection.cursor()
    cursor.executemany('INSERT INTO colored_days(day, type) VALUES (%s, "BLUE")', s_data)
    cursor.executemany('INSERT INTO colored_days(day, type) VALUES (%s, "RED")', h_data)
    connection.commit()
    connection.close()


def db_del_days(days):
    connection = set_sql_connection()

    data = date_format(days)

    cursor = connection.cursor()
    cursor.executemany('DELETE FROM colored_days WHERE day = %s', data)
    connection.commit()
    connection.close()


def date_format(date):
    return ['-'.join(day.split('.')[::-1]) for day in date]


def db_read_colored_days(year, month):
    connection = set_sql_connection()

    cursor = connection.cursor()
    cursor.execute(f'select day from colored_days where (type like "BLUE" and day >= "{year}-{month}-01" and '
                   f'day <= DATE_ADD("{year}-{month}-01", INTERVAL 1 MONTH))')
    blue = cursor.fetchall()
    cursor.execute(f'select day from colored_days where (type like "RED" and day >= "{year}-{month}-01" and '
                   f'day <= DATE_ADD("{year}-{month}-01", INTERVAL 1 MONTH))')
    red = cursor.fetchall()
    res_red = [int(date[0].strftime("%d")) for date in red]
    res_blue = [int(date[0].strftime("%d")) for date in blue]
    connection.close()
    return res_red, res_blue


def db_read_aways(year, month):
    connection = set_sql_connection()

    cursor = connection.cursor()
    cursor.execute(f'select name, type, date1, date2 from locsia_away where (date2 >= "{year}-{month}-01" and '
                   f'date1 <= DATE_ADD("{year}-{month}-01", INTERVAL 1 MONTH))')
    res = cursor.fetchall()
    connection.close()
    return res


if __name__ == '__main__':
    # aways = db_read_aways(2021, 2)
    # for away in aways:
    #     print(away)
    # conn = set_sql_con_samba()
    # print(conn)
    pass
