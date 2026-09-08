# ============================================================
# AI IT HELPDESK AGENT
# RAG + TOOLS + AGENT ROUTING
# ============================================================

# -----------------------------
# 1. IMPORT REQUIRED LIBRARIES
# -----------------------------

import platform
import shutil

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


# ============================================================
# 2. IT KNOWLEDGE BASE
# ============================================================

knowledge_base = """
IT HELPDESK KNOWLEDGE BASE

1. Password Reset
If a user forgets their password, they should use the company's password reset portal.
If self-service reset does not work, contact the IT helpdesk.

2. Wi-Fi Connection Problem
Check that Wi-Fi is enabled and connected to the correct network.
Restart the router or reconnect to the Wi-Fi network.
If the problem continues, contact IT support.

3. Computer Running Slowly
Close unnecessary applications and browser tabs.
Restart the computer.
Check available storage space.
If the computer is still slow, contact IT support.

4. Email Problems
Check your internet connection.
Verify that your email password is correct.
Restart the email application.
If emails are still not sending or receiving, contact IT support.

5. Software Installation
Only install software approved by the organization.
Contact the IT helpdesk if administrator permission is required.

6. Printer Problem
Check that the printer is powered on and connected.
Check for paper or ink problems.
Restart the printer and try again.
If the problem continues, contact IT support.

7. VPN Problem
Check your internet connection.
Make sure your VPN credentials are correct.
Restart the VPN application.
If the VPN still does not connect, contact IT support.

8. Account Locked
If an account is locked after multiple failed login attempts,
wait for the specified lockout period or contact IT support.

9. Hardware Problem
For keyboard, mouse, monitor, or other hardware problems,
check the physical connections and restart the computer.
If the issue remains, contact IT support.

10. IT Support Contact
For unresolved technical problems, create an IT support ticket
with the issue description, device information, and error message.
"""


# ============================================================
# 3. CREATE DOCUMENT CHUNKS
# ============================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

documents = text_splitter.create_documents([knowledge_base])


# ============================================================
# 4. CREATE EMBEDDING MODEL
# ============================================================

print("Loading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding model loaded successfully!")


# ============================================================
# 5. CREATE CHROMA VECTOR DATABASE
# ============================================================

print("Creating vector database...")

vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    collection_name="it_helpdesk"
)

print("Chroma vector database created successfully!")


# ============================================================
# 6. CREATE RAG RETRIEVER
# ============================================================

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)

print("RAG retriever created successfully!")


# ============================================================
# 7. SYSTEM INFORMATION TOOL
# ============================================================

def get_system_info():
    """
    Get basic system information.
    """

    return {
        "operating_system": platform.system(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }


# ============================================================
# 8. DISK SPACE TOOL
# ============================================================

def check_disk_space():
    """
    Check available disk space.
    """

    total, used, free = shutil.disk_usage("/")

    return {
        "total_gb": round(total / (1024 ** 3), 2),
        "used_gb": round(used / (1024 ** 3), 2),
        "free_gb": round(free / (1024 ** 3), 2)
    }


# ============================================================
# 9. RAG SEARCH FUNCTION
# ============================================================

def search_knowledge_base(query):
    """
    Search the IT knowledge base using RAG.
    """

    results = retriever.invoke(query)

    if not results:
        return "No relevant information found in the IT knowledge base."

    # Remove duplicate content
    unique_results = []
    seen = set()

    for doc in results:

        content = doc.page_content.strip()

        if content not in seen:
            unique_results.append(content)
            seen.add(content)

    response = "Relevant IT Knowledge:\n\n"

    for i, content in enumerate(unique_results, 1):

        response += f"{i}. {content}\n\n"

    return response


# ============================================================
# 10. AI IT HELPDESK AGENT
# ============================================================

def helpdesk_agent(user_query):
    """
    AI IT Helpdesk Agent.

    Routes user requests to:
    - RAG knowledge retrieval
    - System information tool
    - Disk space tool
    """

    query = user_query.lower()


    # --------------------------------------------------------
    # SYSTEM INFORMATION REQUEST
    # --------------------------------------------------------

    if any(word in query for word in [
        "system information",
        "system info",
        "computer information",
        "my system",
        "system details"
    ]):

        info = get_system_info()

        return f"""
============================================================
🤖 AI IT HELPDESK AGENT
============================================================

I detected a system information request.

SYSTEM INFORMATION
------------------
Operating System : {info['operating_system']}
OS Version       : {info['os_version']}
Machine          : {info['machine']}
Processor        : {info['processor']}

🔧 Tool Used: get_system_info()

============================================================
"""


    # --------------------------------------------------------
    # SLOW COMPUTER + DISK SPACE
    # --------------------------------------------------------

    elif (
        ("slow" in query or "slowly" in query)
        and any(word in query for word in [
            "disk",
            "storage",
            "space"
        ])
    ):

        knowledge = search_knowledge_base(user_query)

        disk = check_disk_space()

        return f"""
============================================================
🤖 AI IT HELPDESK AGENT
============================================================

I found troubleshooting information in the IT knowledge
base and checked the system's disk space.

📚 RAG RESULTS
--------------
{knowledge}

🔧 SYSTEM CHECK
---------------
Total Disk Space : {disk['total_gb']} GB
Used Disk Space  : {disk['used_gb']} GB
Free Disk Space  : {disk['free_gb']} GB

🔧 Tools Used:
• RAG Knowledge Retrieval
• check_disk_space()

💡 Recommendation:
Close unnecessary applications, restart the computer,
and check whether sufficient storage space is available.

============================================================
"""


    # --------------------------------------------------------
    # DIRECT DISK SPACE REQUEST
    # --------------------------------------------------------

    elif any(word in query for word in [
        "disk space",
        "storage space",
        "free space",
        "hard disk",
        "disk usage",
        "storage"
    ]):

        disk = check_disk_space()

        return f"""
============================================================
🤖 AI IT HELPDESK AGENT
============================================================

I checked your system's disk space.

DISK SPACE
----------
Total : {disk['total_gb']} GB
Used  : {disk['used_gb']} GB
Free  : {disk['free_gb']} GB

🔧 Tool Used: check_disk_space()

============================================================
"""


    # --------------------------------------------------------
    # GENERAL IT PROBLEM → RAG
    # --------------------------------------------------------

    else:

        knowledge = search_knowledge_base(user_query)

        return f"""
============================================================
🤖 AI IT HELPDESK AGENT
============================================================

I searched the IT knowledge base for your problem.

{knowledge}

💡 Recommendation:
Please follow the troubleshooting steps above.
If the problem continues, contact IT support.

📚 Source: IT Knowledge Base
🔎 Method: Retrieval-Augmented Generation (RAG)

============================================================
"""


# ============================================================
# 11. COMMAND LINE CHATBOT
# ============================================================

print()
print("=" * 60)
print("🤖 AI IT HELPDESK AGENT")
print("=" * 60)
print("RAG + TOOLS + AGENT ROUTING")
print("Type 'exit' to stop the chatbot.")
print()

while True:

    user_question = input("Ask your question: ")

    if user_question.lower().strip() == "exit":

        print()
        print("Thank you for using AI IT Helpdesk Agent!")
        print("Goodbye!")
        break

    if user_question.strip() == "":
        print("Please enter a question.")
        continue

    response = helpdesk_agent(user_question)

    print(response)