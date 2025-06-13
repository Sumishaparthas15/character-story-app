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