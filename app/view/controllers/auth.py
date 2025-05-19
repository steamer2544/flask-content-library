import os
from flask import Blueprint, render_template
import requests


bp = Blueprint('auth', __name__, url_prefix='/auth')


# เราต้อง store ไปที่ session  มั้งง
@bp.route("/login", methods=["GET"])
def login():
    return render_template('login.html')