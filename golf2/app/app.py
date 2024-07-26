# https://medium.com/@dmitryrastorguev/basic-user-authentication-login-for-flask-using-mongoengine-and-wtforms-922e64ef87fe

from flask_login import login_required, current_user
from flask import render_template, request, jsonify, redirect, url_for, flash
from app import app, db, login_manager
from datetime import datetime, date
from pymongo import MongoClient

# Register Blueprint so we can factor routes
# from bmi import bmi, get_dict_from_csv, insert_reading_data_into_database

from controllers.dashboard import dashboard
from controllers.auth import auth
# from auth import auth

# register blueprint from respective module
app.register_blueprint(dashboard)
app.register_blueprint(auth)

# from models.chart import CHART
from models.users import User
from models.golfsetData import *
import csv
import io

# Load the current user if any
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

@app.route('/base')
def show_base():
    return render_template('base.html')

@app.route("/upload", methods=['GET','POST'])
@login_required
def upload():
    # if hte user just key in the /upload in the address
    if request.method == 'GET':
        ## Get all user, and pass it to upload.html dropdownlist
        users = User.getAllUsers()
        return render_template("upload.html", alluser=users, name=current_user.name, panel="Upload")
    elif request.method == 'POST':
        selectedGolfer = request.form.get('golfer')
        dataType = request.form.get('data_type')
        email = request.form.get("golfer")
        ##End of edit
        type = request.form.get('type')
        file = request.files.get('file')               
        data = file.read().decode('utf-8')
        dict_reader = csv.DictReader(io.StringIO(data), delimiter=',', quotechar='"')
        file.close()
        if type == 'create':
            print("No create Action yet")
 
        elif type == 'upload':
            if dataType == "Golf Set":
                try:
                    headers = ["label","clubtype","clubheadloft","clubheadweight","clubheadsize_material_style","shaftlength","shaftweight","shaftmaterial","shaftflex","gripdiameter","gripweight", "gripmaterial"]
                    datawithhead = io.StringIO(','.join(headers) + '\n' + data)
                    dict_reader = csv.DictReader(datawithhead, delimiter=',', quotechar='"', fieldnames=headers)
                    next(dict_reader)
                    for data in dict_reader:
                        label = data['label'].strip('"')
                        clubtype = (data['clubtype'])
                        clubheadloft = data['clubheadloft']
                        clubheadweight = data['clubheadweight']
                        clubheadsize_material_style= data['clubheadsize_material_style']
                        shaftlength= data['shaftlength']
                        shaftweight= data['shaftweight']
                        shaftmaterial= data['shaftmaterial']
                        shaftflex= data['shaftflex']
                        gripdiameter= data['gripdiameter']
                        gripweight= data['gripweight']
                        gripmaterial= data['gripmaterial']
                        golfset = GolfSet.createGolfSet(email, label, clubtype, clubheadloft, clubheadweight, clubheadsize_material_style, shaftlength, shaftweight, shaftmaterial, shaftflex, gripdiameter, gripweight, gripmaterial).save()
                    print('Golf Set uploaded successfully!', 'success')
                    flash('Golf Set uploaded successfully!', 'success')                    
                except Exception as e:
                    flash('Wrong file!!')
                    return redirect(url_for("upload"))
                return redirect(url_for("upload"))

            elif dataType == "Swings":
                try:

                    for data in dict_reader:
                        swing_datetime_str = data['swing_time'].strip('"')
                        swingSpeed = int(data['swing_speed'])
                        club = str(data['club_label'])
                        distance = Swing.getDistance(email=email, label=club, speed=swingSpeed)
                        data['distance'] = distance  # add distance field to the dictionary
                        swing = Swing.createSwingDistance(email, club, swingSpeed, swing_datetime_str, distance)
                    file.close
                    print(' Swing data uploaded successfully!', 'success')
                    flash('Swing data uploaded successfully!', 'success')
                except Exception as e:
                    flash('Wrong file!!')
                    return redirect(url_for("upload"))
                return redirect(url_for("upload"))
                
@app.route("/swing", methods=['GET','POST'])
@login_required
def swing():
    if request.method == 'GET':
        ## Get all user, and pass it to upload.html dropdownlist
        users = User.getAllUsers()
        return render_template("golfcalculator.html", alluser=users, name=current_user.name)

@app.route('/swingprocess', methods=['POST'])
@login_required
def swingprocess():
    email = request.form['email']
    club_label = request.form['club']
    speed = float(request.form['swing_speed'])
    datetime_str = request.form['datetime']
    
    # Retrieve the club object for the label
    club = Club.objects(email=email,label=club_label).first()
    distance = Swing.getDistance(email=email, label=club.label, speed=speed)
    print(club.clubtype)
    print(distance)
    Swing.createSwingDistance(email, club_label, speed, datetime_str, distance)
    return redirect(url_for("swing"))
    
@app.route("/swingchart", methods=['GET', 'POST'])
@login_required
def swingchart():
    if request.method == 'GET':
        return render_template('swingchart.html')

    elif request.method == 'POST':
        xyData = {}
        if current_user.email == 'admin@abc.com':  # check if the current user is an admin
            golfers = Swing.getAllOwnersWhoSwings()
        else:
            golfers = [current_user.email]  # restrict to only the current user

        if 'admin@abc.com' in golfers:
            for golfer in golfers:
                datetime_distance_list = Swing.getDateTimeDistanceList(golfer)
                xyData[golfer] = datetime_distance_list
            return jsonify({"xyData": xyData})
        else:
            dictionaryOfData = {}
            for golfer in golfers:
                swings = Swing.objects(golfer=golfer)
                for swing in swings:
                    club = swing.club
                    datetime_str = dt.datetime.strftime(swing.swing_datetime, "%Y-%m-%d %H:%M:%S")
                    distance = swing.distance
                    value = [datetime_str, distance]
                    if club in dictionaryOfData:
                        dictionaryOfData[club].append(value)
                    else:
                        dictionaryOfData[club] = [value]
            xyData = dictionaryOfData

        return jsonify({"xyData": xyData})

    return redirect(url_for("swingchart"))
        

@app.route("/getClubs", methods=["POST"])
@login_required
def getClubs():
    email = request.form.get("email")
    print(f"(Back-end) getClubs: email is {email}")
    
    clubs = Club.objects(email=email)

    arr = []
    for club in clubs:
        arr.append(club.label)

    return jsonify({"myClubs":arr})

@app.route("/getClubHeight", methods=["POST"])
@login_required
def getClubHeight():
    email = request.form.get("email")
    label = request.form.get("label")

    print(f"(Back-end) getClubHeight:\nemail= {email}\nlabel= {label}")

    golfset = GolfSet.getGolfSetByEmail(email)

    clubHeight = 0
    if not golfset is None:
        club = golfset.getClub(label)
        clubHeight = club.getClubHeight()

    return jsonify({"clubheight":clubHeight})


@app.route("/getClubAdvice", methods=["GET"])
def getClubAdvice():
    if request.method == 'GET':
        return render_template('getClubAdvice.html')

@app.route("/getClubAdviceprocess", methods=["POST"])
def getClubAdviceprocess():
    email = current_user.email
    swing_speed = float(request.form.get("swing_speed"))
    distance_input = float(request.form.get("distance"))
    delta = 50
    clubs = Club.objects(email=email)
    arr = []
    output = []
    output.append(f"Speed = {swing_speed}, distance = {distance_input} yards")
    
    if not clubs:
        output.append("No golfset recorded yet!")
        return jsonify(output=output)

    for club in clubs:
        distance = Swing.getDistance(email=email, label=club.label, speed=swing_speed)
        difference = abs(distance_input - distance)
        if difference <= delta:
            if club.label not in arr:
                arr.append(club.label)

    if arr:
        for club_label in arr:
            club = Club.objects(email=email, label=club_label).first()
            if club:
                output.append(f"Club: {club.label} length: {club.shaftlength} Loft: {club.clubheadloft}")
    else:
        output.append("No suitable club.")

    return jsonify(output=output)