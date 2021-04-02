import calendar
import os, sys, subprocess
import re
from datetime import datetime, timedelta
from tkinter import END

from consts import *
from sql_handle import db_names_get, db_get, db_read_colored_days, db_read_aways

import http.client
import socket



def normalize(string: str):
    res = string
    res = res.replace(' ', '')
    res = res.replace('\n', '')
    res = res.replace('\t', '')
    res = res.replace(',', '.')
    res = res.replace(':', '.')
    res = res.replace('по', '-')

    if re.search('-', res):
        str_type = 2
    else:
        str_type = 1

    if str_type == 2:
        temp = res.split('-')
        if len(temp[0].split('.')) == 1:
            temp[0] += '.00'

        if len(temp[1].split('.')) == 1:
            temp[1] += '.00'

        res = f'{temp[0]}-{temp[1]}'

    print(f'string = {string} res = {res} ')
    return res


def hhmm_to_float(hhmm: str):
    hhmm_split = hhmm.split('.')
    minutes = int(hhmm_split[1])
    if minutes == 0:
        return float(hhmm_split[0])
    elif minutes <= 15:
        return float(hhmm_split[0]) + 0.25
    elif minutes <= 30:
        return float(hhmm_split[0]) + 0.5
    elif minutes <= 45:
        return float(hhmm_split[0]) + 0.75
    else:
        return int(hhmm_split[0]) + 1


def f_to_nice_str(f: float):
    if float(f).is_integer():
        res = str(int(f))
    elif float(f * 2).is_integer():
        res = f'{f:.1f}'
    else:
        res = f'{f:.2f}'
    return res


def datatime_to_str(dt = datetime.timedelta(hours=0)):
    hours = dt.seconds//3600
    minutes = (dt.seconds//60)%60
    if minutes == 00:
        res = f'{hours}'
    elif minutes == 30:
        res = f'{hours}.5'
    else:
        minutes = round(minutes/60*100)
        res = f'{hours}.{minutes}'
    return res


def calc_overlap(aw_start, aw_end, d_start, d_end):
    aw_start = datetime.timedelta(hours=aw_start.hour, minutes=aw_start.minute)
    aw_end = datetime.timedelta(hours=aw_end.hour, minutes=aw_end.minute)
    if aw_start <= d_end and aw_end >= d_start:
        return max(aw_end, d_end) - min(aw_start, d_start) - (d_end - d_start)
    else:
        return aw_end - aw_start


def calc_hours(calc_name: str, day_type: int, calc_date: str, aways):
    """
    return number of hours for current date
    :param calc_name: name of current person
    :param day_type: norm/short/saturday
    :param calc_date: string dd.mm.YYYY
    :param aways: list of aways
    :return: str
    """

    if day_type == DAY_NORM:
        res = WORK_END - WORK_START  # res = 9
    elif day_type == DAY_SHORT:
        res = WORK_END_SHORT - WORK_START  # res = 8
    else:
        res = WORK_END_SAT - WORK_START

    dinner_time = (DINNER_END - DINNER_START)
    res -= dinner_time

    calc_date = datetime.datetime.strptime(calc_date, '%d.%m.%Y')
    res_str = ''

    if aways == ():
        pass
    else:
        for away in aways:
            if away[AWAY_NAME_POS] == calc_name:
                if away[AWAY_TYPE_POS] == AWAY_TYPE_ADMIN:
                    if away[AWAY_DATE1_POS].day == calc_date.day:
                        res -= calc_overlap(away[AWAY_DATE1_POS], away[AWAY_DATE2_POS], DINNER_START, DINNER_END)
                    if res == datetime.timedelta(hours=0):
                        res_str = 'A'
                elif away[AWAY_TYPE_POS] == AWAY_TYPE_OTPUSK:
                    if away[AWAY_DATE1_POS] <= calc_date <= away[AWAY_DATE2_POS]:
                        res_str = 'O'
                elif away[AWAY_TYPE_POS] == AWAY_TYPE_HOSP:
                    if away[AWAY_DATE1_POS] <= calc_date <= away[AWAY_DATE2_POS]:
                        res_str = 'Б'
                else: # away[AWAY_TYPE_POS] == AWAY_TYPE_OTGUL:
                    pass

    if res_str not in ['A', 'O', 'Б', 'А', 'О']:
        res_str = datatime_to_str(res)

    return res_str


def date_analysis(date: str):
    tdate = date.replace('\n', '')
    if len(tdate) <= 10:  # BAD CONDITION
        return DATE_TYPE_SINGLE
    else:
        date_split_sp = tdate.split(' ')
        if len(date_split_sp) > 1:
            return DATE_TYPE_DATE_PLUS_TIME_INTERVAL
    return DATE_TYPE_DATE_INTERVAL


def fill_person_listbox(listbox):
    # f = open(BASE_PATH, 'r')
    names = db_names_get()
    for name in names:
        listbox.insert(END, f'{name}')


def make_report():
    pass
    # report_type = away_doc_type.get()
    # with open(BASE_PATH, 'r') as db:
    #     db_lines = db.readlines()
    # db.close()
    # person = []
    # for db_line in db_lines:
    #     person.append(db_line.split(', '))
    #
    # cur = person_listbox.curselection()
    # date_away1 = entry_away_date1.get()
    # date_away2 = entry_away_date2.get()
    # date_away1 = normalize(date_away1)
    # date_away2 = normalize(date_away2)
    # cur_person = person[cur[0]]  # cur (2,), cur[0] = 2
    # if report_type != REPORT_TYPE_HOSPITAL:
    #     with open(NEW_REPORT_PATH, 'w') as f:
    #         f.write('<div id = "m_text">' + '\n')
    #         f.write('\t' + '<table id = "m_text">' + '\n')
    #         f.write('\t\t' + '<tr>' + '\n')
    #         f.write('\t\t\t' + '<td width=450></td>' + '\n')  # empty cell
    #         f.write('\t\t\t' + '<td>Главному конструктору<br>Начальнику ОКБ<br>Воронцову В.А.<br>\n')
    #         f.write('\t\t\t\t' + f'от {cur_person[BASE_JOB1_POS]} {cur_person[BASE_LAB_POS]}<br>\n')  # speciality
    #         f.write('\t\t\t\t' + f'{cur_person[BASE_NAME1_POS]}<br>\n')  # last name + initials
    #         f.write('\t\t\t\t' + f'таб. №{cur_person[BASE_TABLE_NUM_POS]}<br>\n')  # table number
    #         f.write('\t\t\t\t' + f'пропуск № {cur_person[BASE_PASS_NUM_POS]}<br>\n')  # pass number
    #         f.write('\t\t\t\t' + f'тел. 26-40<br>\n')  # laboratory telephone number
    #         f.write('\t\t\t' + '</td>' + '\n')
    #         f.write('\t\t' + '</tr>' + '\n')
    #         f.write('\t' + '</table>' + '\n')
    #         f.write('\t<p id = "z">Заявление</p>\n')
    #         if date_away2 == '':
    #             away_string = f'{date_away1} г.'
    #             report_date = date_away1
    #         else:
    #             match = re.search('-', date_away2)
    #             if match:
    #                 date_away2_split = date_away2.split('-')
    #                 away_string = f'{date_away1} г. с {date_away2_split[0]} по {date_away2_split[1]}'
    #                 report_date = f'{date_away1} {date_away2_split[0]}-{date_away2_split[1]}'
    #             else:
    #                 away_string = f'с {date_away1} г. по {date_away2} г.'
    #                 report_date = f'{date_away1}-{date_away2}'
    #
    #         if report_type == REPORT_TYPE_ADMIN:
    #             away_reason = f'Прошу предоставить мне отпуск без сохранения заработной платы {away_string}' \
    #                           f' по семейным обстоятельствам.'
    #             report_type_record = 'ADMIN'
    #             status_page1['text'] = 'заявка на административный отпуск оформлена!'
    #         elif report_type == REPORT_TYPE_OTGUL:
    #             away_reason = f'Прошу предоставить мне отгул {away_string} за заранее отработанное время'
    #             report_type_record = 'OTGUL'
    #             status_page1['text'] = 'заявка на отгул оформлена!'
    #         elif report_type == REPORT_TYPE_OTPUSK_FULL:
    #             away_reason = f'Прошу предоставить очередной отпуск за {datetime.now().year} г. {away_string}'
    #             report_type_record = 'OTPUSK'
    #             status_page1['text'] = 'заявка отпуск оформлена!'
    #
    #         f.write(f'\t<p style="white-space: pre-wrap;">\t{away_reason}</p>\n')
    #         f.write('</div>\n')
    #
    #         f.write('<style>\n')
    #         f.write('\t #z { text-align: center }\n')
    #         f.write('\t #m_text { font: 16px sans-serif}\n')
    #         f.write('</style>\n')
    #     f.close()
    #     os.startfile(NEW_REPORT_PATH, "open")
    # elif report_type == REPORT_TYPE_HOSPITAL:
    #     report_type_record = 'HOSP'
    #     report_date = f'{date_away1}-{date_away2}'
    #     status_page1['text'] = 'информация о больничном принята'
    #
    # make_report_record(cur_person[BASE_NAME_POS], report_type_record, report_date)


def make_report_record(name, rep_type, rep_date):
    pass
    # with open(REPORTS_PATH, 'a') as rep:
    #     rep.write(f'{name}, {rep_type}, {rep_date}\n')
    # rep.close()


def make_table_subtitle(table_date: str, aways):
    s = ''
    for away in aways:
        if away[AWAY_TYPE_POS] == AWAY_TYPE_HOSP:
            s1 = away[AWAY_DATE1_POS].strftime("%d.%m.%Y")
            s2 = away[AWAY_DATE2_POS].strftime("%d.%m.%Y")
            s += f'Б - больничный - {away[AWAY_NAME_POS]} {s1} - {s2}\n'
    for away in aways:
        if away[AWAY_TYPE_POS] == AWAY_TYPE_OTPUSK:
            s1 = away[AWAY_DATE1_POS].strftime("%d.%m.%Y")
            s2 = away[AWAY_DATE2_POS].strftime("%d.%m.%Y")
            s += f'О - отпуск - {away[AWAY_NAME_POS]} {s1} - {s2}\n'
    return s


def make_table(table_date_entry, table_type='TABLE_TYPE_FULL'):
    str_month = ('', 'январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сенябрь',
                 'октябрь', 'ноябрь', 'декабрь')
    str_month2 = ('', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сенября',
                  'октября', 'ноября', 'декабря')

    person = db_get()

    table_date = table_date_entry.get()
    table_date_split = str(table_date).split('.')
    table_year = int(table_date_split[1])
    table_month = int(table_date_split[0])

    aways = db_read_aways(table_year, table_month)
    for away in aways:
        print(away)
    holidays, short_days = db_read_colored_days(table_year, table_month)

    html = ''
    html += '<div>\n\t<p>График выходов на работу<br>\n'
    html += f'\t<p>работников ОКБ отдела ЦОС лаборатории ЛОЦСиА за {str_month[table_month]} {table_year}<br>\n'
    if table_type == TABLE_TYPE_HALF:
        html += f'\t<p style="white-space: pre-wrap;">\t\t\t\t\tI период {str_month2[table_month]} {table_year}' \
                f'года <br></p>\n'
    else:  # TABLE_TYPE_FULL
        html += f'\t<p style="white-space: pre-wrap;">\t\t\t\t\tI период {str_month2[table_month]} {table_year} ' \
                f'года\t\t\t\t\t\t\t\t\t\t II период {str_month2[table_month]} {table_year} года <br></pre></p>\n'

    if table_type == TABLE_TYPE_FULL:
        table_length = calendar.monthrange(table_year, table_month)[1]
        day_range = list(range(1, 16)) + [40] + list(range(16, table_length + 1)) + [41, 42]
    else:
        day_range = list(range(1, 16)) + [40]

    table_index = 0
    # write table header
    html += '\t<table id = "tb", cellpadding = "4">\n'
    html += '\t\t<tr>\n'  # table header
    html += '\t\t\t<td>№<br>п/п</td>\t<td>Должность</td>\t<td>Фамилия<br> и инициалы</td>\t<td>Таб. №</td>\t'
    for day in day_range:
        if day == 40:
            html += '<td>Кол.<br>отраб.<br>дней<br>за I п.</td><td>Кол.<br>отраб.<br>часов<br>за I п.</td>\n'
        elif day == 41:
            html += '<td>Кол.<br>отраб.<br>дней<br>за II п.</td><td>Кол.<br>отраб.<br>часов<br>за II п.</td>\n'
        elif day == 42:
            html += '<td>Дней</td><td>Часов</td>\n'
        elif (datetime.datetime(table_year, table_month, day).weekday() not in (5, 6)) and (day not in holidays) \
                or (day in short_days):
            html += f'<td>{day}</td>'
    html += '\t\t</tr>\n'  # end of table header

    # write other table strings
    for per in person:
        person_name = person[table_index][DB_NAME_POS]
        person_table_num = person[table_index][DB_TABN_POS]
        person_job = person[table_index][DB_JOB_POS]
        sum_days = 0
        sum_hours = 0.0
        sum_days_half = 0
        sum_hours_half = 0.0

        html += '\t\t<tr>\n'  # new row in table
        html += f'\t\t\t<td>{table_index + 1}</td>\t<td id = "al_left">{person_job}</td>\t' \
                f'<td id = "al_left">{person_name}</td>\t'\
                f'<td>{person_table_num}</td>\t'
        for day in day_range:
            if day == 40:
                html += f'<td>{sum_days}</td><td>{f_to_nice_str(sum_hours)}</td>\n'
            elif day == 41:
                html += f'<td>{sum_days-sum_days_half}</td><td>{f_to_nice_str(sum_hours-sum_hours_half)}</td>\n'
            elif day == 42:
                html += f'<td>{sum_days}</td><td>{f_to_nice_str(sum_hours)}</td>\n'
            else:
                if day in short_days:
                    day_type = DAY_SHORT
                else:
                    day_type = DAY_NORM

                if datetime.datetime(table_year, table_month, day).weekday() not in (5, 6) and (day not in holidays) \
                        or day_type == DAY_SHORT:
                    cur_hours = calc_hours(person_name, day_type, f'{day}.{table_month}.{table_year}', aways)
                    if cur_hours not in ['A', 'O', 'А', 'Б', 'О']:
                        sum_hours += float(cur_hours)
                        sum_days += 1
                        if day <= 15:
                            sum_hours_half += float(cur_hours)
                            sum_days_half += 1
                    html += f'<td id="hc">{cur_hours}</td>'

        html += '\t\t</tr>\n'  # end of row
        table_index += 1

    html += '\t</table>\n'

    sub = make_table_subtitle(table_date, aways)
    sub_split = sub.split('\n')
    html += '<p>\n'
    for string in sub_split:
        html += '\t' + string + '<br>\n'
    html += '</p>\n'

    html += f'<p style="white-space: pre-wrap;">\tНачальник ЛОЦСиА'\
            f'\t\t\t\t{person[0][DB_NAME_POS]}</p>\n'

    html += '</div>\n'
    html += '<style>\n'
    html += '\t div, table { font: 22px times; } \n'
    html += '\t table, td, tr {\n'
    html += '\t border: 1px solid black;\n'
    html += '\t word-break: break-all;\n'
    html += '\t border-collapse: collapse;\n'
    html += '\t text-align: center\n'
    html += '\t}\n'
    html += '\t #al_left {text-align: left}\n'
    if table_type == TABLE_TYPE_FULL:
        html += '\t @media print { @page {size: A3 landscape} }\n'
    else:
        html += '\t @media print { @page {size: A4 landscape} }\n'

    html += '</style>\n'

    print(os.listdir())
    with open(TABLE_PATH, 'w') as table_file:
        table_file.write(html)
    start_file(TABLE_PATH)


def fill_date2(event, entry1, entry2, fill_tp):
    fill_type = fill_tp.get()
    print(f'{fill_type}; {fill_tp}')
    entry2.config(state='normal')
    entry2.delete(0, 20)
    if fill_type == FILL_TYPE_ADMIN:
        entry2.insert(0, '8.00-17.00')
    elif fill_type == FILL_TYPE_OTGUL:
        entry2.insert(0, '12.45-17.00')
    elif fill_type == FILL_TYPE_OTPUSK:
        otpusk_start = datetime.strptime(entry1.get(), '%d.%m.%Y')
        otpusk_end = otpusk_start + timedelta(days=14)
        entry2.insert(0, f'{otpusk_end.day}.{otpusk_end.month:02d}.{otpusk_end.year}')
    elif fill_type == FILL_TYPE_HOSPITAL:
        hosp_start = datetime.strptime(entry1.get(), '%d.%m.%Y')
        hosp_end = hosp_start + timedelta(days=7)
        entry2.insert(0, f'{hosp_end.day}.{hosp_end.month:02d}.'
                                   f'{hosp_end.year}')


def start_file(file):
    if sys.platform in ['win32', 'win64']:
        os.startfile(file)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, file])


if __name__ == '__main__':
    # aways = ( ('Ляхов Е.Л.', 'отпуск', datetime.datetime(2021, 3, 10), datetime.datetime(2021, 4, 10)),
    #           ('Ляхов Е.Л.',   'админ.', datetime.datetime(2021, 3, 2, 8, 0), datetime.datetime(2021, 3, 8, 8, 30)),
    #           ('Поляков А.Е.', 'админ.', datetime.datetime(2021, 3, 2, 8, 0), datetime.datetime(2021, 3, 2, 8, 30)),
    #           ('Поляков А.Е.', 'админ.', datetime.datetime(2021, 3, 3, 8, 0), datetime.datetime(2021, 3, 3, 8, 30)),
    #           ('Поляков А.Е.', 'админ.', datetime.datetime(2021, 3, 3, 9, 0), datetime.datetime(2021, 3, 3, 10, 0)),
    #           ('Поляков А.Е.', 'админ.', datetime.datetime(2021, 3, 4, 11, 0), datetime.datetime(2021, 3, 4, 13, 0)),
    #           ('Поляков А.Е.', 'админ.', datetime.datetime(2021, 3, 5, 12, 0), datetime.datetime(2021, 3, 5, 14, 0)),
    #           ('Поляков А.Е.', 'админ.', datetime.datetime(2021, 3, 6, 15, 0), datetime.datetime(2021, 3, 6, 17, 0)),
    #           ('Поляков А.Е.', 'отпуск', datetime.datetime(2021, 3, 10), datetime.datetime(2021, 3, 25)),
    #           ('Романова К.А.', 'больн.', datetime.datetime(2021, 3, 10), datetime.datetime(2021, 3, 25)),
    # )
    # print(calc_hours('Ляхов Е.Л.', DAY_NORM, '12.03.2021', aways))
    # print(calc_hours('Ляхов Е.Л.', DAY_NORM, '8.03.2021', aways))
    # print(calc_hours('Поляков А.Е.', DAY_NORM, '12.03.2021', aways))
    # print(calc_hours('Поляков А.Е.', DAY_NORM, '2.03.2021', aways))
    # print(make_table_subtitle('04.2021', aways))


    # 192.168.142.209
