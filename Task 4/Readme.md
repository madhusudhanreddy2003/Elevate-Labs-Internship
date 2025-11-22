# 🧩 Task 4 – User REST API (Flask)

A simple **RESTful User Management API** built using **Flask** for the Elevate Labs Internship.

This task demonstrates:

- Building a REST API with Flask  
- Using **HTTP methods**: GET, POST, PUT, DELETE  
- Testing APIs with **Postman** or **curl**  
- Understanding **in-memory data storage** and JSON responses  

---

## 🚀 Features

- Create a new user  
- Get all users  
- Get a single user by ID  
- Update an existing user  
- Delete a user  
- JSON request/response format  
- Simple in-memory “database” using a Python dictionary  

> ⚠️ Data is **not persistent** – it resets every time you restart the app, because it is stored in memory.

---

## 🛠 Tech Stack

- **Language:** Python 3.x  
- **Framework:** Flask  
- **Tools:**  
  - Postman Desktop (for API testing)  
  - or `curl` from terminal/PowerShell  

---

## 📁 Project Structure

```bash
Task 4/
│
├── app.py          # Main Flask application (User REST API)
└── README.md       # Documentation for Task 4 (this file)
```

## 📦 Installation & Setup
### 1️⃣ Install dependencies
```bash
pip install flask
```
### 2️⃣ Run the Flask app
```bash
python app.py
```
You should see something like:
```bash
Running Task 4 Flask App
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```
### ⚙ In-Memory Data Model<br>
The app stores users in a simple Python dictionary:

```bash
users = {
    1: {"id": 1, "name": "Madhu", "email": "madhu@example.com", "age": 21},
    2: {"id": 2, "name": "Madhan", "email": "madhan@example.com", "age": 23},
    ...
}

```
next_id is used to auto-increment user IDs.<br>
### 🌐 API Endpoints
<br>
Base URL (when running locally):

```bash
http://127.0.0.1:5000
```


## 🧪 Testing the API with Postman (Desktop)

Important: Use Postman Desktop App (not Postman Web) so it can reach 127.0.0.1.

### Basic steps:

- Open Postman Desktop.
- Create a new HTTP Request.
- Use the appropriate method and URL, for example:
  - GET http://127.0.0.1:5000/users
  - POST http://127.0.0.1:5000/users
- For POST and PUT:
  - Go to Body → raw
  - Select JSON
  - Paste the JSON body (same as examples above).
- Click Send and inspect the response JSON and status code.

###  👨‍💻 Author
- Kethari Madhu Sudhan Reddy
- Python Developer • ML Enthusiast •  Full Stack Developer • IT Enthusiast

### ⭐ Contributing

 Contributions are welcome!


### 📜 License

This project is an Open Source — use it freely!
