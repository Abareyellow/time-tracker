import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from helpers import *


# Configure application
app = Flask(__name__)
app.secret_key = "secret key"

# Ensure templates are auto-reloaded
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///inmates.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# When the application runs, this method will run everything for the index page.
# This page is the login page for the application. Once the user logins, they will be redirect to the homepage.
@app.route("/", methods=["GET", "POST"])
def index():

    session.clear()
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        valid = db.execute("SELECT * FROM Staff WHERE Username = ? AND Password = ?", username, password)

        if len(valid) == 1:
            session["user_id"] = valid[0]["Plant"]
            return redirect("/homepage")
        else:
            error = "Invalid Username and/or Password"
            return render_template("index.html", error=error)

    else:
        return render_template("index.html")

@app.route("/request", methods=["GET", "POST"])
@login_required
def get_request():
    plant = db.execute("SELECT Name From Plant WHERE id = ?", session["user_id"])
    re = db.execute("SELECT * FROM Request WHERE status = ?", "Open")
    if request.method == "POST":
        plan =  request.form.get("plant")
        need = request.form.get("need")
        note = ""

        if need == "Add":
            first = request.form.get("first")
            last = request.form.get("last")
            note = f"{first} {last} needs to be add to {plant[0]['Name']}"
        elif need == "Update":
            note = request.form.get("update")
        elif need == "Other":
            note = request.form.get("update")

        db.execute("INSERT INTO Request (need, plant, note, status) VALUES (?,?,?,?)", need, plan, note, "Open")

        return redirect("/request")

    else:
        return render_template("request.html", plant=plant[0]["Name"], request=re)

@app.route("/status", methods=["POST"])
@login_required
def status():
   if request.method == "POST":
    num = request.form.get("num")
    find_request = db.execute("SELECT * FROM Request WHERE num = ?", num)

    return render_template("status.html", num=num, plant=find_request[0]['plant'], need=find_request[0]['need'], note=find_request[0]['note'])

@app.route("/closed", methods=["POST"])
@login_required
def closed():
    num = request.form.get("num")
    db.execute("UPDATE Request SET status = 'Closed' WHERE num = ?", num)
    return redirect("/request")

#This homepage will display every inmates within the plant.
@app.route("/homepage", methods=["GET", "POST"])
@login_required
def homepage():
    all = db.execute("SELECT * FROM Inmates Where Plant = ?", session["user_id"])
    plant = db.execute("SELECT Name FROM Plant WHERE id = ?", session["user_id"])
    lenOfAll = len(all)
    update = db.execute("SELECT * FROM Inmates WHERE NextVacationDate = ? and Plant = ?", today_date(), session["user_id"])
    lupdate = len(update)
    get_vacation_hours(update)
    sick = db.execute("SELECT * FROM Inmates WHERE NextSickDate = ? and Plant = ?", today_date(), session["user_id"])
    lsick = len(sick)
    get_sick_hours(sick)
    remind = db.execute("SELECT * FROM Inmates WHERE VacationHours >= 200 and Plant = ?", session["user_id"])
    lremind = len(remind)
    nsick = past_sick_date(all)
    nvaca = past_vacation_date(all)
    get_sick_hours(nsick)
    get_vacation_hours(nvaca)
    lenTog = len(nsick) + len(nvaca)

    if request.method == "POST":
        print("Here")

        if request.form.get("hours") == "sick":
            print()
            num = request.form.get("opus")
            value = db.execute("SELECT * FROM Inmates WHERE OPUSNumber = ?", num)

            if len(value) == 1:
                val = int(value[0]['SickHours']) + 3
                date = add_a_month(value[0]['NextSickDate'])
                db.execute("UPDATE Inmates SET SickHours = :sick, NextSickDate = :dat WHERE OPUSNumber = :n", sick=val, dat=date, n=num)

        elif request.form.get("hours") == "vacation":
            print()
            num = request.form.get("opus")
            value = db.execute("SELECT * FROM Inmates WHERE OPUSNumber = ?", num)

            if len(value) == 1:
                val = int(value[0]['VacationHours'])
                date = value[0]['NextVacationDate']
                start = value[0]['StartDate']
                db.execute("UPDATE Inmates SET VacationHours = :hours, NextVacationDate = :vaca WHERE OPUSNumber = :n", hours=findTime(start, val), vaca=next_month_last_day(date), n=num)

        elif request.form.get("hours") == "hsick":
            print()
            num = request.form.get("opus")
            value = db.execute("SELECT * FROM Inmates WHERE OPUSNumber = ?", num)

            if len(value) == 1:
                val = int(value[0]['SickHours']) + 3
                date = add_a_month(value[0]['NextSickDate'])
                db.execute("UPDATE Inmates SET SickHours = :sick, NextSickDate = :dat WHERE OPUSNumber = :n", sick=val, dat=date, n=num)

        elif request.form.get("hours") == "hvaca":
            print()
            num = request.form.get("opus")
            value = db.execute("SELECT * FROM Inmates WHERE OPUSNumber = ?", num)

            if len(value) == 1:
                val = int(value[0]['VacationHours'])
                date = value[0]['NextVacationDate']
                start = value[0]['StartDate']
                db.execute("UPDATE Inmates SET VacationHours = :hours, NextVacationDate = :vaca WHERE OPUSNumber = :n", hours=findTime(start, val), vaca=next_month_last_day(date), n=num)

        return redirect('/homepage')
    else:
        return render_template("homepage.html", all=all, update=update, sick=sick, remind=remind, lall=lenOfAll, lupdate=lupdate, lsick=lsick, lremind=lremind, nsick=nsick, nvaca=nvaca, lenTog=lenTog, plant=plant[0]["Name"])

@app.route("/add_plant", methods=["GET", "POST"])
@login_required
def add_plant():
    if request.method == "POST":
        name = request.form.get("name")
        db.execute("INSERT INTO Plant (Name) VALUES (?)", name)
        return redirect("/add_plant")

    else:
        return render_template("addplant.html")

@app.route("/add_user", methods=["GET", "POST"])
@login_required
def add_user():
    all = db.execute("SELECT * FROM Plant WHERE Name != 'Admin'")
    if request.method == "POST":
         name = request.form.get("name")
         plant = request.form.get("plant")

         split = name.split()
         username = split[0] + split[1]
         password = split[0] + f"{randomize4Digits()}" + "is_rock!"

         db.execute("INSERT INTO Staff (Name, Username, Password, Plant) VALUES (?,?,?,?)", name, username, password, plant)
         return redirect("/add_user")
    else:
        return render_template("adduser.html", all=all)


# Adds Inmates to the Database
@app.route("/add", methods=["GET", "POST"])
@login_required
def add_to_datebase():
    all = db.execute("SELECT * FROM Plant WHERE Name != 'Admin'")
    if request.method == "POST":

        first = request.form.get("first")
        last = request.form.get("last")
        start = request.form.get("start")
        opus = request.form.get("opus")
        plant = request.form.get("plant")

        months = count_months(start)

        if months == 0:
            vdate = add_six_months(start)
            sdate = add_a_month(start)
            vacation = 0
            sick = 3
        elif months >= 1 and months < 6:
            vdate = add_six_months(start)
            sdate = add_n_months(start, months + 1)
            vacation = 0
            sick = 3 + (3 * months)
        elif months == 6:
            vdate = add_six_months(start)
            sdate = add_n_months(start, months + 1)
            vacation = 0
            sick = 3 + (3 * months)
        elif months > 6:
            vdate = find_the_last_day(today_date())
            sdate = add_n_months(start, months + 1)
            vacation = vacation_time(months)
            sick = 3 + (3 * months)

        db.execute("INSERT INTO Inmates (OPUSNumber, FirstName, LastName, StartDate, Plant, NextVacationDate, NextSickDate, VacationHours, SickHours) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", opus, first, last, start, plant, vdate, sdate, vacation, sick)

        return redirect("/add")

    else:
        return render_template("add.html", plant=session["user_id"], all=all)

# Updates Sick Hours and Vacation Hours
@app.route("/update", methods=["GET", "POST"])
@login_required
def update_hours():
    all = db.execute("SELECT * FROM Inmates WHERE Plant = ?", session["user_id"])
    every = db.execute("SELECT * FROM Inmates")
    if request.method == "POST":
        if request.form.get("time") == "vacation":
            num = request.form.get("opus")
            hours = int(request.form.get("hours"))

            value = db.execute("SELECT * FROM Inmates WHERE OPUSNumber = ?", num)
            hour = int(value[0]['VacationHours']) - hours
            if hour < 0:
                hour = 0
            db.execute("UPDATE Inmates SET VacationHours = :hours WHERE OPUSNumber = :num", hours=hour, num=num)
            db.execute("INSERT INTO Note (opus, date, note, hours) VALUES (?,?,?,?)", num, today_date(), f"Inmate {num} used {hours} of their vacation hours.", hours)
        else:
            num = request.form.get("opus")
            hours = int(request.form.get("hours"))

            value = db.execute("SELECT * FROM Inmates WHERE OPUSNumber = ?", num)
            hour = int(value[0]['SickHours']) - hours
            if hour < 0:
                hour = 0
            db.execute("UPDATE Inmates SET SickHours = :hours WHERE OPUSNumber = :num", hours=hour, num=num)
            db.execute("INSERT INTO Note (opus, date, note, hours) VALUES (?,?,?,?)", num, today_date(), f"Inmate {num} used {hours} of their sick hours.", hours)

        return redirect("/update")
    else:
        return render_template("update.html", inmates=all, every=every)

# Deletes An Inmate From a Database
@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    all = db.execute("SELECT * FROM Inmates WHERE Plant = ?", session["user_id"])
    every = db.execute("SELECT * FROM Inmates")
    if request.method == "POST":
        num = request.form.get("opus")

        db.execute("DELETE FROM Inmates WHERE OPUSNumber = ?", num)
        return redirect("/delete")
    else:
        return render_template("delete.html", plant=all, every=every)


def get_sick_hours(data):
    for i in data:
        id = i['OPUSNumber']
        hours = i['SickHours'] + 3
        day = add_a_month(i['NextSickDate'])
        db.execute("UPDATE Inmates SET SickHours = ?, NextSickDate = ? WHERE OPUSNumber = ?", hours, day, id)
        print(f"Got It! {i['FirstName']} {i['LastName']} has Updated")

def get_vacation_hours(data):
    for i in data:
        id = i['OPUSNumber']
        hours = findTime(today_date(), i['VacationHours'])
        day = add_a_month(i['NextVacationDate'])
        db.execute("UPDATE Inmates SET VacationHours = ?, NextVacationDate = ? WHERE OPUSNumber = ?", hours, day, id)
        print(f"Got It! {i['FirstName']} {i['LastName']} has Updated")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)