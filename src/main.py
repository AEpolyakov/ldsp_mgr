from tkinter import *
from tkinter import messagebox
import tkinter.ttk as tk_ttk
from datetime import datetime, timedelta
from utils import normalize, hhmm_to_float, f_to_nice_str, calc_overlap, calc_hours, date_analysis
from utils import fill_person_listbox, make_report, make_report_record, make_table_subtitle, make_table, fill_date2
from consts import PAGE_ADMIN, PAGE_TABLE, PAGE_MAGIC, PAGE_BASE, TABLE_TYPE_FULL, TABLE_TYPE_HALF

root = Tk()
root.title('табель-менеджер')
root.geometry('500x220-0-35')

menu = tk_ttk.Notebook(root)
menu.pack(fill=BOTH)
status_bar = Label(text='')
status_bar.pack()
pages = []

page_admins = tk_ttk.Frame(root)
menu.add(page_admins, text='Заявления')
pages.append(page_admins)

page_table = tk_ttk.Frame(root)
menu.add(page_table, text='График выходов')
pages.append(page_table)

page_magic = tk_ttk.Frame(root)
menu.add(page_magic, text='Учёт раб. времени')
pages.append(page_magic)

page_base = tk_ttk.Frame(root)
menu.add(page_base, text='Другое')
pages.append(page_base)

#  items on page1
person_listbox = Listbox(pages[PAGE_ADMIN], width=20, height=10, exportselection=False)
person_listbox.pack(side=LEFT)
fill_person_listbox(person_listbox)
scroll = Scrollbar(pages[PAGE_ADMIN], command=person_listbox.yview)
scroll.pack(side=LEFT)

away_doc_type = IntVar()
away_doc_type.set(0)

BUTTON_WIDTH = 8
rb_admin = Radiobutton(pages[PAGE_ADMIN], variable=away_doc_type, text="админ.",
                       value=0, indicatoron=0, relief=GROOVE, width=BUTTON_WIDTH).place(x=200, y=20)
rb_otgul = Radiobutton(pages[PAGE_ADMIN], variable=away_doc_type, text="отгул",
                       value=1, indicatoron=0, relief=GROOVE, width=BUTTON_WIDTH).place(x=270, y=20)
rb_otpusk = Radiobutton(pages[PAGE_ADMIN], variable=away_doc_type, text="больнич.",
                        value=2, indicatoron=0, relief=GROOVE, width=BUTTON_WIDTH).place(x=340, y=20)
rb_hospital = Radiobutton(pages[PAGE_ADMIN], variable=away_doc_type, text="отпуск",
                          value=3, indicatoron=0, relief=GROOVE, width=BUTTON_WIDTH).place(x=410, y=20)

today = datetime.now()

entry_away_date1 = Entry(pages[PAGE_ADMIN], width=10)
entry_away_date1.place(x=200, y=50)
entry_away_date1.insert(0, f'{today.day}.{today.month}.{today.year}')

entry_away_date2 = Entry(pages[PAGE_ADMIN], width=10)
entry_away_date2.place(x=300, y=50)
entry_away_date2['state'] = 'disabled'
entry_away_date2.bind('<Button-1>', lambda e, ent1=entry_away_date1, ent2=entry_away_date2, tp=away_doc_type: fill_date2(e, ent1, ent2, tp))

Button(pages[PAGE_ADMIN], width=15, text='Заявка!', command=make_table).place(x=200, y=100)

status_page1 = Label(pages[PAGE_ADMIN], text='')
status_page1.place(x=200, y=140)

# items on page 2
table_date_entry = Entry(pages[PAGE_TABLE], width=7)
table_date_entry.insert(0, f'{today.month}.{today.year}')
table_date_entry.pack()
button_make_table_15 = Button(pages[PAGE_TABLE], width=30, text='Табель за 15 дней', relief=GROOVE,
                              command=lambda dt=table_date_entry, tp=TABLE_TYPE_HALF: make_table(dt, tp)).pack()
button_make_table_full = Button(pages[PAGE_TABLE], width=30, text='Табель за весь месяц', relief=GROOVE,
                                command=lambda dt=table_date_entry, tp=TABLE_TYPE_FULL: make_table(dt, tp)).pack()

# items on page 3: magic square
magic_date_entry = Entry(pages[PAGE_MAGIC], width=7)
magic_date_entry.insert(0, f'{today.month}.{today.year}')
magic_date_entry.pack()
button_make_magic = Button(pages[PAGE_MAGIC], width=30, text='ведомость учёта рабочего времени!', relief=GROOVE,
                                ).pack()
# Label(pages[PAGE_MAGIC], text='в разработке :-(').pack()

# items on page 4: data base
Button(pages[PAGE_BASE], width=30, text='База записей', relief=GROOVE,
       ).pack()
Button(pages[PAGE_BASE], width=30, text='База сотрудников', relief=GROOVE,
       ).pack()
Button(pages[PAGE_BASE], width=30, text='База праздников', relief=GROOVE,
       ).pack()
Button(pages[PAGE_BASE], width=30, text='База сокращённых дней', relief=GROOVE,
       ).pack()
Button(pages[PAGE_BASE], width=30, text='Последний табель', relief=GROOVE,
       ).pack()
Button(pages[PAGE_BASE], width=30, text='Пояледняя заявка', relief=GROOVE,
       ).pack()
Button(pages[PAGE_BASE], width=10, text='Справка', relief=GROOVE,
       ).place(x=350, y=0)

root.mainloop()
