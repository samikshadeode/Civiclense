from flask import Flask, render_template, request, jsonify, url_for,redirect,session
from ultralytics import YOLO
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from PIL import Image
import os
import uuid
from datetime import datetime
from helper import apology,login_required
from flask_session import Session
from cs50 import SQL
from helper import apology


import sqlite3
conn = sqlite3.connect('civiclens.db')
c = conn.cursor()
for row in c.execute("SELECT report_id, lat, lon FROM reports"):
    print(row)
conn.close()

db = SQL("sqlite:///civiclens.db")

app = Flask(__name__)

app.secret_key = "samiksha123"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "uploads")

model = YOLO("ml/best.pt")  # your trained weights

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    print("SESSION:", dict(session))
    my_reports = []
    if session.get("user_id"):
        my_reports = db.execute(
            "SELECT * FROM reports WHERE user_id = ? ORDER BY created_at DESC",
            session["user_id"]
        )

    top_reports = db.execute(
        "SELECT * FROM reports ORDER BY upvotes DESC LIMIT 3"
    )

    return render_template("index.html", my_reports=my_reports, top_reports=top_reports)


@app.route("/upload", methods=["POST"])
@login_required
def upload_page():
    if "image" not in request.files:
        return apology("No file part", 400)

    file = request.files["image"]

    if file.filename == "":
        return apology("No selected file", 400)

    filename = secure_filename(file.filename)
    unique_filename = str(uuid.uuid4()) + "_" + filename
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
    file.save(file_path)

    # Run inference
    results = model.predict(source=file_path, save=False,conf=0.15)
    boxes = results[0].boxes

    # Determine category (first detected class) and severity
    if len(boxes) > 0:
        class_names = [model.names[int(b.cls[0])] for b in boxes]
        category = class_names[0]
    else:
        category = "unknown"

    severity = estimate_severity(boxes, results[0].orig_shape)

    # Save the annotated image properly
    annotated_array = results[0].plot()
    annotated_filename = "annotated_" + unique_filename
    annotated_path = os.path.join(app.config["UPLOAD_FOLDER"], annotated_filename)
    Image.fromarray(annotated_array[..., ::-1]).save(annotated_path)

    # Get lat/lng from the form (sent via hidden inputs from geolocation)
    lat = request.form.get("lat")
    lng = request.form.get("lng")

     # Check for a nearby duplicate report (same category, close location, not yet resolved)
    duplicate = db.execute("""
    SELECT * FROM reports 
    WHERE category = ? 
    AND ABS(lat - ?) < 0.001 
    AND ABS(lon - ?) < 0.001
    AND status != 'resolved'
""", category, lat, lng)

    is_duplicate = len(duplicate) > 0 

    # Save report to database
    db.execute(
    """INSERT INTO reports 
       (user_id, image_url, category, severity, lat, lon, status, upvotes, created_at, is_duplicate) 
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
    session["user_id"], annotated_filename, category, severity,
    lat, lng, "pending", 0, datetime.now().isoformat(), int(is_duplicate)
)

    return render_template("result.html", 
    original_image=unique_filename, 
    annotated_image=annotated_filename,
    is_duplicate=is_duplicate,
    duplicate_report_id=duplicate[0]["report_id"] if is_duplicate else None
)

def estimate_severity(boxes, img_shape):
    if len(boxes) == 0:
        return "none"
    img_area = img_shape[0] * img_shape[1]
    areas = [
        (float(b.xyxy[0][2] - b.xyxy[0][0])) * (float(b.xyxy[0][3] - b.xyxy[0][1]))
        for b in boxes
    ]
    ratio = max(areas) / img_area
    if ratio > 0.15:
        return "severe"
    elif ratio > 0.05:
        return "moderate"
    return "minor"


  
@app.route("/check_status", methods=["GET","POST"])
@login_required
def check_status():
    if request.method=="GET":
        return render_template("check_status.html")
    else:
        report_id=request.form.get("report_id")
        rows=db.execute("SELECT * FROM reports WHERE report_id=?",report_id)
        if len(rows)==0:
            return apology("Report id not found!")
        else:
            return render_template("show_status.html",report=rows[0])
        



@app.route("/register",methods=['GET','POST'])
def register():
    if request.method=="GET":
        return render_template("register.html")

    elif request.method=="POST":
       password=request.form.get("password")
       username=request.form.get("username")
       confirm_password=request.form.get("confirmation")

       rows=db.execute("SELECT username FROM users WHERE username=?",username)
       if len(rows)==1:
           return apology("Username is already taken!")

       if not password:
           return apology("Password is necesssary",400)

       if not username:
           return apology("Username is necessary",400)

       if not confirm_password:
           return apology("Confirmaton of password is necessary",400)

       if confirm_password!=password:
           return apology("Password does not match")

       password_hash=generate_password_hash(password, method='pbkdf2:sha256')

       try:
           user=db.execute("INSERT INTO users (username,password) VALUES(?,?)",username,password_hash)

       except ValueError:
           return apology("Username already taken!")

       return render_template("login.html",message="Registration successful! Please log in.")



@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)


        rows=db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))


        if len(rows) != 1 or not check_password_hash( rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["user_id"]
        session["is_admin"] = rows[0]["is_admin"]
        session['username']=rows[0]["username"]
        print("LOGIN SET:", session["user_id"])
        return redirect("/")

    elif request.method=="GET":
        return render_template("login.html")

@app.route("/map_data")
@login_required
def map_data():
    user_lat = float(request.args.get("lat", 0))
    user_lon = float(request.args.get("lon", 0))

    # Rough bounding box filter (~0.1 degrees ≈ 11km, adjust as needed)
    reports = db.execute(
        "SELECT * FROM reports WHERE lat BETWEEN ? AND ? AND lon BETWEEN ? AND ?",
        user_lat - 0.1, user_lat + 0.1, user_lon - 0.1, user_lon + 0.1
    )
    return jsonify(reports)


@app.route("/nearby")
@login_required
def nearby():
    return render_template("nearby.html")




@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/admin/reports")
@login_required
def admin_reports():
    user = db.execute("SELECT is_admin FROM users WHERE user_id = ?", session["user_id"])
    if len(user) == 0 or not user[0]["is_admin"]:
        return apology("Admins only", 403)

   
    reports = db.execute("""
        SELECT *, 
        (CASE severity 
            WHEN 'severe' THEN 3 
            WHEN 'moderate' THEN 2 
            WHEN 'minor' THEN 1 
            ELSE 0 
        END) * (1 + upvotes) AS priority_score
        FROM reports 
        WHERE status != 'resolved' 
        ORDER BY priority_score DESC
    """)
    print("DEBUG:", reports)
    return render_template("admin_reports.html", reports=reports)


@app.route("/update_status", methods=["POST"])
@login_required
def update_status():
    # Check admin permission
    user = db.execute("SELECT is_admin FROM users WHERE user_id = ?", session["user_id"])
    if len(user) == 0 or not user[0]["is_admin"]:
        return apology("Admins only", 403)

    report_id = request.form.get("report_id")
    new_status = request.form.get("status")

    # Validate the status value against allowed options
    valid_statuses = ["pending", "in_progress", "resolved"]
    if new_status not in valid_statuses:
        return apology("Invalid status", 400)

    # Make sure the report actually exists
    rows = db.execute("SELECT * FROM reports WHERE report_id = ?", report_id)
    if len(rows) == 0:
        return apology("Report not found", 404)

    # Update it
    db.execute("UPDATE reports SET status = ? WHERE report_id = ?", new_status, report_id)

    return redirect("/admin/reports")

@app.route("/upvote", methods=["POST"])
@login_required
def upvote():
    report_id = request.form.get("report_id")

    # Make sure the report exists
    rows = db.execute("SELECT * FROM reports WHERE report_id = ?", report_id)
    if len(rows) == 0:
        return apology("Report not found", 404)

    # Check if this user already upvoted this report
    already_voted = db.execute(
        "SELECT * FROM report_upvotes WHERE user_id = ? AND report_id = ?",
        session["user_id"], report_id
    )
    if len(already_voted) > 0:
        return apology("You already upvoted this report", 400)

    # Record the vote
    db.execute(
        "INSERT INTO report_upvotes (user_id, report_id) VALUES (?, ?)",
        session["user_id"], report_id
    )

    # Increment the count on the report itself
    db.execute(
        "UPDATE reports SET upvotes = upvotes + 1 WHERE report_id = ?",
        report_id
    )

    return redirect(request.referrer or "/")


@app.route("/reports")
@login_required
def all_reports():
    reports = db.execute("SELECT * FROM reports ORDER BY upvotes DESC, report_id DESC")
    return render_template("all_reports.html", reports=reports)


@app.route("/my_reports")
@login_required
def my_reports():
    reports = db.execute("SELECT * FROM reports WHERE user_id = ? ORDER BY created_at DESC", session["user_id"])
    return render_template("my_reports.html", reports=reports)

if __name__ == "__main__":
    app.run(debug=True,port=5083) 
 