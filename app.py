# app/app.py

from flask import Flask, render_template
from flask_login import login_required, current_user
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from app.models.users import User
from app.models.golfsetData import GolfSet, Swing
import csv
import io

app = Flask(__name__)
app.static_folder = "static"
app.config["SECRET_KEY"] = "your_secret_key"
app.config["MONGODB_SETTINGS"] = {
    'db': 'my_golf',
    'host': 'localhost'
}

db = MongoEngine(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Set login view for Flask-Login

# Import and register Blueprints
from app.controllers.dashboard import dashboard
from app.controllers.auth import auth

app.register_blueprint(dashboard)
app.register_blueprint(auth)

# Load the current user if any
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

# Define routes

@app.route('/base')
def show_base():
    return render_template('base.html')

@app.route("/upload", methods=['GET','POST'])
@login_required
def upload():
    if request.method == 'GET':
        users = User.getAllUsers()
        return render_template("upload.html", alluser=users, name=current_user.name, panel="Upload")
    elif request.method == 'POST':
        selectedGolfer = request.form.get('golfer')
        dataType = request.form.get('data_type')
        email = request.form.get("golfer")
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
                        data['distance'] = distance
                        swing = Swing.createSwingDistance(email, club, swingSpeed, swing_datetime_str, distance)
                    print('Swing data uploaded successfully!', 'success')
                    flash('Swing data uploaded successfully!', 'success')
                except Exception as e:
                    flash('Wrong file!!')
                    return redirect(url_for("upload"))
                return redirect(url_for("upload"))

@app.route("/swing", methods=['GET','POST'])
@login_required
def swing():
    if request.method == 'GET':
        users = User.getAllUsers()
        return render_template("golfcalculator.html", alluser=users, name=current_user.name)

@app.route('/swingprocess', methods=['POST'])
@login_required
def swingprocess():
    email = request.form['email']
    club_label = request.form['club']
    speed = float(request.form['swing_speed'])
    datetime_str = request.form['datetime']
    
    club = Club.objects(email=email,label=club_label).first()
    distance = Swing.getDistance(email=email, label=club.label, speed=speed)
    Swing.createSwingDistance(email, club_label, speed, datetime_str, distance)
    return redirect(url_for("swing"))

if __name__ == '__main__':
    app.run(debug=True)
