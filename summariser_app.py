import os
import fitz  # PyMuPDF for PDF
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from docx import Document # For Word documents
from io import BytesIO # Import BytesIO for handling byte streams

# --- Configuration and Setup ---
# Load environment variables (ensure .env file has GEMINI_API_KEY)
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
if not GEMINI_API_KEY:
    st.error("Gemini API key not found. Please set GEMINI_API_KEY in your .env file.")
else:
    genai.configure(api_key=GEMINI_API_KEY)
    # Initialize the Generative Model
    # Using 'gemini-2.0-flash' for efficient text generation and summarization
    model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

# Streamlit UI Setup
st.set_page_config(page_title="Student Notes Summarizer 📝", page_icon="📖")
st.title("📚 Student Notes Summarizer")
st.markdown("""
    Upload your notes (PDF or Word) and I'll help you summarize them!
""")

# --- Text Extraction Functions ---

def extract_text_pdf(file_bytes):
    """
    Extracts text from a PDF file.
    Args:
        file_bytes: Bytes of the PDF file.
    Returns:
        A string containing all extracted text.
    """
    text = ""
    try:
        # fitz.open can directly handle bytes if filetype is specified
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return ""
    return text

def extract_text_docx(file_bytes):
    """
    Extracts text from a DOCX (Word) file.
    Args:
        file_bytes: Bytes of the DOCX file.
    Returns:
        A string containing all extracted text.
    """
    text = ""
    try:
        # Wrap file_bytes in BytesIO to provide a file-like object
        doc = Document(BytesIO(file_bytes))
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        st.error(f"Error extracting text from Word document: {e}")
        return ""
    return text

# --- Main Application Logic ---

# Initialize session state variables if they don't exist
if 'full_notes_text' not in st.session_state:
    st.session_state.full_notes_text = ""
if 'summarized_text' not in st.session_state:
    st.session_state.summarized_text = ""
if 'uploaded_file_name' not in st.session_state:
    st.session_state.uploaded_file_name = ""

# File type selection
doc_type = st.radio(
    "Choose your document type:",
    ("PDF (.pdf)", "Word Document (.docx)"),
    index=0 # Default to PDF
)

# File uploader based on selected type
if doc_type == "PDF (.pdf)":
    uploaded_file = st.file_uploader("Upload your notes PDF", type="pdf")
elif doc_type == "Word Document (.docx)":
    uploaded_file = st.file_uploader("Upload your notes Word Document", type="docx")

# Process uploaded file
if uploaded_file:
    # Read file as bytes
    file_bytes = uploaded_file.read()

    # Extract text based on file type
    if doc_type == "PDF (.pdf)":
        st.session_state.full_notes_text = extract_text_pdf(file_bytes)
    elif doc_type == "Word Document (.docx)":
        st.session_state.full_notes_text = extract_text_docx(file_bytes)

    st.session_state.uploaded_file_name = uploaded_file.name

    if st.session_state.full_notes_text:
        st.success(f"{st.session_state.uploaded_file_name} uploaded and text extracted successfully!")
        st.info("Now, click 'Summarize Notes' to get your summary!")
    else:
        st.warning("Could not extract text from the document. Please try another file.")

# Summarization button logic
if st.button("Summarize Notes", help="Click to generate a summary of your uploaded notes"):
    if st.session_state.full_notes_text and GEMINI_API_KEY:
        with st.spinner("Summarizing your notes... This might take a moment. 🧠"):
            try:
                # Craft a clear prompt for summarization
                prompt = (
                    "Please provide a concise and clear summary of the following student notes. "
                    "Focus on the main concepts, key facts, and important details. "
                    "Organize the summary logically, perhaps using bullet points or short paragraphs. "
                    "Ensure the summary is easy to understand for a student revising the material. "
                    "Here are the notes:\n\n"
                    f"{st.session_state.full_notes_text}"
                )
                response = model.generate_content(prompt)
                st.session_state.summarized_text = response.text
                # The display logic for summarized_text and download button is now consolidated below
            except Exception as e:
                st.error(f"Error generating summary from Gemini: {e}")
                st.session_state.summarized_text = "" # Clear summary on error
    elif not GEMINI_API_KEY:
        st.error("Cannot summarize without a Gemini API key. Please check your setup.")
    else:
        st.warning("Please upload a document first before attempting to summarize.")

# --- Consolidated display of summarized text and download option ---
# This block will now be the ONLY place responsible for displaying the summary
# It displays if st.session_state.summarized_text has content.
if st.session_state.summarized_text:
    st.markdown("---")
    st.subheader("Summarized Notes ✨")
    st.write(st.session_state.summarized_text)
    st.download_button(
        label="Download Summarized Notes ⬇️",
        data=st.session_state.summarized_text,
        file_name=f"summarized_notes_{os.path.splitext(st.session_state.uploaded_file_name)[0]}.txt",
        mime="text/plain",
        key="download_summarized_notes", # Unique key for this single download button
        help="Click to download the summary as a text file."
    )

# Instructions if no file uploaded
if not uploaded_file and not st.session_state.full_notes_text:
    st.info("Please upload your notes (PDF or Word) to begin summarization. ☝️")

