# SkyCheck Weather Chatbot

An AI-powered weather chatbot that combines real-time weather data with generative AI and supports Japanese voice input. Built with React frontend, FastAPI backend, and CrewAI multi-agent system.

## 🚀 Features

- **Japanese Voice Input**: Speech recognition for natural voice interactions
- **Multilingual Support**: Japanese and English language support
- **AI-Powered Responses**: Google Gemini 2.0 Flash for intelligent conversations
- **Real-time Weather**: OpenWeatherMap API integration with forecasts
- **Weather Advisory**: Intelligent clothing and activity recommendations
- **Multi-Agent System**: CrewAI framework with specialized agents

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React Frontend │    │  FastAPI Backend │    │  External APIs  │
│                 │    │                  │    │                 │
│ • Voice Input   │◄──►│ • CrewAI System  │◄──►│ • OpenWeatherMap│
│ • Chat UI       │    │ • Intent Class   │    │ • Google Gemini │
│ • Theme Toggle  │    │ • Error Handling │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Multi-Agent System (CrewAI)

1. **Conversation Agent**: Extracts locations from natural language
2. **Weather Agent**: Fetches real-time weather data from APIs  
3. **Response Agent**: Creates natural responses with practical advice

### Tech Stack

**Frontend:**
- React 18 + Vite
- Tailwind CSS + shadcn/ui
- Web Speech API for voice input
- Axios for API communication

**Backend:**
- FastAPI + Python 3.8+
- CrewAI multi-agent framework
- Google Gemini 2.0 Flash
- OpenWeatherMap API

## 🛠️ Setup & Installation

### Prerequisites
- Node.js 16+ and npm/yarn
- Python 3.8+ and pip
- Google Gemini API key
- OpenWeatherMap API key

### 1. Clone Repository
```bash
git clone <repository-url>
cd skycheck-weather-chatbot
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
GOOGLE_API_KEY=your_google_gemini_api_key_here
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key_here
LLM_MODEL=gemini-2.0-flash-exp
EOF
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cat > .env << EOF
VITE_API_BASE_URL=http://localhost:8000
EOF
```

## 🚀 Running the Application

### Start Backend Server
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

### Start Frontend
```bash
cd frontend
npm run dev
```

Frontend will be available at: http://localhost:5173

## 🤖 How the Chatbot Works

### 1. Input Processing
- **Voice Input**: Web Speech API converts Japanese/English speech to text
- **Language Detection**: Automatic detection using Unicode character analysis
- **Intent Classification**: Hybrid rule-based + LLM system classifies user intent

### 2. Multi-Agent Processing

```
User Query → Intent Classification → Agent Routing
                    ↓
┌─────────────────────────────────────────┐
│            CrewAI Agents                │
│                                         │
│ Conversation Agent → Weather Agent      │
│        ↓                   ↓            │
│   Extract Location    Fetch Weather     │
│        ↓                   ↓            │
│        Response Agent ←────┘            │
│        ↓                                │
│   Natural Response + Advice             │
└─────────────────────────────────────────┘
                    ↓
              Frontend Display
```

### 3. Intent Categories
- **WEATHER_QUERY**: Weather info, forecasts, travel decisions
- **GREETING**: Hello, introductions
- **CAPABILITY_INFO**: Help requests, feature explanations
- **GENERAL_CHAT**: Casual conversation

### 4. Weather Advisory Logic
Based on API data, the chatbot provides:

**Temperature-based advice:**
- Below 5°C: Heavy winter clothing
- 5-15°C: Warm layers, jacket
- 15-25°C: Comfortable casual wear
- Above 25°C: Light, breathable clothing

**Condition-based recommendations:**
- Rain: Umbrella, waterproof clothing
- Snow: Warm layers, waterproof boots
- Sunny: Sun protection, light colors

### 5. Response Generation
- **Natural Language**: Context-aware responses in user's language
- **Cultural Adaptation**: Appropriate communication style (Japanese keigo, English casual)
- **Integrated Advice**: Weather data + practical recommendations in one response

## 🎯 API Usage

### Chat Endpoint
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "今日の東京の天気はどうですか？",
    "location": "",
    "context": []
  }'
```

### Response Format
```json
{
  "response": "東京の天気情報と服装アドバイス...",
  "success": true,
  "error": null
}
```

## 🔑 Getting API Keys

### Google Gemini API
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create project and generate API key
3. Add to backend `.env` file

### OpenWeatherMap API
1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Get free API key
3. Add to backend `.env` file

## 📁 Project Structure

```
skycheck-weather-chatbot/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── chat/           # Chat interface components
│   │   │   ├── voice/          # Voice input component
│   │   │   ├── weather/        # Weather display component
│   │   │   └── ui/             # shadcn/ui components
│   │   ├── services/
│   │   │   └── api.js          # API communication
│   │   └── App.jsx
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── crew/
│   │   │   ├── agents/         # CrewAI agent definitions
│   │   │   ├── tasks/          # CrewAI task definitions
│   │   │   └── tools/          # Weather API tools
│   │   ├── services/           # Business logic layer
│   │   └── api/                # FastAPI routes
│   ├── main.py                 # FastAPI entry point
│   └── requirements.txt
└── README.md
```

## 📄 License

MIT License - see LICENSE file for details.