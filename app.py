from flask import Flask,render_template,request
from datetime import datetime
import sqlite3

app=Flask(__name__)

def get_db():
    conn=sqlite3.connect("expense.db")
    conn.row_factory=sqlite3.Row
    return conn

@app.route("/")
def home():
        conn=get_db()
        category = request.args.get("category", "")
        if category=="":
                expenses=conn.execute("select * From expense").fetchall()
        else:
                expenses=conn.execute("SELECT * FROM expense WHERE category=?",(category,)).fetchall()
        #total = sum(float(expense['cost']) for expense in expenses if expense['cost'])
        total = 0
        for expense in expenses:
                print(expense['cost'], type(expense['cost']))  # ← 加这行
                try:
                    total += float(expense['cost'])
                except:
                    pass

        conn.close()
        now=datetime.now().strftime("%Y-%m-%d")
        return render_template("home.html",expenses=expenses,now=now,total=total)

@app.route("/add", methods=["POST"])
def add():
        conn=get_db()
        category=request.form["category"]
        cost = float(request.form.get("cost") or 0)
        date=request.form["date"]
        #date=datetime.now().strftime("%Y-%m-%d,%H:%M")
        conn.execute("INSERT INTO expense(category,cost,date) VALUES(?,?,?)",(category,cost,date))
        conn.commit()
        conn.close()
        return home()

@app.route("/delete", methods=["POST"])
def delete():
        id=request.form["id"]
        conn=get_db()
        conn.execute("DELETE FROM expense WHERE id=?",(id,))
        conn.commit()
        conn.close()
        return home()
total = 0


if __name__=="__main__":
    app.run(debug=True)                                                             