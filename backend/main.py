from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from supabase import create_client
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
open_api_key = os.getenv("OPENAI_API_KEY")


supabase = create_client(supabase_url, supabase_key)

origins = [
    "http://localhost:3000",  
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Character(BaseModel):
    name:str
    details:str

@app.post("/api/create_character")  
def create_character(characters:Character):
    print(characters.name,".......................")
    try:
          respose = supabase.table("characters").insert({
               "name":characters.name,
               "details":characters.details
          }).execute()
          return {"message":"charcter addedd successfully","data":respose.data}
    except Exception as e:
        print("Error occurred:", e)
        raise HTTPException(status_code=500,detail=str(e))
    

@app.post("/api/generate_story")    
def generate_story(payload:dict):
    print(payload,"................................")
    try:
        name = payload.get("charcter_name")
        character_data = supabase.table("characters").select("*").eq("name",name).single().execute()

        if not character_data:
            raise HTTPException(status_code=404,detail="Character not found")    
        
        prompt = f"Write a 5-line short story about this character: {character_data.data['details']}"

        from openai import OpenAI
        import openai

        openai.api = open_api_key

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages =[{"role":"user","context":prompt}]
        )
         
        story = response.choices[0].messages.content
        return {"story":story} 
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))