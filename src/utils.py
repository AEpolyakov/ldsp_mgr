import calendar
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from tkinter import END, ACTIVE

from consts import *
from sql_handle import db_names_get, db_get, db_read_colored_days, db_read_aways, db_get_all_aways, db_delete_by_id


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


def datatime_to_str(dt=datetime.timedelta(hours=0)):
    hours = dt.seconds // 3600
    minutes = (dt.seconds // 60) % 60
    if minutes == 00:
        res = f'{hours}'
    elif minutes == 30:
        res = f'{hours}.5'
    else:
        minutes = round(minutes / 60 * 100)
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
                else:  # away[AWAY_TYPE_POS] == AWAY_TYPE_OTGUL:
                    pass

    if res_str not in ['A', 'O', 'Б', 'А', 'О']:
        res_str = datatime_to_str(res)

    return res_str


def fill_person_listbox(listbox):
    names = db_names_get()
    for name in names:
        listbox.insert(END, f'{name}')


def parse_date(date1='1.2.2021', date2=''):
    d1 = datetime.datetime.strptime(date1, '%d.%m.%Y')
    date2 = date2.replace(',', '.')

    try:
        if date2 == '':
            ds = date1
            d2 = d1 + WORK_END
            d1 += WORK_START
        else:
            if '-' in date2:  # date2 = '8.00-12.00'
                date2_spl = date2.split('-')  # ('8.00', '12.00')
                date2_0_spl = date2_spl[0].split('.')  # ('8', '00')
                date2_1_spl = date2_spl[1].split('.')  # ('12', '00')
                ds = f'{date1} c {date2_spl[0]} по {date2_spl[1]}'
                if len(date2_0_spl) == 1:
                    dt1 = datetime.timedelta(hours=int(date2_0_spl[0]))
                else:
                    dt1 = datetime.timedelta(hours=int(date2_0_spl[0]), minutes=int(date2_0_spl[1]))
                if len(date2_1_spl) == 1:
                    dt2 = datetime.timedelta(hours=int(date2_1_spl[0]))
                else:
                    dt2 = datetime.timedelta(hours=int(date2_1_spl[0]), minutes=int(date2_1_spl[1]))
                d2 = d1 + dt2
                d1 += dt1
            else:
                d2 = datetime.datetime.strptime(date2, '%d.%m.%Y')
                ds = f'c {date1} по {date2}'
        print(f'ds = {ds}')
        return d1, d2, ds
    except TypeError:
        return None, None, None


def make_report(away_type, listbox, date1, date2, status_label):
    d1, d2, ds = parse_date(date1.get(), date2.get())
    report = {'name': listbox.get(ACTIVE), 'type': away_type.get(),
              'date1': d1, 'date2': d2, 'string_date': ds, 'string_away': ''}
    if report['date1'] is None:
        status_label['text'] = '!! неверная дата !!'
    else:
        status_label['text'] = ''

        # red, blue = db_read_colored_days(report['date1'].year, report['date1'].month)

        person = db_get('*', report['name'])[0]

        if report['type'] != REPORT_TYPE_HOSPITAL:
            html = ''
            html += '<div id = "m_text">' + '\n'
            html += '\t' + '<table id = "m_text">' + '\n'
            html += '\t\t' + '<tr>' + '\n'
            html += '\t\t\t' + '<td width=410></td>' + '\n'  # empty cell
            html += '\t\t\t' + '<td>Главному конструктору<br>Начальнику ОКБ<br>Воронцову В.А.<br>\n'
            html += '\t\t\t\t' + f'от {person[DB_JOB2_POS]}<br>\n'  # speciality
            html += '\t\t\t\t' + f'ЛОЦСиА<br>\n'  # speciality
            html += '\t\t\t\t' + f'{person[DB_NAME2_POS]}<br>\n'  # last name + initials
            html += '\t\t\t\t' + f'таб. №{person[DB_TABN_POS]}<br>\n'  # table number
            html += '\t\t\t\t' + f'пропуск № {person[DB_PASSN_POS]}<br>\n'  # pass number
            html += '\t\t\t\t' + f'тел. 26-40<br>\n'  # laboratory telephone number
            html += '\t\t\t' + '</td>' + '\n'
            html += '\t\t' + '</tr>' + '\n'
            html += '\t' + '</table>' + '\n'
            html += '\t<p id = "z">Заявление</p>\n'

            if report['type'] == REPORT_TYPE_ADMIN:
                away_reason = f'Прошу предоставить мне отпуск без сохранения заработной платы {report["string_date"]}' \
                              f' по семейным обстоятельствам.'
                status_label['text'] = 'заявка на административный отпуск оформлена!'
            elif report['type'] == REPORT_TYPE_OTGUL:
                away_reason = f'Прошу предоставить мне отгул {report["string_date"]} за заранее отработанное время'
                status_label['text'] = 'заявка на отгул оформлена!'
            elif report['type'] == REPORT_TYPE_OTPUSK:
                away_reason = f'Прошу предоставить очередной отпуск за {report["date1"].year} г. ' \
                              f'{report["string_date"]}.'
                status_label['text'] = 'заявка отпуск оформлена!'
            else:
                away_reason = ''

            html += f'\t<p style="white-space: pre-wrap;">\t{away_reason}</p>\n'
            html += '</div>\n'

            html += '<style>\n'
            html += '\t #z { text-align: center }\n'
            html += '\t #m_text { font: 16px sans-serif; line-height: 1.5;}\n'
            html += '</style>\n'
            with open(NEW_REPORT_PATH, 'w') as f:
                f.write(html)
            start_file(NEW_REPORT_PATH)
        elif report['type'] == REPORT_TYPE_HOSPITAL:
            status_label['text'] = 'информация о больничном принята'

        make_db_record(report)


def make_db_record(report):
    print(f'make_db_record: {report}')
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
                f'<td id = "al_left">{person_name}</td>\t' \
                f'<td>{person_table_num}</td>\t'
        for day in day_range:
            if day == 40:
                html += f'<td>{sum_days}</td><td>{f_to_nice_str(sum_hours)}</td>\n'
            elif day == 41:
                html += f'<td>{sum_days - sum_days_half}</td><td>{f_to_nice_str(sum_hours - sum_hours_half)}</td>\n'
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

    html += f'<p style="white-space: pre-wrap;">\tНачальник ЛОЦСиА' \
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

    with open(TABLE_PATH, 'w') as table_file:
        table_file.write(html)
    start_file(TABLE_PATH)


def fill_date2(event, entry1, entry2, fill_tp):
    fill_type = fill_tp.get()
    entry2.config(state='normal')
    entry2.delete(0, 20)
    if fill_type == FILL_TYPE_ADMIN:
        entry2.insert(0, '8.00-17.00')
    elif fill_type == FILL_TYPE_OTGUL:
        entry2.insert(0, '12.45-17.00')
    elif fill_type == FILL_TYPE_OTPUSK:
        otpusk_start = datetime.datetime.strptime(entry1.get(), '%d.%m.%Y')
        otpusk_end = otpusk_start + timedelta(days=14)
        entry2.insert(0, f'{otpusk_end.day}.{otpusk_end.month:02d}.{otpusk_end.year}')
    elif fill_type == FILL_TYPE_HOSPITAL:
        hosp_start = datetime.datetime.strptime(entry1.get(), '%d.%m.%Y')  # datetime.strptime(entry1.get(), '%d.%m.%Y')
        hosp_end = hosp_start + timedelta(days=7)
        entry2.insert(0, f'{hosp_end.day}.{hosp_end.month:02d}.'
                         f'{hosp_end.year}')


def start_file(file):
    if sys.platform in ['win32', 'win64']:
        os.startfile(file)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, file])


def td(string, td_id=''):
    return f'<td>{string}</td>' if td_id == '' else f'<td id="{td_id}">{string}</td>'


def tr(string, tr_id=''):
    return f'<tr>{string}</tr>' if tr_id == '' else f'<tr id="{tr_id}">{string}</tr>'


def table(string, table_id=''):
    return f'<table>{string}</table>' if table_id == '' else f'<table id="{table_id}">{string}</table>'


def info_styles():
    s = 'table { font: 22px Aial; ' \
        'margin-left: auto;' \
        'margin-right: auto;' \
        '}' \
        'table, td, tr {' \
        'border: 1px solid black; ' \
        'word-break: break-all;' \
        'border-collapse: collapse;' \
        'text-align: center;' \
        'padding: 5px;' \
        '}' \
        '#a, #c, #e, #g {' \
        'background-color: #E8E8E8; }' \
        '#b, #d, #f, #h {' \
        'background-color: #F8F8F8; }' \
        '#head {' \
        'background-color: #E0E0E0; }'

    return f'<style>{s}</style>'


def del_by_id(db_id_entry, label):
    db_id = db_id_entry.get()
    if db_id is not None:
        db_delete_by_id(int(db_id))
        label['text'] = f'запись {db_id} удалена'
    else:
        label['text'] = f'неверный номер'


def info_base():
    lines = db_get()
    html = tr(
        f'{td("Ф.И.О.", "head")}{td("Табельный номер", "head")}{td("Номер пропуска", "head")}{td("Должность", "head")}')
    for line in lines:
        row = f'{td(line[DB_NAME_POS], "a")}' \
              f'{td(line[DB_TABN_POS], "b")}' \
              f'{td(line[DB_PASSN_POS], "c")}' \
              f'{td(line[DB_JOB_POS], "d")}'
        html += tr(row)

    html = table(html)
    html += info_styles()
    return html


def info_help():
    with open(HELP_PATH, 'r') as f:
        lines = f.read()
    return lines


def info_aways():
    lines = db_get_all_aways()
    html = tr(
        f'{td("id", "head")}{td("Ф.И.О.", "head")}{td("Тип", "head")}{td("Дата 1", "head")}{td("Дата 2", "head")}')
    for line in lines:
        row = f'{td(line[DB_AWAY_ID_POS], "a")}' \
              f'{td(line[DB_AWAY_NAME_POS], "b")}' \
              f'{td(line[DB_AWAY_TYPE_POS], "c")}' \
              f'{td(line[DB_AWAY_DATE1_POS], "d")}' \
              f'{td(line[DB_AWAY_DATE2_POS], "e")}'
        html += tr(row)

    html = table(html)
    html += info_styles()
    return html


def info_holidays():
    pass


def info(info_type):
    func_dict = {INFO_AWAYS: info_aways, INFO_BASE: info_base, INFO_HOLIDAY: info_holidays, INFO_HELP: info_help}
    html = func_dict[info_type]()

    with open(INFO_PATH, 'w') as f:
        f.write(html)
    start_file(INFO_PATH)


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

    # print(parse_date('7.04.2021'))
    # print(parse_date('7.04.2021', '8.04.2021'))
    # print(parse_date('7.04.2021', '8.00-17.00'))
    # print(parse_date('7.04.2021', '8.00-14.30'))
    # print(parse_date('7.04.2021', '8-17'))
    # print(parse_date('7.04.2021', '8,15-11,45'))

    pass
