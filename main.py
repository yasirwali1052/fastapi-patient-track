from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

app = FastAPI()

# -------------------- Patient Model --------------------
class Patient(BaseModel):
    id: Annotated[str, Field(..., description="The unique identifier for the patient", example="1")]
    name: Annotated[str, Field(..., description="The name of the patient", example="John Doe")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="The age of the patient", example=30)]
    blood_group: Annotated[str, Field(..., description="The blood group of the patient", example="O+")]
    gender: Annotated[Literal['male', 'female', 'other'], Field(..., description="Gender of the patient")]
    phone: Annotated[str, Field(..., description="The phone number of the patient", example="+1234567890")]
    email: Annotated[str, Field(..., description="The email address of the patient", example="abc@gmail.com")]
    address: Annotated[str, Field(..., description="The address of the patient", example="123 Main St, City, Country")]
    doctor: Annotated[str, Field(..., description="The doctor assigned to the patient", example="Dr. Smith")]
    salary: Annotated[float, Field(..., gt=0, description="The salary of the patient", example=50000.0)]
    height: Annotated[float, Field(..., gt=0, description="The height of the patient in cm", example=170.0)]
    weight: Annotated[float, Field(..., gt=0, description="The weight of the patient in kg", example=70.0)]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi_value = self.weight / ((self.height / 100) ** 2)
        return round(bmi_value, 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

# -------------------- Patient Update Model --------------------
class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    blood_group: Optional[str] = None
    gender: Optional[Literal['male', 'female', 'other']] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    doctor: Optional[str] = None
    salary: Optional[float] = None
    height: Optional[float] = None
    weight: Optional[float] = None

# -------------------- File Handling --------------------
def load_data():
    try:
        with open("patient.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(data):
    with open("patient.json", "w") as f:
        json.dump(data, f, indent=4)

# -------------------- Routes --------------------
@app.get("/")
def hello():
    return {"message": "Patient management system"}

@app.get("/about")
def about():
    return {'message': "A fully functional patient management system"}

@app.get("/view")
def view():
    return load_data()

@app.get("/patient/{patient_id}")
def get_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", example="1")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patient(
    sort_by: str = Query(..., description="Sort on the basis of salary and age"),
    order: str = Query("asc", description="Sort order")
):
    valid_fields = ["salary", "age"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Choose from {valid_fields}")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order")

    data = load_data()
    sort_desc = True if order == "desc" else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by), reverse=sort_desc)
    return sorted_data

@app.post("/create")
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")

    data[patient.id] = patient.model_dump()
    save_data(data)

    return JSONResponse(status_code=201, content={
        "message": "Patient created successfully",
        "patient": patient.model_dump()
    })

# -------------------- Update Patient --------------------
@app.put("/update/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Update only provided fields
    for field, value in patient_update.dict(exclude_unset=True).items():
        data[patient_id][field] = value

    # Recalculate BMI and verdict if height/weight updated
    if "height" in patient_update.dict(exclude_unset=True) or "weight" in patient_update.dict(exclude_unset=True):
        height = data[patient_id]["height"]
        weight = data[patient_id]["weight"]
        bmi_value = round(weight / ((height / 100) ** 2), 2)
        data[patient_id]["bmi"] = bmi_value
        if bmi_value < 18.5:
            data[patient_id]["verdict"] = "Underweight"
        elif 18.5 <= bmi_value < 24.9:
            data[patient_id]["verdict"] = "Normal weight"
        elif 25 <= bmi_value < 29.9:
            data[patient_id]["verdict"] = "Overweight"
        else:
            data[patient_id]["verdict"] = "Obesity"

    save_data(data)
    return JSONResponse(
        status_code=200,
        content={
            "message": "Patient updated successfully",
            "patient": data[patient_id]
        }
    )

# -------------------- Delete Patient --------------------
@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    deleted_patient = data.pop(patient_id)
    save_data(data)
    return {"message": "Patient deleted successfully", "deleted": deleted_patient}
