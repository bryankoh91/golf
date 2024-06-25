# https://medium.com/@dmitryrastorguev/basic-user-authentication-login-for-flask-using-mongoengine-and-wtforms-922e64ef87fe
from importlib import import_module
from flask_login import login_required, current_user
from flask import render_template, request
from app import app, db, login_manager
from datetime import datetime

# Register Blueprint so we can factor routes
# from bmi import bmi, get_dict_from_csv, insert_reading_data_into_database
from controllers.bmi import bmi
from controllers.dashboard import dashboard
from controllers.auth import auth
# from auth import auth

# register blueprint from respective module
app.register_blueprint(dashboard)
app.register_blueprint(auth)
app.register_blueprint(bmi)

# from models.chart import CHART
from models.bmidaily import BMIDAILY
from models.bmilog import BMILOG
from models.users import User
import csv
import io

# Load the current user if any
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

@app.route('/base')
def show_base():
    return render_template('base.html')

@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'GET':
        return render_template("upload.html", name=current_user.name, panel="Upload")
    elif request.method == 'POST':
        file = request.files.get('file')
        if file:
            data = file.read().decode('utf-8')
            csv_reader = csv.DictReader(data.splitlines())
            for row in csv_reader:
                user_email = row['User_email']
                print(user_email)
                measure_date = datetime.strptime(row['Date'], '%Y-%m-%d %H:%M:%S')
                print(measure_date)
                weight = float(row['Weight'])
                print(weight)
                height = float(row['Height'])
                print(height)
                unit = row['Unit']
                print(unit) 

                existing_user = User.getUser(email=user_email)
                if existing_user:
                    bmilog = BMILOG(user=existing_user, datetime=measure_date, weight=weight, height=height, unit=unit)
                    bmilog.bmi = bmilog.computeBMI()
                    bmilog.save()     
            file.close()

        return render_template("upload.html", name=current_user.name, panel="Upload")
