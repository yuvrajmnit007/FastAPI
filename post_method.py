from fastapi import FastAPI ,Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
import json 
app=FastAPI()



class Address(BaseModel):
    city: Annotated[str, Field(..., description="Enter Your City Name", examples=["Jaipur"])]
    state: Annotated[str, Field(..., description="Enter Your State Name", examples=["Rajasthan"])]
    pin: Annotated[str, Field(..., description="Enter PIN Code", examples=["302017"])]




    
#lets make a pydantic class which will provide us pid,name,city,height,weight and we will calculate the bmi and verdict and post the data 
class patient_add(BaseModel):
    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])] #here ... means this field is required to post the data 
    name: Annotated[Optional[str], Field(default=None)]  #Annotated -> it is an feature from pythons typing module which allows us to add meta data 
    address: Annotated[Optional[Address], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]
    


    #this will calculate the bmi of the patient from the given data 
    @computed_field 
    @property
    def bmi(self)->float:
        bmi=round((self.weight/self.height**2),2)
        return bmi
    
    #this will give the verdict to the patient according to there bmi
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return 'under weight'
        elif self.bmi<25:
            return 'normal'
        elif self.bmi<30:
            return 'overweight'
        else :
            return 'obese'
        



# it is to laod the data from the json file
def load_data():
    with open ('patient.json','r') as f:
        data=json.load(f)

    return data
#it will save the data in the json the file 
def save_data(data):
    with open ('patient.json','w')as f:
        json.dump(data,f)
@app.get('/')
def hello():
    return {'msg':'patient management system api'}   

@app.get('/about')
def about():
    return {'msg':'A fully functional api to manage patient record'}

@app.get('/view')
def view():
    data=load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id:str=Path(...,description='ID of the patient in the DB',examples='P001')):
    data=load_data()
    if patient_id in data :
        return data[patient_id]
    raise HTTPException(status_code=404,detail='patient not found')

@app.get('/sort')
def sort_patients(sort_by:str=Query(..., description='sort on the basis of height,weight or bmi'),order:str=Query('asc', description='sort asc and desc order')):
        vaild_fields=['height','weight','bmi','age']
        if sort_by not in vaild_fields:
            raise HTTPException(status_code=400,detail='invalid field selected from {valid_fields}')
        
        if order not in ['asc','desc']:
            raise HTTPException(status_code=400,detail='Invalid order select between asc and desc')
            
        data=load_data()
        sort_order=True if order=='desc' else False

        sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)
        return sorted_data


#we will create an end point to add the patient record in the data 
@app.post('/create')
def create_patient(patient:patient_add):
    #load the existing data 


    data=load_data()

    #check if patient is already there in data  

    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')


    #add this patient to database

    data[patient.id] = patient.model_dump(exclude=['id'])
    #bcoz in our json file data is save like pid:{} so we excluded pid

    #save the data to json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message':'patient created successfully'})
