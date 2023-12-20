from flask import Flask, render_template, request, url_for, redirect
from database import get_database, connect_to_database
from text import check_time, sent_text_message
import time as tm
import schedule

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    db = get_database()
    task_cursor = db.execute("select * from todolist")
    alltasks = task_cursor.fetchall()
    return render_template("index.html" , alltasks = alltasks, check_time=check_time)

@app.route("/inserttask", methods=["POST", "GET"])
def inserttask():
    if request.method == "POST":
        enteredtask = request.form["todaystask"]
        if not enteredtask.strip() =="":
            db = get_database()
            db.execute("insert into todolist ( task) values (?)", [enteredtask])
            db.commit()
        return redirect(url_for("index"))
    return render_template("index.html")

@app.route("/deletetask<int:id>", methods=["POST", "GET"])
def deletetask(id):
    if request.method == "GET":
        db = get_database()
        db.execute("delete from todolist where id = ?", [id])
        db.commit()
        return redirect(url_for("index"))
    return render_template("index.html")


schedule.every(10).minutes.do(check_time)

while True:
    schedule.run_pending()
    
    db = get_database()
    task_cursor = db.execute("select * from todolist")
    alltasks = task_cursor.fetchall()
    for eachtask in alltasks:
        item = eachtask.task.split('+')[0]
        time = eachtask.task.split('+')[1]
        complete = check_time(time)
        if complete:
            sent_text_message(item)
    tm.sleep(1)

if __name__ == "__main__":
    app.run(debug = True)

