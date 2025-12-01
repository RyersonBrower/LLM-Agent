# LLM-Agent

An intelligent agent system built with Python, Flask, and Docker. The project provides an interactive web interface that communicates with a backend agent service powered by LLMs. The system is fully containerized and designed for easy expansion.

## 🚀 Features
- Interactive Flask-based web UI  
- Backend agent powered by OpenAI API  
- Fully containerized using Docker and docker-compose  
- Clean separation between web and agent services  
- Environment-variable configuration  
- Easy to extend with tools, memory, or additional agents  

## 📂 Project Structure
LLM-Agent/
├── docker-compose.yml
├── .env
├── web/
│   ├── Dockerfile
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── script.js
└── agent/
    ├── Dockerfile
    └── app.py

## ⚙️ How It Works

### Web Service (Port 5000)
- Hosts the frontend UI  
- Sends user messages to the agent service  
- Displays results

### Agent Service (Port 5001)
- Processes messages from the web  
- Calls the LLM (e.g., OpenAI)  
- Returns JSON responses  

## 🐳 Running the Project

### 1. Add a `.env` file:
OPENAI_API_KEY=your_api_key_here

### 2. Build and start:
docker compose up --build

### 3. Open the app:
http://localhost:5000

## 🧩 Agent API

### POST /agent  
Request:
{
  "message": "Write a Python function that reverses a string."
}

Response:
{
  "response": "Here's a sample Python function..."
}

## 🛠️ Tech Stack
- Python  
- Flask  
- Docker / Docker Compose  
- OpenAI API  
- HTML, CSS, JavaScript  

## 🔧 Future Enhancements
- Memory and persistence  
- Multi-agent workflows  
- Tool/function calling  
- Authentication  
- React frontend  

## 📄 License
This project is for educational and personal use. Modify and extend as needed.
