from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from fastapi.responses import JSONResponse
from fastapi import status
from supabase import create_client
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq  


load_dotenv()

app = FastAPI()


supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)


print("Loaded GROQ API Key:", os.getenv("GROQ_API_KEY"))  
client = Groq(api_key=os.getenv("GROQ_API_KEY"))



origins = ["http://localhost:3000"] 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Character(BaseModel):
    name: str
    details: str


@app.post("/api/create_character")
def create_character(characters: Character):
    try:
        response = supabase.table("characters").insert({
            "name": characters.name,
            "details": characters.details
        }).execute()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Character added successfully", "data": response.data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate_story")
def generate_story(payload: dict):
    try:
        name = payload.get("character_name")  
        character_data = supabase.table("characters").select("*").eq("name", name).single().execute()

        if not character_data.data:
            raise HTTPException(status_code=404, detail="Character not found")

        prompt = f"Write a fantasy short story in 5 to 6 lines about this character:\n{character_data.data['details']}"

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
        )

        story = response.choices[0].message.content.strip() 
        print(story, "llllllllllllllllllllllll")  

        return {"story": story}
    
    except Exception as e:
        print("Error in /generate_story:", e)
        raise HTTPException(status_code=500, detail=str(e))
