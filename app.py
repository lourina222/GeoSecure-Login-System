from flask import Flask, request, session, render_template, redirect, url_for
import requests
import random
import time
import smtplib
import json
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session management

# File to store user data persistently
USER_DATA_FILE = "users.json"

def load_users():
    try:
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_users(users):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)

users = load_users()


def get_location():
    response = requests.get("https://ipinfo.io/json")
    data = response.json()
    print(data.get("city") + ", " + data.get("country"))  # Extract city and count
    return data.get("city") + ", " + data.get("country")

def generate_otp():
    return random.randint(100000, 999999)

def send_otp_email(to_email, otp):
    sender_email = "lourinaemil788@gmail.com"
    sender_password = "uzkkckvwqlrtnjyu"

    msg = EmailMessage()
    msg.set_content(f"Your OTP for login is: {otp}")
    msg["Subject"] = "Your Login OTP"
    msg["From"] = sender_email
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            user_location = get_location()
            user_data = users[username]

            if user_location in user_data["trusted_locations"]:
                session["authenticated"] = True
                return redirect(url_for("dashboard"))
            else:
                otp = generate_otp()
                users[username]["otp"] = otp
                users[username]["otp_expiry"] = time.time() + 300
                session["pending_user"] = username
                send_otp_email(user_data["email"], otp)
                save_users(users)
                return redirect(url_for("verify_otp"))

    return render_template("login.html")

@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():
    if request.method == "POST":
        username = session.get("pending_user")
        if not username:
            return "No OTP process in progress."

        user_otp = int(request.form["otp"])
        user_data = users[username]

        if time.time() > user_data["otp_expiry"]:
            return "OTP expired. Please log in again."

        if user_otp == user_data["otp"]:
            session["authenticated"] = True
            user_data["trusted_locations"].append(get_location())
            save_users(users)
            return redirect(url_for("dashboard"))
        else:
            return "Invalid OTP. Try again."

    return render_template("verify_otp.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("authenticated"):
        return redirect(url_for("login"))
    return "<h3 style='text_align: center'>Welcome to your dashboard! You are logged in.</h3>"

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
