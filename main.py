from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def read_root():
    return {'message':'welcome to swiggy order services',
            'status':'healthy'}


if "__name__"=="__main __":
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)  # we can modify port and host as well according to our need