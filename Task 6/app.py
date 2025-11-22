from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime

app = Flask(__name__)

# Needed for flash messages (like success after contact form submit)
app.secret_key = "supersecretkey_change_this"


# ---------- Home Route ----------
@app.route("/")
def home():
    # You can pass dynamic data here if needed
    projects = [
        {
            "title": "Jarvis AI Assistant",
            "description": "A voice-controlled desktop assistant that automates tasks like opening apps, searching web, and chatting.",
            "tech": "Python, SpeechRecognition, SQLite, HuggingFace"
        },
        {
            "title": "Crack Detection using Deep Learning",
            "description": "A MobileNet-based model to detect structural cracks in images using transfer learning.",
            "tech": "Python, TensorFlow, OpenCV"
        },
        {
            "title": "Grocery Store Management System",
            "description": "CRUD-based web app to manage grocery inventory, billing, and reports.",
            "tech": "Python, Flask, MySQL"
        }
    ]
    skills = [
        "Python", "Flask", "HTML", "CSS", "JavaScript",
        "SQL", "Machine Learning", "Data Analysis"
    ]
    return render_template("index.html", projects=projects, skills=skills)


# ---------- Contact Form Handler ----------
@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    if not name or not email or not message:
        flash("All fields are required. Please fill the form completely.", "error")
        return redirect(url_for("home"))

    # Option 1: Just log to console (for learning)
    print("New contact message:")
    print("Name:", name)
    print("Email:", email)
    print("Message:", message)

    # Option 2: Save to a simple text file (so you can show in internship)
    save_contact(name, email, message)

    flash("Thank you! Your message has been received.", "success")
    return redirect(url_for("home"))


def save_contact(name, email, message):
    """Save contact form submissions to a file."""
    os.makedirs("data", exist_ok=True)
    filepath = os.path.join("data", "contacts.txt")
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"Time: {datetime.now()}\n")
        f.write(f"Name: {name}\n")
        f.write(f"Email: {email}\n")
        f.write(f"Message: {message}\n")
        f.write("-" * 40 + "\n")


if __name__ == "__main__":
    app.run(debug=True)
