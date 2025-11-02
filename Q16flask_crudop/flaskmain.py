from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd
import os

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CSV_FILE = "coursera_courses.csv"

# ------------------ Load CSV ------------------
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
    if "id" not in df.columns:
        df.insert(0, "id", range(1, len(df) + 1))
else:
    df = pd.DataFrame(columns=["id", "Course Name", "Duration", "Skills"])
    df.to_csv(CSV_FILE, index=False)

courses = df.to_dict(orient="records")
course_counter = int(df['id'].max()) if not df.empty else 0  # convert to int

# Helper: convert any non-Python types to native
def to_native(obj):
    if isinstance(obj, dict):
        return {k: to_native(v) for k, v in obj.items()}
    elif hasattr(obj, "item"):
        return obj.item()  # convert numpy types
    return obj

# ------------------ Serve HTML ------------------
@app.get("/")
def serve_home():
    return FileResponse("index.html")

# ------------------ CRUD APIs ------------------
@app.get("/api/courses")
def get_courses():
    return {"data": [to_native(c) for c in courses]}

@app.post("/api/courses")
def add_course(course: dict):
    global courses, course_counter
    if "Course Name" not in course or "Duration" not in course:
        raise HTTPException(status_code=400, detail="Course Name and Duration required")

    course_counter += 1
    course_data = {
        "id": int(course_counter),
        "Course Name": str(course.get("Course Name", "")),
        "Duration": str(course.get("Duration", "")),
        "Skills": str(course.get("Skills", ""))
    }

    courses.append(course_data)
    pd.DataFrame(courses).to_csv(CSV_FILE, index=False)
    return {"message": "Course added", "data": to_native(course_data)}

@app.put("/api/courses/{course_id}")
def update_course(course_id: int, course: dict):
    global courses
    for c in courses:
        if int(c["id"]) == course_id:
            for key in ["Course Name", "Duration", "Skills"]:
                if key in course:
                    c[key] = str(course[key])
            pd.DataFrame(courses).to_csv(CSV_FILE, index=False)
            return {"message": "Course updated", "data": to_native(c)}
    raise HTTPException(status_code=404, detail="Course not found")

@app.delete("/api/courses/{course_id}")
def delete_course(course_id: int):
    global courses
    courses = [c for c in courses if int(c["id"]) != course_id]
    pd.DataFrame(courses).to_csv(CSV_FILE, index=False)
    return {"message": "Course deleted"}

