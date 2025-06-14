Character Story Generator

This full-stack app lets you add your own imaginary characters, then magically generates short fantasy 
stories about them using AI. It’s built with FastAPI, React, and Supabase, and powered by Groq’s AI models.

---

# Tech Stack

Backend: FastAPI (Python)
Frontend: React.js
Database: Supabase (PostgreSQL)
AI Integration: Groq LLaMA 3 API


<!-- Setup Instructions -->

--Backend Setup (FastAPI)
1. Clone repo and enter directory  
   git clone https://github.com/Sumishaparthas15/character-story-app.git
   cd character-story-app

2. Create & activate virtual environment  
    python3 -m venv venv
    source venv/bin/activate 

3. pip install -r requirements.txt
4. SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   GROQ_API_KEY=your_groq_api_key

5. uvicorn main:app --reload
   
--Frontend Setup(React.js)

1. cd frontend
2. npm install
3. npm start


<!-- sample curl commands -->

1. Create Character
        curl -X POST http://localhost:8000/api/create_character \
        -H "Content-Type: application/json" \
        -d '{"name": "Bilbo Baggins", "details": "Hobbit lives in the Shire owning a magic ring"}'

2. Generate Story
        curl -X POST http://localhost:8000/api/generate_story \
        -H "Content-Type: application/json" \
        -d '{"character_name": "Bilbo Baggins"}'


3.Generated Story 

In the heart of the rolling green hills of the Shire, a hobbit named Percy lived a simple life in his cozy hobbit-hole. Unbeknownst to his friends and neighbors, Percy possessed a magical artifact that had been passed down through his family for generations. The ring granted him incredible luck and agility, allowing him to excel in every aspect of his life. One day, as he was tending to his garden, the ring glowed brightly, warning him of an imminent danger threatening the Shire. With his trusty ring by his side, Percy set out to face the unknown peril, ready to defend his home against all odds.

