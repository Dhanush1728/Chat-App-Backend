# Chat App Backend

A real-time chat backend built with FastAPI and WebSockets.
Users can join rooms and exchange messages instantly.

## Tech Stack

- Python 3.x
- FastAPI
- WebSockets
- SQLAlchemy
- SQLite
- Uvicorn

## Features

- Real-time messaging using WebSockets
- Multiple chat rooms support
- Chat history stored in database
- View all active rooms

## Project Structure

chat_app/
├── main.py         # API routes, WebSocket logic
├── database.py     # Database connection setup
├── models.py       # Database models
└── requirements.txt

## Installation & Setup

1. Clone the repository
   git clone https://github.com/yourusername/chat-app-backend.git
   cd chat-app-backend

2. Install dependencies
   pip install -r requirements.txt

3. Run the server
   uvicorn main:app --reload

4. Open Swagger UI
   (https://chat-app-backend-5zv8.onrender.com/docs)

## API Endpoints

| Method    | Endpoint                  | Description               |
|-----------|---------------------------|---------------------------|
| WebSocket | /ws/{room}/{username}     | Join a chat room          |
| GET       | /rooms/{room}/history     | Get chat history of room  |
| GET       | /rooms                    | Get all active rooms      |

## Testing WebSocket

Open browser console and paste:

const ws = new WebSocket("ws://localhost:8000/ws/general/Dhanush");
ws.onmessage = (event) => console.log(event.data);
ws.onopen = () => {
    ws.send("Hello everyone!");
};

## Author

Your Name
GitHub: github.com/Dhanush1728
