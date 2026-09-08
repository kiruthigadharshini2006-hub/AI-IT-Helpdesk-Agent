# 🤖 AI IT Helpdesk Agent

## 📌 Project Overview

The AI IT Helpdesk Agent is an intelligent IT support system designed to help users troubleshoot common technical problems. The system combines an AI agent, Retrieval-Augmented Generation (RAG), and system diagnostic tools to provide relevant and practical solutions.

## 🎯 Objective

The main objective of this project is to develop an AI-based IT helpdesk assistant that can understand user queries, retrieve relevant troubleshooting information from an IT knowledge base, and use system tools to provide useful diagnostic information.

## 🏗️ System Architecture

The system follows the architecture:

User → AI Agent → RAG + Tools → Final Response

The AI Agent analyzes the user's question and decides whether to retrieve information from the knowledge base or use a system diagnostic tool.

## 🧠 Key Components

### 1. AI Agent

The AI Agent acts as the decision-making component of the system. It analyzes the user's query and determines the appropriate action.

### 2. Retrieval-Augmented Generation (RAG)

RAG is used to retrieve relevant information from the IT Helpdesk Knowledge Base. This allows the system to provide troubleshooting information based on the stored IT support documentation.

The knowledge base contains information about:

- Password reset
- Wi-Fi connection problems
- Slow computers
- Email problems
- Software installation
- Printer problems
- VPN problems
- Locked accounts
- Hardware problems
- IT support tickets

### 3. System Diagnostic Tools

The project includes tools that can directly check system information.

The available tools are:

- System Information Tool – retrieves operating system, OS version, machine type, and processor information.
- Disk Space Tool – checks total, used, and available disk space.

## 🛠️ Technologies Used

- Python
- LangChain
- LangChain Community
- ChromaDB
- HuggingFace Sentence Transformers
- Retrieval-Augmented Generation (RAG)
- Python System Tools
- Windows Command Prompt
- Google Colab

## ⚙️ How the System Works

1. The user enters an IT-related question.
2. The AI Agent analyzes the query.
3. If the question requires knowledge-based troubleshooting, the RAG system searches the IT knowledge base.
4. If the question requires system information, the appropriate diagnostic tool is executed.
5. The retrieved information or tool result is processed.
6. The final troubleshooting response is displayed to the user.

## 💻 How to Run the Project

First, install the required Python packages:

```bash
pip install -r requirements.txt

Then run the application:

```bash

python helpdesk_agent.py

💬 Example Queries

The following questions can be used to test the system:

    1.My Wi-Fi is connected but I cannot access the internet.

    2.I forgot my password.

    3.My printer is not working.

    4.My computer is running very slowly.

    5.My computer is running slowly. Check my disk space.

    6.Can you check my system information?

To stop the application, type:

exit
