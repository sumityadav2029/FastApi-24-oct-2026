from fastapi import FastAPI, HTTPException, Path , Query
import pydantic
from pydantic import BaseModel
import json


app = FastAPI()

def load_data():
    with open('patient_data.json','r') as f:
        data=json.load(f)

    return data

# class Patient(BaseModel):
#     email:str
#     mobile:int

@app.get("/")
def hello():
    return {'message':"Patient management API"}


@app.get("/about")
def about():
    return {'message':'Fully functional API to manage Patient records'}



@app.get("/view")
def view():
    data = load_data()
    return data

# path params
@app.get("/patient/{patient_id}")
def view_patient(patient_id:str = Path(...,description='ID of the patient from DB',example='PT-60289')):
    #load the data
    data=load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail="patient not found")
    return data[patient_id]


#query params
@app.get("/sort")
def sort_patient(sort_by:str = Query(...,description="sort on the basis of height, weight or bmi"),order:str=Query('asc',description='sort in asc or dsc order')):

    valid_fields=['height_cm','weight_kg','bmi','medication_duration_days']

    order_fields=['asc','dsc']


    if sort_by not in valid_fields:
        raise HTTPException(status_code=400 , detail=f"invalid field,  choose from {valid_fields} ")

    if order not in order_fields:
        raise HTTPException(status_code=400, detail=f'invalid fields choose from {order_fields}')

    data  = load_data()

    sort_order = True if order =='dsc' else False

    sorted_data = sorted(data.values(), key=lambda x:x.get(sort_by,0), reverse=sort_order)

    return sorted_data
