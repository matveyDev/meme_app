# Meme Generator App

A web application that generates memes using AI. Built with Vue.js and FastAPI.

## Features

- Generate memes using AI
- Select from predefined items and animals
- Save generated memes
- Responsive design for mobile and desktop
- TON blockchain integration

## Prerequisites

- Docker and Docker Compose
- OpenAI API key

## Setup

1. Clone the repository:
```bash
git clone https://github.com/matveyDev/meme_app.git
cd meme_app
```

2. Create a `.env` file in the root directory with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

3. Build and run the application using Docker Compose:
```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:8080
- Backend API: http://localhost:8000

## Development

To run the application in development mode:

1. Frontend:
```bash
cd frontend
npm install
npm run serve
```

2. Backend:
```bash
cd fastapi
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Project Structure

```
meme_app/
├── frontend/           # Vue.js frontend application
├── fastapi/           # FastAPI backend application
├── docker-compose.yml # Docker Compose configuration
└── README.md         # This file
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 