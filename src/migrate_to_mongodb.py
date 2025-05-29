#!/usr/bin/env python3
"""
Script para migrar los datos de actividades en memoria a MongoDB.
Este script toma los datos de actividades definidos en app.py y los guarda en MongoDB.
"""

from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import sys

# Datos iniciales (copiados de app.py para asegurar consistencia)
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in local leagues",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Practice basketball skills and play friendly matches",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["liam@mergington.edu", "ava@mergington.edu"]
    },
    "Drama Club": {
        "description": "Participate in theater productions and acting workshops",
        "schedule": "Mondays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["noah@mergington.edu", "isabella@mergington.edu"]
    },
    "Art Workshop": {
        "description": "Explore painting, drawing, and other visual arts",
        "schedule": "Fridays, 2:00 PM - 3:30 PM",
        "max_participants": 16,
        "participants": ["amelia@mergington.edu", "benjamin@mergington.edu"]
    },
    "Math Olympiad": {
        "description": "Prepare for math competitions and solve challenging problems",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 10,
        "participants": ["charlotte@mergington.edu", "elijah@mergington.edu"]
    },
    "Debate Club": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 14,
        "participants": ["william@mergington.edu", "sophia@mergington.edu"]
    }
}

async def migrate_to_mongodb():
    """Migra los datos a MongoDB de forma asíncrona"""
    try:
        # Conectar a MongoDB
        client = AsyncIOMotorClient('mongodb://localhost:27017/')
        
        # Crear/acceder a la base de datos
        db = client['school_activities']
        
        # Acceder a la colección activities
        activities_collection = db['activities']
        
        # Eliminar datos previos si existen
        await activities_collection.delete_many({})
        
        # Preparar documentos para inserción
        documents = []
        for name, details in activities.items():
            doc = {
                "name": name,
                **details  # Expandir todos los campos del diccionario details
            }
            documents.append(doc)
        
        # Insertar todos los documentos
        result = await activities_collection.insert_many(documents)
        
        print(f"Migración exitosa! {len(result.inserted_ids)} actividades insertadas en MongoDB.")
        print("Documentos insertados:")
        
        # Mostrar los documentos insertados
        async for doc in activities_collection.find():
            print(f"- {doc['name']}")
            
        return True
        
    except Exception as e:
        print(f"Error durante la migración: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    success = asyncio.run(migrate_to_mongodb())
    sys.exit(0 if success else 1)
