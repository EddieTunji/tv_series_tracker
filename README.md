# TV Series Tracker CLI App 🎬

This is a command-line application built with Python and SQLAlchemy to help users track their favorite TV series, manage their watch progress by seasons and episodes, leave reviews, and update their viewing status.

---

## 💡 Features

- User login and selection
- Add and view TV series
- Track seasons and episodes for each series
- Update viewing status (e.g., Watching, Completed, Plan to Watch)
- Write and manage series reviews
- Delete seasons and update entries dynamically

---

## 🛠️ Technologies Used

- Python 3
- SQLAlchemy ORM
- SQLite (via SQLAlchemy)
- Rich (for colored terminal styling)
- Click (optional CLI interaction)
- Pipenv for dependency management

---

## 🧠 Learning Goals Met

This project demonstrates:

- Designing and connecting multiple tables using SQLAlchemy relationships
- Implementing full CRUD functionality via a CLI interface
- Creating and managing a relational database using ORM (no raw SQL)
- Practicing clean code structure, logic separation, and interactive terminal apps

---


## 🧪 Running the App

1. Clone the repository
2. Run `pipenv install`
3. Seed the database: `pipenv run python db/seed.py`
4. Launch the app: `pipenv run python app.py`

---

## 👤 Sample Use Flow

- Select or create a user
- Browse or add new series
- Add seasons and episodes for a show
- Mark progress by updating episode or season status
- Write a review and assign a personal status like "Watching" or "Completed"

---

## ✨ Extras

- Stylized CLI output with `rich` for a smoother experience
- Clear menus and guided prompts for each feature
- Option to delete seasons

---

## ✅ Still To Do (Stretch Ideas)

- Episode-level progress tracking
- Favorite series list
- Export data to JSON or text



