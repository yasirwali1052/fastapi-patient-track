
# 🏥 FastAPI Patient Management System

A simple **FastAPI**-based REST API for managing patient data such as personal info, health metrics, and doctor assignments.  
Built with **FastAPI** — a modern, high-performance Python web framework for building APIs quickly and efficiently.

---

## 🚀 Purpose
- Learn and practice **FastAPI** for backend API development.
- Perform CRUD operations (Create, Read, Update, Delete) on patient data.
- Store data in JSON without requiring a database.

---

## ⚙️ How to Run

### 1️⃣ Clone the Repo
```bash
git clone https://github.com/yasirwali1052/fastapi-patient-track.git
cd fastapi-patient-track
````

### 2️⃣ Create & Activate Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Start the Server

```bash
uvicorn main:app --reload
```

Visit:

* API Home → `http://127.0.0.1:8000`
* Swagger Docs → `http://127.0.0.1:8000/docs`

---

## 📦 Requirements

```
fastapi
uvicorn
pydantic
```


