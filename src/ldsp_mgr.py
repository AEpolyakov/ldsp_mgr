from utils import fill_person_listbox, make_report, make_table, fill_date2, info, del_by_id, make_magic, open_base_editor
from tkinter import *
import tkinter.ttk as tk_ttk
from consts import *

root = Tk()
root.title('табель-менеджер')
root.geometry('600x220-0-35')

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
person_listbox.select_set(0)
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
rb_komand = Radiobutton(pages[PAGE_ADMIN], variable=away_doc_type, text="команд.",
                          value=4, indicatoron=0, relief=GROOVE, width=BUTTON_WIDTH).place(x=480, y=20)

today = datetime.datetime.now()

entry_away_date1 = Entry(pages[PAGE_ADMIN], width=10)
entry_away_date1.place(x=200, y=50)
entry_away_date1.insert(0, f'{today.day}.{today.month:02d}.{today.year}')

entry_away_date2 = Entry(pages[PAGE_ADMIN], width=10)
entry_away_date2.place(x=300, y=50)
entry_away_date2['state'] = 'disabled'
entry_away_date2.bind('<Button-1>', lambda e, ent1=entry_away_date1, ent2=entry_away_date2,
                                           tp=away_doc_type: fill_date2(e, ent1, ent2, tp))

status_page1 = Label(pages[PAGE_ADMIN], text='')
status_page1.place(x=200, y=140)

Button(pages[PAGE_ADMIN], width=15, text='Заявка!',
       command=lambda t=away_doc_type, lb=person_listbox, d1=entry_away_date1, d2=entry_away_date2, l=status_page1:
       make_report(t, lb, d1, d2, l)).place(x=200, y=100)
# Button(pages[PAGE_ADMIN], width=15, text='В базу данных!', comm)


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
                           command=lambda dt=magic_date_entry: make_magic(dt))
button_make_magic.pack()

# items on page 4: data base
Button(pages[PAGE_BASE], width=30, text='База записей', relief=GROOVE,
       command=lambda x=INFO_AWAYS: info(x)).pack()
Button(pages[PAGE_BASE], width=30, text='База сотрудников', relief=GROOVE,
       command=lambda x=INFO_BASE: info(x)).pack()

base_id_entry = Entry(pages[PAGE_BASE], width=7)
base_id_entry.place(x=40, y=65)
db_status_label = Label(pages[PAGE_BASE], text='')
db_status_label.place(x=20, y=150)

Button(pages[PAGE_BASE], width=30, text='Удалить запись', relief=GROOVE,
       command=lambda x=base_id_entry, lb=db_status_label: del_by_id(x, lb)).pack()

Button(pages[PAGE_BASE], width=30, text='База записей 2', relief=GROOVE,
       command=lambda b=root, d="4.2021": open_base_editor(b, d)).pack()

Button(pages[PAGE_BASE], width=8, text='Справка', relief=GROOVE,
       command=lambda x=INFO_HELP: info(x)).place(x=400, y=0)

root.mainloop()
