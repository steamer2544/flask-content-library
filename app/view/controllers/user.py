import os
from flask import Blueprint, render_template, request
import requests

bp = Blueprint('user', __name__, url_prefix='/user')
base_url = f"http://localhost:{os.getenv('PORT', 1234)}/api{bp.url_prefix}"

@bp.route("/", methods=["GET"])
def list_users():
    token = request.cookies.get('access_token')
    api_url = f"{base_url}"

    session = requests.Session()
    session.cookies.set('access_token', token)

    # Call the API to get the list of users
    response = session.get(
        f"{api_url}",
    )

    if response.status_code == 200:
        user_data = response.json().get('data', {}).get('data', [])
    else:
        user_data = []
    return render_template('user.html', users=user_data)