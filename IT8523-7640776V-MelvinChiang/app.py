# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from models import initialize_database, register_user, login_user, update_user_password, get_user_by_id, get_filtered_users, delete_user_by_id
from extensions import db
import os

app = Flask(__name__)
CORS(app) # This will allow CORS (Cross-Origin Resource Sharing) for all routes.  
          # frontend=http://127.0.0.1:5500), backend=(http://localhost:5000)

config_class = os.getenv('FLASK_CONFIG', 'DevelopmentConfig')
app.config.from_object(f'config.{config_class}')

db.init_app(app)

with app.app_context():
  initialize_database()

@app.route("/") #home page
def serve_index():
  return render_template("TT_index.html")

# Frontend
@app.route("/register")
def register_page():
  return render_template("register.html")

@app.route("/login")
def login_page():
  return render_template("login.html")

@app.route("/update")
def update_page():
  return render_template("update.html")

@app.route("/read")
def read_page():
  return render_template("read.html")

@app.route("/readAll")
def read_all_page():
  return render_template("readAll.html")

@app.route("/delete")
def delete_page():
  return render_template("delete.html")

# Backend
@app.route("/api/register", methods=["POST"])
def register():
  print('api.register')
  data = request.json
  success, message = register_user(data.get("name"), data.get("email"), data.get("password"), data.get("url"))
  if success:
    return jsonify({"message": "User registered successfully"}), 201
  return jsonify({"message": message}), 400 if message == "Email already exists" else 500

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    success, message = login_user(data.get("email"), data.get("password"))
    if success:
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": message}), 401

@app.route("/api/update/<int:user_id>", methods=["PUT"])
def update_password(user_id):
  data = request.json
  rowcount, error = update_user_password(user_id, data.get("password"))
  if error:
    return jsonify({"message": error}), 500
  if rowcount == 0:
    return jsonify({"message": "User not found"}), 404
  return jsonify({"message": "Password updated successfully"}), 200

if __name__ == "__main__":
  app.run(debug=True, host="localhost") # True=will restart server
