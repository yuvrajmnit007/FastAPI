from fastapi import FastAPI
# this is edited from mac
app=FastAPI()
@app.get('/')
def hello():
    return {'msg':'hello yuvraj'}

@app.get("/home")

def home():
    return "hello yuvraj!!"



@app.get("/contact")

def contact():
    return "6375064079 is my number baby"


@app.get("/about")
def about():
    return "i am a python developer"