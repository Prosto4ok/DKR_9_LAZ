import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import ttk

conn = sqlite3.connect('base.db') # создаем бд
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS JoBro(
    id INT PRIMARY KEY,
   fname TEXT,
   lname TEXT,
   gender TEXT,
   KIA TEXT,
   chapter TEXT,
   stand TEXT);
""")
conn.commit()

# cur.execute("""INSERT INTO JoBro(id, fname, lname, gender, KIA, chapter, stand)
#    VALUES('01','Alex', 'Smith', 'male', 'kill', '3', 'her green');""")
# conn.commit()

# Выполнение SQL-запроса для получения данных из таблицы
select_query = "SELECT * FROM JoBro;"
cur.execute(select_query)
rows = cur.fetchall()

# создаем окно
root = tk.Tk()
root.title('JoBros')

# Создание графического интерфейса с таблицей
tree = ttk.Treeview(root)

# Определение столбцов таблицы
tree["columns"] = ("id", "Имя", "Фамилия", "Пол", "Статус", "Глава", "Стенд")
tree.heading("id", text="id")
tree.heading("Имя", text="Имя")
tree.heading("Фамилия", text="Фамилия")
tree.heading("Пол", text="Пол")
tree.heading("Статус", text="Статус")
tree.heading("Глава", text="Глава")
tree.heading("Стенд", text="Стенд")
tree.column('id', width=len('id') * 30)
tree.column('Имя', width=len('Имя') * 30)
tree.column('Фамилия', width=len('Фамилия') * 30)
tree.column('Пол', width=len('Пол') * 30)
tree.column('Статус', width=len('Статус') * 30)
tree.column('Глава', width=len('Глава') * 30)
tree.column('Стенд', width=len('Стенд') * 30)

# Заполнение таблицы данными
for row in rows:
    tree.insert("", "end", values=row)

tree.pack()

# создание поля для кнопок
canw= Canvas(root, bg='#f0f0f0')
canw.pack()

# окно добавления данных
def add():
    global okno, id, fname, lname, gender, KIA, chapter, stand
    okno = tk.Tk()
    id_text= Label(okno, text='id')
    id_text.grid(row=0, column=0)
    id = tk.Entry(okno)
    id.grid(row=0, column=1)
    fname_text= Label(okno, text='Имя')
    fname_text.grid(row=1, column=0)
    fname = tk.Entry(okno)
    fname.grid(row=1, column=1)
    lname_text= Label(okno, text='Фамилия')
    lname_text.grid(row=2, column=0)
    lname = tk.Entry(okno)
    lname.grid(row=2, column=1)
    gender_text = Label(okno, text='Пол')
    gender_text.grid(row=3, column=0)
    gender = tk.Entry(okno)
    gender.grid(row=3, column=1)
    KIA_text= Label(okno, text='Статус')
    KIA_text.grid(row=4, column=0)
    KIA = tk.Entry(okno)
    KIA.grid(row=4, column=1)
    chapter_text= Label(okno, text='Глава')
    chapter_text.grid(row=5, column=0)
    chapter = tk.Entry(okno)
    chapter.grid(row=5, column=1)
    stand_text= Label(okno, text='Стенд')
    stand_text.grid(row=6, column=0)
    stand = tk.Entry(okno)
    stand.grid(row=6, column=1)
def knopka_add():
    add()
    button = tk.Button(okno, text='Добавить', command=getdata)
    button.grid()

# функция добавления данных
def getdata():
    jobro = (id.get(), fname.get(), lname.get(), gender.get(), KIA.get(), chapter.get(), stand.get())
    print(jobro)
    cur.execute("INSERT INTO JoBro VALUES(?, ?, ?, ?, ?, ?, ?);", jobro)
    conn.commit()
    okno.destroy()
    # Очистить таблицу
    for i in tree.get_children():
        tree.delete(i)
    # Заполнить таблицу заново
    cur.execute(select_query)
    rows = cur.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)
    # Обновить графический интерфейс
    tree.update()

# функция поиска данных
def search_data():
    # Очистить таблицу
    for item in tree.get_children():
        tree.delete(item)

    search_criteria = search_entry.get()
    search_query = "SELECT * FROM JoBro WHERE id LIKE ? OR fname LIKE ? OR lname LIKE ?;"
    cur.execute(search_query, ('%' + search_criteria + '%', '%' + search_criteria + '%', '%' + search_criteria + '%'))
    search_results = cur.fetchall()
    # Заполнение таблицы данными
    for result in search_results:
        tree.insert("", "end", values=result)

    # Обновить графический интерфейс
    tree.update()

# функция удаления данных
def delete_data():
    # Получение выделенной строки таблицы
    selected_item = tree.focus()
    data = tree.item(selected_item)['values']
    # Удаление записи из базы данных
    cur.execute("DELETE FROM JoBro WHERE id=?", (data[0],))
    conn.commit()
    # Удаление строки из таблицы
    tree.delete(selected_item)

# функция обновления
def update():
    # Очистить таблицу
    for i in tree.get_children():
        tree.delete(i)
    cur.execute(select_query)
    rows = cur.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)
    # Обновить графический интерфейс
    tree.update()

def editdata():
    # Получить выбранную строку
    selected_item = tree.focus()
    values = tree.item(selected_item)["values"]
    # Заполнить поля существующими данными
    add()
    id.delete(0, tk.END)
    id.insert(0, values[0])
    fname.delete(0, tk.END)
    fname.insert(0, values[1])
    lname.delete(0, tk.END)
    lname.insert(0, values[2])
    gender.delete(0, tk.END)
    gender.insert(0, values[3])
    KIA.delete(0, tk.END)
    KIA.insert(0, values[4])
    chapter.delete(0, tk.END)
    chapter.insert(0, values[5])
    stand.delete(0, tk.END)
    stand.insert(0, values[6])
    redakt_button= tk.Button(okno, text='Редактировать', command=updatedata)
    redakt_button.grid()

def updatedata():
    # Получить новые значения полей
    jobro = (id.get(), fname.get(), lname.get(), gender.get(), KIA.get(), chapter.get(), stand.get())
    # Обновить данные в базе данных
    cur.execute("UPDATE JoBro SET fname=?, lname=?, gender=?, KIA=?, chapter=?, stand=? WHERE id=?;", jobro[1:]+(jobro[0],))
    conn.commit()
    okno.destroy()
    update()

# добавление кнопок под таблицей
del_button = tk.Button(canw, text='Удалить', command=delete_data)
del_button.place(x=0, y=0)
button_add = tk.Button(canw, text='Добавить', command=knopka_add)
button_add.place(x=60, y=0)
search_entry = tk.Entry(canw)
search_entry.place(x=130, y=0)
search_button = tk.Button(canw, text='Поиск', command=search_data)
search_button.place(x=170, y=30)
update_button = tk.Button(canw, text='Обновить', command=update)
update_button.place(x=260, y=0)
edit_button = tk.Button(canw, text='Редактировать', command=editdata)
edit_button.place(x=260, y=30)
root.mainloop()