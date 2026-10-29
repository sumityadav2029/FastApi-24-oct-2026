from fastapi import FastAPI, HTTPException, Path , Query
from fastapi.responses import JSONResponse
import pydantic
from pydantic import BaseModel, Field, computed_field
import json
from typing import Annotated, Optional


app = FastAPI()

def load_data():
    with open('patient_data.json','r') as f:
        data=json.load(f)

    return data

def save_data(data):
    with open('patient_data.json','w') as f:
        json.dump(data, f)

class Patient(BaseModel):
    id:Annotated[str,Field(...,description="ID of the patient", example="PT-34567")]
    first_name:Annotated[str,Field(...,description="First name  of the patient", example='john')]
    last_name:Annotated[str,Field(...,description="last name of the patient ", example="doe")]
    date_of_birth:Annotated[str,Field(...,description=" D.O.B of the patient", example="23/06/1987")]
    gender:Annotated[str,Field(...,description="genre of the patient", example='male / female')]
    blood_type:Annotated[str,Field(...,description="blood type of the patient", example="ab+")]
    contact_number:Annotated[str,Field(...,description="contact number of the patient",example="9315874598")]
    email:Annotated[str,Field(...,description="email of the patient if patient's age greater tahn 60 then give the parents email",example='email@gmail.com')]
    status:Annotated[str,Field(...,description="patients are waiting for treatement or treatement complete", example="waiting / Done")]
    height_cm:Annotated[float,Field(...,gt=0,description="height in cm")]
    weight_kg:Annotated[int,Field(...,gt=0,lt=120,description="weight in kg")]
    medication_duration_days:Annotated[int,Field(...,description="how long paient taking medicine")]


    @computed_field
    @property
    def BMI(self) -> float:
        bmi=round(self.weight_kg/((self.height_cm/100)**2),2)
        return bmi


    @computed_field
    @property
    def verdict(self) -> str:

        if self.BMI < 18.5:
            return "underweight" 

        elif self.BMI < 25 :
            return "normal"

        elif self.BMI < 30:
            return 'obese'


class Update_Patient(BaseModel):

    first_name:Annotated[Optional[str],Field(default=None)]
    last_name:Annotated[Optional[str],Field(default=None)]
    date_of_birth:Annotated[Optional[str],Field(default=None)]
    gender:Annotated[Optional[str],Field(default=None)]
    blood_type:Annotated[Optional[str],Field(default=None)]
    contact_number:Annotated[Optional[str],Field(default=None)]
    email:Annotated[Optional[str],Field(default=None)]
    status:Annotated[Optional[str],Field(default=None)]
    height_cm:Annotated[Optional[float],Field(gt=0,default=None)]
    weight_kg:Annotated[Optional[float],Field(gt=0,default=None)]
    medication_duration_days:Annotated[Optional[int],Field(gt=0,default=None)]

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




@app.post("/post")
def create_patient(patient:Patient):

    # STEP= O1    load data
    data = load_data()  # in the form of dict

    #STEP= 02    check if the patient already exist
    if patient.id in data:
        raise HTTPException(status_code=400,detail="patients data already exist")

    # STEP= 03      ann new patient 
    data[patient.id]   =   patient.model_dump(exclude=['id'])            # model_dumpo() change pydantic object to dictionary

    # save to json file 
    save_data(data)

    return JSONResponse(status_code=201, content={'message':'patient created succesfully'})


# endpoint to delete data
@app.delete("/delete/{patient_id}")
def delete_patient(patient_id:str):

    #load the data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="patient not found")

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content="patient deleted")



# to update the data
@app.put("/edit/{patient_id}")
def update_data(update_patient:Update_Patient,patient_id:str):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="patient not fopund")

    existing_patient_info=data[patient_id]

    updated_patient_info= update_patient.model_dump(exclude_unset= True)

    for key , value in updated_patient_info.items():
        existing_patient_info[key] = value

    existing_patient_info['id']=patient_id
    patient_pydantic_object = Patient(**existing_patient_info)
    existing_patient_info  =  patient_pydantic_object.model_dump(exclude='id')


    data[patient_id]= existing_patient_info

    save_data(data)

    return JSONResponse(status_code=200, content="data updated succesfully")
