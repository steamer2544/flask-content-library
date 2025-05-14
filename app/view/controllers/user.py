import os
from flask import Blueprint, render_template
import requests


bp = Blueprint('user', __name__, url_prefix='/user')

base_url = f"http://localhost:{os.getenv('PORT', 1234)}/api{bp.url_prefix}"

# Headers with the token
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJhZG1pbiIsImlhdCI6MTc0NzE5NDI4MCwiZXhwIjoxNzQ3MjgwNjgwfQ.s4hmwTeIQku0L_4Y8oHow9WXesQQoYaHcctL1l2XMdw"
headers = {
    "Authorization": f"Bearer {token}"
}


# เราต้อง store ไปที่ session  มั้งง
@bp.route("/", methods=["GET"])
def list_users():
    # Call the API to get the list of users
    api_url = f"{base_url}"
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        user_data = response.json().get('data', {}).get('data', [])
    else:
        user_data = []
    return render_template('user.html', users=user_data)