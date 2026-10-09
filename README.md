# AI Research Assistant with Web Search

An AI-powered research assistant that searches the web, analyzes relevant sources, and generates research answers using a local large language model.

The application combines a React frontend, FastAPI backend, Tavily web search, and Ollama to create an interactive research experience with multiple research modes, agentic query decomposition, source quality scoring, research history, and downloadable reports.

## Overview

Researching a topic manually can require visiting multiple websites, comparing information, and organizing findings.

This project automates much of that workflow. Users submit a research question, select a research mode, and receive an AI-generated answer supported by retrieved web sources.

The application also breaks complex questions into smaller research questions, searches for information about those questions, and synthesizes the collected findings into a final answer.

## Features

* **Live Web Search:** Retrieve relevant information from the web using Tavily.
* **Local AI Model:** Generate research answers using Ollama and LangChain.
* **Quick Research:** Produce concise answers with important findings.
* **Deep Research:** Generate more detailed research reports.
* **Compare Sources:** Analyze similarities, differences, and conflicting information across sources.
* **Agentic Query Decomposition:** Break complex research questions into smaller sub-questions.
* **Source Quality Scoring:** Rank sources using relevance and other quality signals.
* **Duplicate Source Removal:** Reduce duplicate search results.
* **Agent Activity:** Display the main stages of the research workflow.
* **Research History:** Save and revisit previous searches using browser local storage.
* **Markdown Report Download:** Download a research report containing the question, research plan, answer, and source information.
* **Markdown Rendering:** Display formatted answers, lists, headings, links, and other supported Markdown content.
* **REST API:** Expose research functionality through a FastAPI backend.
* **Interactive Frontend:** Use a React interface to submit questions and explore research results.

## Technology Stack

### Frontend

* React
* Vite
* JavaScript
* CSS
* React Markdown
* Remark GFM
* Browser Local Storage

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic

### AI and Research

* LangChain
* Ollama
* Tavily Search API

## System Architecture

The application follows a frontend-backend architecture.

1. The user enters a research question in the React interface.
2. The frontend sends the question and selected research mode to FastAPI.
3. The backend uses the local Ollama model to decompose the question into smaller research questions.
4. Tavily searches the web for relevant information.
5. The backend removes duplicate results and evaluates source quality.
6. LangChain and Ollama synthesize the retrieved information into a research answer.
7. FastAPI returns the answer, sources, research plan, and activity information.
8. React displays the results and allows the user to download the research report.

### Architecture Diagram

```text
                 User
                  |
                  v
           React + Vite
                  |
             HTTP Request
                  |
                  v
           FastAPI Backend
                  |
          Research Planning
                  |
                  v
        Query Decomposition
                  |
                  v
            Tavily Search
                  |
                  v
       Source Processing and
          Quality Scoring
                  |
                  v
           Ollama + LLM
                  |
                  v
        Research Answer and
             Source List
                  |
                  v
           React Frontend
                  |
          Download Report
```

## Project Structure

```text
AI_Research_Assistant/
│
├── backend/
│   ├── __init__.py
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.css
│   ├── package.json
│   └── index.html
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

Additional files may be present in your local project.

**Security note:** The `.env` file contains configuration and secrets. It should remain private and must not be committed to Git.

## Prerequisites

Before running the project, install or configure:

* Python 3.11 or another Python version compatible with the project's dependencies.
* Node.js and npm.
* Ollama.
* A local language model supported by your Ollama installation.
* A Tavily API key.

The AI model runs locally through Ollama. Tavily requires internet access to perform web searches.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/rayankhan-ai/AI_Research_Assistant.git
cd AI_Research_Assistant
```

### 2. Create a Python virtual environment

On Windows PowerShell:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, resolve the execution-policy issue for your current session before activating the environment.

### 3. Install Python dependencies

```powershell
pip install -r requirements.txt
```

### 4. Install frontend dependencies

Open a terminal in the project directory and run:

```powershell
cd frontend
npm install
```

Return to the project root when finished:

```powershell
cd ..
```

## Environment Configuration

Create a `.env` file in the project root.

Add the following configuration:

```env
TAVILY_API_KEY=your_tavily_api_key
OLLAMA_MODEL=your_installed_ollama_model
```

Replace the example values with your actual configuration.

* `TAVILY_API_KEY`: Your Tavily API key.
* `OLLAMA_MODEL`: The exact model name available in your local Ollama installation.

Never publish your real API key.

## Configure Ollama

Install Ollama and download a model compatible with your computer.

Check the models installed on your machine:

```powershell
ollama list
```

If you need to download a model, use the model name supported by your Ollama installation. For example:

```powershell
ollama pull llama3.2
```

The example model may differ from the one configured for this project. Set `OLLAMA_MODEL` to the model you actually intend to use.

Make sure Ollama is running before submitting research requests.

**Note:** Local model performance depends on available RAM, model size, and hardware resources.

## Running the Application

The frontend and backend run in separate terminals.

### Terminal 1 — Start the backend

From the project root, activate your virtual environment and run:

```powershell
uvicorn backend.main:app --reload
```

The backend should be available at:

```text
http://127.0.0.1:8000
```

Open the interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

### Terminal 2 — Start the frontend

Open another terminal:

```powershell
cd "C:\Users\ahmad\Desktop\AI_Research_Assistant\frontend"
npm run dev
```

Vite will display the local development URL. By default, it is usually:

```text
http://localhost:5173
```

Open the URL displayed in your terminal.

Keep both development servers running while using the application.

## How to Use the Application

1. Open the React frontend in your browser.
2. Enter a research question.
3. Select a research mode.
4. Start the research process.
5. Review the research plan and agent activity.
6. Read the generated answer.
7. Examine the source cards and open relevant websites.
8. Download the Markdown research report if required.
9. Revisit previous searches through the research history.

## Research Modes

### Quick Research

Designed for concise answers and important findings.

### Deep Research

Designed for more detailed answers that organize findings across multiple research questions.

### Compare Sources

Designed to compare information across sources and identify similarities, differences, and conflicting claims.

The quality of each answer depends on the retrieved sources, the selected model, and the research question.

## API Overview

The backend includes endpoints for basic service information, health checks, web searches, and complete research workflows.

| Endpoint         | Purpose                      |
| ---------------- | ---------------------------- |
| `GET /`          | Basic backend information    |
| `GET /health`    | Check backend health         |
| `POST /search`   | Search the web               |
| `POST /research` | Run the AI research workflow |

Open `http://127.0.0.1:8000/docs` to inspect the actual request schemas and test the endpoints.

## Important Notes and Limitations

* Tavily search requires a working API key and internet connectivity.
* Ollama must be installed and running locally.
* A local model may generate incorrect or incomplete statements.
* Source quality scores are heuristic indicators, not guarantees of accuracy.
* Search results can be incomplete, outdated, or biased.
* Always inspect original sources before relying on important findings.
* Research history is stored in the browser's local storage and is not automatically synchronized across devices.
* The application is configured for local development. Public deployment requires additional configuration, security measures, and access to a suitable AI model service.

## Security

* Keep API keys in `.env`.
* Do not commit secrets to GitHub.
* Keep `.env`, `venv/`, `node_modules/`, and generated build files out of version control.
* Do not expose the development server publicly without appropriate security controls.
* Review and verify generated research before using it for important decisions.

## Future Improvements

Potential enhancements include:

* Export reports to PDF and Word.
* Add user authentication and persistent research history.
* Add automated research evaluation.
* Improve citation verification and source reliability analysis.
* Add asynchronous research jobs and progress updates.
* Introduce deployment-specific model hosting and production configuration.
* Add automated tests for the API and frontend.

## Author

**Rayan Ahmad**

AI/ML Developer | Aspiring Agentic AI Engineer

## License

No license has been added yet. Unless a license is included in the repository, others generally do not receive an explicit open-source license to reuse, modify, or distribute this project.
