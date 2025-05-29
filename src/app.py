"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict, List, Any

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# Cliente de MongoDB asíncrono
client = AsyncIOMotorClient('mongodb://localhost:27017/')
db = client['school_activities']
activities_collection = db['activities']

def get_activities_collection():
    """
    Función para obtener la colección de actividades.
    """
    return activities_collection


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
async def get_activities(collection=Depends(get_activities_collection)):
    """Obtener todas las actividades desde MongoDB"""
    activities_cursor = collection.find({}, {'_id': 0})
    activities_list = await activities_cursor.to_list(length=100)
    
    # Convertir la lista de documentos a un diccionario con el nombre como clave
    activities_dict = {activity.pop('name'): activity for activity in activities_list}
    return activities_dict


@app.post("/activities/{activity_name}/signup")
async def signup_for_activity(activity_name: str, email: str, collection=Depends(get_activities_collection)):
    """Sign up a student for an activity"""
    # Validate activity exists
    activity = await collection.find_one({"name": activity_name})
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up")

    # Add student
    result = await collection.update_one(
        {"name": activity_name},
        {"$push": {"participants": email}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to sign up")
    
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
async def unregister_from_activity(activity_name: str, email: str, collection=Depends(get_activities_collection)):
    """Remove a student from an activity"""
    # Validate activity exists
    activity = await collection.find_one({"name": activity_name})
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Validate participant exists in activity
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found in this activity")
    
    # Remove participant
    result = await collection.update_one(
        {"name": activity_name},
        {"$pull": {"participants": email}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to unregister participant")
    
    return {"message": f"{email} eliminado de {activity_name}"}
