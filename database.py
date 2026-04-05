import sqlite3
from datetime import datetime
conn=sqlite3.connect("expense.db")
cursor=conn.cursor()

cursor.execute("""
    create table if not exists expense(
            id integer primary key autoincrement,
            category text,
            cost float,
            date datetime)
""")

conn.commit()
conn.close()

print(f"数据库成功建立 {datetime.now()}")