# 📝 Flask Notes App!

A simple and secure note-taking web application built with **Flask**, **SQLite**, **HTML/CSS**, and **Bootstrap**. Users can create, edit, delete, and comment on notes — and even tag them for better organization.

## 🚀 Features

- 🔐 **User Authentication** – Sign up, log in, and log out securely.
- 📝 **Note Management** – Create, view, edit, and delete personal notes.
- 💬 **Comments** – Leave comments on your own notes.
- 🏷️ **Tags** – Organize notes with tags (e.g., `#school`, `#ideas`).
- 🔍 **Edit** – Able to Edit your note freely.
- ✅ **Validation & Security** – Input validation and password hashing using Flask-Login.

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Flask
- **Frontend**: HTML5, Bootstrap 4
- **Database**: SQLite (via SQLAlchemy ORM)
- **Authentication**: Flask-Login
- **Structure**: Blueprints, Modularized Codebase

## 📁 Folder Structure

```
project/
│
├── website/
│   ├── static/
|   |   ├──images/
|   |   |    ├── 17973908.jpg
|   |   |    ├── flat-lay.jpg
|   |   |    ├── notebook.png
│   |   ├── index.js
│   ├── templates/
|   |   ├── partials/
|   |   |   ├── edit_note_partial.html
|   |   |   ├── view_note_partial.html
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── sign_up.html
│   │   ├── edit_note.html
│   │   └── view_note.html
│   ├── __init__.py
│   ├── views.py
│   ├── auth.py
│   ├── models.py
│   └── database.py
│
├── main.py
└── database.db
```

## 🧪 How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/flask-notes-app.git
cd flask-notes-app
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> Create a `requirements.txt` with this content:
>
> ```
> Flask
> Flask-Login
> Flask-SQLAlchemy
> ```

### 4. Run the App

```bash
python main.py
```

### 5. Open in Browser

Visit `http://127.0.0.1:5000/`

## ✅ To-Do / Improvements (optional)

- Add profile pictures or avatars
- Add due dates or reminders
- Make tags clickable to filter notes

## 📄 License

MIT License — [Sean]
