from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

app = FastAPI()

# Autoriser les requêtes du frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017")
ao_collection = client.ao_db.ao_results
bdc_collection = client.bdc_db.bdc_results

# Convertir ObjectId en str
def convert_id(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@app.get("/api/ao")
async def get_all_aos():
    aos = list(ao_collection.find())
    return JSONResponse(content=jsonable_encoder([convert_id(ao) for ao in aos]))

@app.get("/api/bdc")
async def get_all_bdcs():
    bdcs = list(bdc_collection.find())
    return JSONResponse(content=jsonable_encoder([convert_id(bdc) for bdc in bdcs]))
