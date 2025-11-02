from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os

# -------------------- Config --------------------
DB_USER = "root"           # change to your MariaDB user
DB_PASSWORD = "student"   # change to your MariaDB password
DB_HOST = "localhost"
DB_NAME = "course_db"
CSV_FILE = "coursera_courses.csv"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# -------------------- Database Setup --------------------
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String(255), nullable=False)
    duration = Column(String(255), nullable=False)
    skills = Column(String(255))

Base.metadata.create_all(bind=engine)

# -------------------- FastAPI Setup --------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Pydantic Model --------------------
class CourseModel(BaseModel):
    course_name: str
    duration: str
    skills: str | None = None

# -------------------- Load CSV into DB --------------------
def load_csv_to_db():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        db = SessionLocal()
        for _, row in df.iterrows():
            # Efficiently skip the CSV's id and let DB auto-increment
            existing = db.query(Course).filter(
                Course.course_name == row["Course Name"],
                Course.duration == row["Duration"]
            ).first()
            if not existing:
                new_course = Course(
                    course_name=row["Course Name"],
                    duration=row["Duration"],
                    skills=row.get("Skills", "")
                )
                db.add(new_course)
        db.commit()
        db.close()

load_csv_to_db()

# -------------------- Serve HTML --------------------
@app.get("/")
def serve_home():
    return FileResponse("index.html")

# -------------------- CRUD APIs --------------------
@app.get("/api/courses")
def get_courses():
    db = SessionLocal()
    courses = db.query(Course).all()
    db.close()
    return {"data": [{"id": c.id, "course_name": c.course_name, "duration": c.duration, "skills": c.skills} for c in courses]}

@app.post("/api/courses")
def add_course(course: CourseModel):
    db = SessionLocal()
    new_course = Course(course_name=course.course_name, duration=course.duration, skills=course.skills)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    db.close()
    return {"message": "Course added", "data": {"id": new_course.id, "course_name": new_course.course_name, "duration": new_course.duration, "skills": new_course.skills}}

@app.put("/api/courses/{course_id}")
def update_course(course_id: int, course: CourseModel):
    db = SessionLocal()
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        db.close()
        raise HTTPException(status_code=404, detail="Course not found")
    db_course.course_name = course.course_name
    db_course.duration = course.duration
    db_course.skills = course.skills
    db.commit()
    db.refresh(db_course)
    db.close()
    return {"message": "Course updated", "data": {"id": db_course.id, "course_name": db_course.course_name, "duration": db_course.duration, "skills": db_course.skills}}

@app.delete("/api/courses/{course_id}")
def delete_course(course_id: int):
    db = SessionLocal()
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        db.close()
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(db_course)
    db.commit()
    db.close()
    return {"message": "Course deleted"}

