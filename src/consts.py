import datetime
import os
import sys


WORK_START = datetime.timedelta(hours=8)
WORK_END = datetime.timedelta(hours=17)
WORK_END_SHORT = datetime.timedelta(hours=16)
WORK_END_SAT = datetime.timedelta(hours=16, minutes=30)
DINNER_START = datetime.timedelta(hours=11, minutes=45)
DINNER_END = datetime.timedelta(hours=12, minutes=45)

DAY_NORM = 1
DAY_SHORT = 2
DAY_SATURDAY = 3
DAY_NDDAY = 4

AWAY_PATH = os.path.join('..', 'files', 'away.html')
NEW_REPORT_PATH = os.path.join('..', 'files', 'new_report.html')
TABLE_PATH = os.path.join('..', 'files', 'table.html')
INFO_PATH = os.path.join('..', 'files', 'info.html')
HELP_PATH = os.path.join('..', 'files', 'help.html')
MAGIC_PATH = os.path.join('..', 'files', 'magic.html')
RED_CROSS = os.path.join('..', 'misc', 'red_cross.png')


RU_DATE_FORMAT_5 = '%d.%m.%Y %H.%M'
RU_DATE_FORMAT_3 = '%d.%m.%Y'
RU_DATE_FORMAT_2 = '%m.%Y'

PAGE_ADMIN = 0
PAGE_TABLE = 1
PAGE_MAGIC = 2
PAGE_BASE = 3

REP_NAME_POS = 0
REP_TYPE_POS = 1
REP_DATE_POS = 2

TABLE_TYPE_HALF = 0
TABLE_TYPE_FULL = 1

DATE_TYPE_SINGLE = 0
DATE_TYPE_DATE_INTERVAL = 1
DATE_TYPE_DATE_PLUS_TIME_INTERVAL = 2

SUBTITLE_HOSP = 0
SUBTITLE_OTPUSK = 1

FILL_TYPE_ADMIN = 0
FILL_TYPE_OTGUL = 1
FILL_TYPE_HOSPITAL = 2
FILL_TYPE_OTPUSK = 3
FILL_TYPE_KOMAND = 4


DB_NAME_POS = 1
DB_NAME2_POS = 2
DB_TABN_POS = 3
DB_PASSN_POS = 4
DB_JOB_POS = 5
DB_JOB2_POS = 6

AWAY_NAME_POS = 0
AWAY_TYPE_POS = 1
AWAY_DATE1_POS = 2
AWAY_DATE2_POS = 3

DB_AWAY_ID_POS = 0
DB_AWAY_NAME_POS = 1
DB_AWAY_TYPE_POS = 2
DB_AWAY_DATE1_POS = 3
DB_AWAY_DATE2_POS = 4
DB_AWAY_DATE_ADDED = 5
DB_AWAY_NAME_ADDED = 6

AWAY_TYPE_ADMIN = 'админ.'
AWAY_TYPE_OTGUL = 'отгул'
AWAY_TYPE_HOSP = 'больн.'
AWAY_TYPE_OTPUSK = 'отпуск'
AWAY_TYPE_KOMAND = 'команд.'


REPORT_TYPE_ADMIN = 0
REPORT_TYPE_OTGUL = 1
REPORT_TYPE_HOSPITAL = 2
REPORT_TYPE_OTPUSK = 3
REPORT_TYPE_KOMAND = 4

TYPE_DICT = {REPORT_TYPE_ADMIN: AWAY_TYPE_ADMIN,
             REPORT_TYPE_OTGUL: AWAY_TYPE_OTGUL,
             REPORT_TYPE_HOSPITAL: AWAY_TYPE_HOSP,
             REPORT_TYPE_OTPUSK: AWAY_TYPE_OTPUSK,
             REPORT_TYPE_KOMAND: AWAY_TYPE_KOMAND,
             }

INFO_AWAYS = 0
INFO_BASE = 1
INFO_HOLIDAY = 2
INFO_SHORT_DAY = 3
INFO_LAST_TAB = 4
INFO_LAST_STATEMENT = 5
INFO_LAST_MAGIC = 6
INFO_HELP = 7

exception_list = ['A', 'O', 'А', 'Б', 'О', 'K', 'К', 'НД']
