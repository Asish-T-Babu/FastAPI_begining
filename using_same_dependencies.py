from fastapi import FastAPI, Depends
import random

app = FastAPI()

def get_value():
    return str(random.randint(0, 100))

@app.get("/with-cache")
async def with_cache(value1: str = Depends(get_value), value2: str = Depends(get_value)):
    return {"value1": value1, "value2": value2}

@app.get("/no-cache")
async def no_cache(value1: str = Depends(get_value, use_cache=False), value2: str = Depends(get_value, use_cache=False)):
    return {"value1": value1, "value2": value2}
