# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from extensions import db 
import os
from models import (
  delete_user_by_id,
  get_user_by_id,
  initialize_database,
  register_user,
  login_user,
  update_user_password,
  get_filtered_users,
  create_task as create_task_model,
  update_task as update_task_model
)


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
  return render_template("TT_register.html")

@app.route("/login")
def login_page():
  return render_template("TT_login.html")

@app.route("/update")
def update_page():
  return render_template("TT_update.html")

@app.route("/read")
def read_page():
  return render_template("TT_read.html")

@app.route("/readAll")
def read_all_page():
  return render_template("TT_viewtasks.html")

@app.route("/delete")
def delete_page():
  return render_template("TT_delete.html")

# ---------------------------------------------------------Backend---------------------------------------------------------------------
# create a new task
@app.route("/api/tasks", methods=["POST"])
def create_task_route():
    data = request.json
    success, result = create_task_model(
        data.get("taskName"),
        data.get("description"),
        int(data.get("points")),
        data.get("image_url")
    )
    if success:
        return jsonify({"message": "Task created successfully", "task ID": result}), 201
    return jsonify({"message": result}), 400 if result == "Task already exists" else 500


# update task details
@app.route("/api/tasks/<task_id>", methods=["PUT"])
def update_task_route(task_id):
  data = request.json
  rowcount, error = update_task_model(
    task_id,
    data.get("taskName"),
    data.get("description"),
    int(data.get("points")),
    data.get("image_url")
  )
  if error:
    return jsonify({"message": error}), 500
  if rowcount == 0:
    return jsonify({"message": "Task not found"}), 404
  return jsonify({"message": "Task updated successfully"}), 200






# ----------------------------------------------------------- Backend sample ---------------------------------------------------------------------
"""@app.route("/api/register", methods=["POST"])
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
  return jsonify({"message": "Password updated successfully"}), 200"""

# ----------------------------------------------------------- Backend sample ---------------------------------------------------------------------

if __name__ == "__main__":
  app.run(debug=True, host="localhost") # True=will restart server
