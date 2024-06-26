from flask_login import login_required, current_user
from flask import render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime, date
from pymongo import MongoClient
from controllers.dashboard import dashboard
from controllers.auth import auth

# from models.chart import CHART
from models.users import User
from models.golfsetData import *
import csv
import io

# Load the current user if any
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()
