from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta, date
from app import db

import csv
import io
from statistics import mean
import json

# from models.chart import CHART

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
@login_required
def render_dashboard():
    return render_template('dashboard.html', name=current_user.name, panel="Dashboard")

# Only GET, /chart produces the BMI chart at the Frontend via myChart_CSV.js
