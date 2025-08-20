 Student Notes Summarizer
A Streamlit-powered web application designed to help students quickly summarize their lecture notes from PDF and Word documents using the power of Google's Gemini AI.
 The Problem Statement
Students frequently accumulate large volumes of lecture notes, readings, and study materials. Revisiting these extensive documents for revision can be time-consuming and inefficient. The core problem this prototype addresses is the difficulty students face in quickly extracting key information and concise summaries from their lengthy notes, hindering effective and timely revision.
⏳ Current Progress Status
This prototype has reached a functional initial release (MVP).
Core summarization logic: Fully implemented for both PDF and DOCX files.
User Interface: A simple and intuitive Streamlit web interface is in place for document upload and summary display.
Error Handling: Basic error handling for API issues and document extraction failures is included.
Download Functionality: Users can download the generated summary as a text file.
Pending work:
More advanced summarization options (e.g., keyword extraction, specific sections).
Handling of other document types (e.g., plain text, rich text).
User authentication or saving summaries for later access.
Improved UI/UX for larger text inputs or very long summaries.
 How Your Prototype is Solving the Problem
This application provides a direct solution by:
Automating Summarization: Instead of manually sifting through pages of notes, students can upload their documents, and the AI handles the summarization.
Supporting Common Formats: It accepts both PDF and Microsoft Word (.docx) files, covering frequently used academic document types.
Providing Concise Overviews: The AI generates a focused summary of the main concepts, facts, and details, making revision quicker and more targeted.
Enabling Offline Access: The ability to download summaries as a .txt file allows students to keep and review them even without an internet connection.
This tool aims to enhance study efficiency by delivering digestible, AI-generated summaries, allowing students to grasp core concepts faster and identify areas needing further study.
🛠️ Technologies/Tools Used
The prototype is built using the following key technologies and libraries:
Streamlit: For quickly building and deploying interactive web applications in Python.
PyMuPDF (fitz): Used for robust and efficient text extraction from PDF documents.
python-docx: Utilized for parsing and extracting text content from Microsoft Word (.docx) files.
Google Generative AI (Gemini model): The powerful AI model (specifically gemini-2.0-flash) is used for generating high-quality summaries from the extracted text.
python-dotenv: For securely loading environment variables (like the Gemini API key) from a .env file.

