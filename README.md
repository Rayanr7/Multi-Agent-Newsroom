# Multi-Agent Newsroom System

## Project Overview
The Multi-Agent Newsroom system is designed to automate the process of news gathering, analysis, and dissemination using intelligent agents. This system leverages various AI technologies to provide real-time news updates and insights.

## System Architecture
The architecture consists of multiple agents, each responsible for specific tasks such as news collection, analysis, and user interaction. Agents communicate with each other using a message broker and a shared database stores relevant data.

## How to Set it Up
1. Clone the repository:
   ```bash
   git clone https://github.com/rayanahmedrr1-cpu/multi-agent-newsroom.git
   ```
2. Navigate to the project directory:
   ```bash
   cd multi-agent-newsroom
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the environment variables by creating a `.env` file as specified in `.env.example`.

## Agent Descriptions
- **News Collector Agent**: Gathers news articles from various sources.
- **Analysis Agent**: Analyzes articles for sentiment and relevance.
- **User Interface Agent**: Manages interactions with the user and presents data in the dashboard.

## State Machine Flow
The system operates on a state machine model which includes states such as:
- Idle
- Collecting
- Analyzing
- Presenting
Each state represents a phase in processing news.

## Repository Structure
- `agents/`: Contains all agent implementations.
- `dashboard/`: Contains the UI files.
- `tests/`: Contains unit and integration tests.
- `requirements.txt`: Lists project dependencies.

## Hard Requirements
- Python 3.7+
- Flask
- SQLAlchemy
- Redis

## Deliverables
- Fully functional multi-agent system.
- Complete documentation (this README).
- Source code.

## Task Summaries
- **Task 1**: Implement news gathering functionality.
- **Task 2**: Develop analysis algorithms.
- **Task 3**: Create UI for user interactions.

## Instructions on How to Run the System
To run the system, execute the following command:
```bash
python app.py
```

## How to Use the UI Dashboard
1. Open your browser and navigate to `http://localhost:5000`.
2. Use the dashboard to interact with the agents and view news updates.

---
For further information, consult the Wiki or contact the project maintainers.