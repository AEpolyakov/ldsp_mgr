import datetime

WORK_START = datetime.timedelta(hours=8)
WORK_END = datetime.timedelta(hours=17)
WORK_END_SHORT = datetime.timedelta(hours=16)
WORK_END_SAT = datetime.timedelta(hours=16, minutes=30)
DINNER_START = datetime.timedelta(hours=11, minutes=45)
DINNER_END = datetime.timedelta(hours=12, minutes=45)

DAY_NORM = 1
DAY_SHORT = 2
DAY_SATURDAY = 3

# BASE_PATH = './files/base.txt'
# REPORTS_PATH = './files/reports.txt'
NEW_REPORT_PATH = './files/new_report.html'
TABLE_PATH = './files/table.html'
# SHORT_DAY_PATH = './files/short_days.txt'
# HOLIDAY_PATH = './files/holidays.txt'
# HELP_PATH = './files/help.html'

RU_DATE_FORMAT_5 = '%d.%m.%Y %H.%M'
RU_DATE_FORMAT_3 = '%d.%m.%Y'
RU_DATE_FORMAT_2 = '%m.%Y'

PAGE_ADMIN = 0
PAGE_TABLE = 1
PAGE_MAGIC = 2
PAGE_BASE = 3

REPORT_TYPE_ADMIN = 0
REPORT_TYPE_OTGUL = 1
REPORT_TYPE_HOSPITAL = 2
REPORT_TYPE_OTPUSK_FULL = 3
REPORT_TYPE_OTPUSK_HALF1 = 4
REPORT_TYPE_OTPUSK_HALF2 = 5

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
FILL_TYPE_OTPUSK = 3
FILL_TYPE_HOSPITAL = 2

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

AWAY_TYPE_ADMIN = 'админ.'
AWAY_TYPE_OTGUL = 'отгул'
AWAY_TYPE_HOSP = 'больн.'
AWAY_TYPE_OTPUSK = 'отпуск'