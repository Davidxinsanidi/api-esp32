from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime

app = FastAPI()

# Conexión MongoDB Atlas

MONGO_URI = "mongodb+srv://esp32:esp32pass@cluster0.kaqfde1.mongodb.net/iot"


client = MongoClient(MONGO_URI)
db = client.iot
collection = db.sensores
from pydantic import BaseModel, Field

class SensorData(BaseModel):
    temperatura: float = Field(..., ge=-50, le=100)
    humedad: float = Field(..., ge=0, le=100)
@app.get("/")
def root():
    return {"mensaje": "API funcionando"}

@app.post("/sensor")
def guardar_sensor(data: SensorData):
    try:
        doc = data.dict()
        doc["fecha"] = datetime.now()
        collection.insert_one(doc)
        return {"status": "dato guardado"}
    except Exception as e:
        return {"error": str(e)}