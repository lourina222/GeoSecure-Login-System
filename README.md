# 🔐 GeoSecure Login System

An intelligent, location-aware multi-factor authentication system built with Flask.  
It enhances login security by combining password-based login, IP-based location verification, and email-based OTP for unfamiliar locations.

---

## 🌍 Features

- ✅ Username & password login
- 🌐 IP-based trusted location verification (via ipinfo.io)
- 📩 Email-based OTP fallback for unrecognized locations
- 🔐 Automatic location whitelisting after OTP success
- 📁 Persistent user data using JSON file storage
- 💻 Clean user experience using Flask templates

---

## 🛠️ Tech Stack

- **Backend**: Flask, Python
- **Email**: Gmail SMTP (smtplib, EmailMessage)
- **Location API**: ipinfo.io (via `requests`)
- **Session & Security**: Flask session management
- **Storage**: JSON (for users and trusted locations)
- **Security:** `.env` file for protecting email credentials

---

## 🚀 How It Works

1. User logs in with username and password.
2. The system checks if the current location (based on IP) is **trusted**.
3. - If trusted ➝ access granted directly.
   - If unrecognized ➝ send OTP to user's email.
4. After OTP verification, the location is **added to trusted list**.

---

