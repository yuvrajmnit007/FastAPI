from fastapi import FastAPI ,Path,HTTPException,Query
import json 
app=FastAPI()

def load_data():
    with open ('patient.json','r') as f:
        data=json.load(f)

    return data
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
def view_patient(patient_id:str=Path(...,description='ID of the patient in the DB',example='P001')):
    data=load_data()
    if patient_id in data :
        return data[patient_id]
    raise HTTPException(status_code=404,detail='patient not found')

@app.get('/sort')
def sort_patients(sort_by:str=Query(..., description='sort on the basis of height,weightor bmi'),order:str=Query('asc', description='sort asc and desc order')):
        vaild_fields=['height','weight','bmi','age']
        if sort_by not in vaild_fields:
            raise HTTPException(status_code=400,detail='invalid field selected from {valid_fields}')
        
        if order not in ['asc','desc']:
            raise HTTPException(status_code=400,detail='Invalid order select between asc and desc')
            
        data=load_data()
        sort_order=True if order=='desc' else False

        sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)
        return sorted_data