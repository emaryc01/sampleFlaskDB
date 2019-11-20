import os
from flask import Flask, request, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, Numeric

app = Flask(__name__)

#find current path and use to connect to database
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "peopleDatabase.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

#Create people table if not exists
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    balance = db.Column(Numeric(precision=2), nullable=False)
    email = db.Column(db.String, nullable=False)
    address = db.Column(db.String(80), nullable=False)
    CheckConstraint(age > 0)

    # allow query return
    def __repr__(self):
        return " <ID: {}> <Name: {}> <Age: {} <Balance: {} <Email: {}  <Address: {}>".format(self.id, self.name, self.age, self.balance, self.email, self.address)


@app.route("/app/people", methods=["GET", "POST"])
def allObjects():
    try:
        people = None
        # If new person added from form POST request
        if request.form:
            person = People(name=request.form.get("newName"), age=request.form.get("newAge"), balance=request.form.get("newBalance"), email=request.form.get("newEmail"), address=request.form.get("newAddress"))
            db.session.add(person)
            db.session.commit()
        # fetch all people from table and return HTML page with new values
        people = db.session.query(People).all()
        return render_template("appPeople.html", people=people)
    except:
        return "Unable to carry out request.  Please check the database connection and try again."

# If person edited via form POST request
@app.route("/app/update", methods=["POST"])
def update():
    # if edit is update request
    if "update" in request.form:
        try:
            person = People.query.filter_by(id=request.form.get("updateID")).first()
            person.name = request.form.get("updateName")
            person.age = request.form.get("updateAge")
            person.balance = request.form.get("updateBalance")
            person.email = request.form.get("updateEmail")
            person.address = request.form.get("updateAddress")
            db.session.commit()
            return redirect("/app/people")
        except:
            return "Unfortunately something has gone wrong with your update.  Please return to the main page and try again."

    # if edit is delete request
    try:
        if "delete" in request.form:
            person = People.query.filter_by(id=request.form.get("updateID")).first()
            db.session.delete(person)
            # commit change to table and return HTML page with new values
            db.session.commit()
            return redirect("/app/people")
    except:
        return "Unfortunately something has gone wrong with your delete.  Please return to the main page and try again."

    #create database if not exists
def setupDB():
    db.create_all()

#on app launch
if __name__ == "__main__":
    setupDB()
    app.run()