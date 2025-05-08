# pip install -r requirements.txt
# required API key - Google AI Studio API key 
# tried to implement this in google colab but ngrok is not working 
# and local tunnel is showing TCP error
# pusing it to github

import streamlit as st 
# error - streamlit require page_config to be the first command
st.set_page_config(
    page_title="Video Summarizer",
    page_icon=":guardsman:",  
    layout="wide",
    initial_sidebar_state="expanded",
)

from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from google.generativeai import upload_file, get_file
import google.generativeai as genai

import time
from pathlib import Path
import tempfile
from dotenv import load_dotenv
load_dotenv()
import os

# Configure API key
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY is None:
    raise ValueError("API_KEY is not set. Please set the GOOGLE_API_KEY environment variable.")
else:
    genai.configure(api_key=API_KEY)
    #st.write("API key successfully configured.") - not expose key in streamlit

# Set the title of the Streamlit app
st.title("Video Summarizer & Analyzer")
st.header("This app summarizes and analyzes video using the LLM on LangChain.")

# Sidebar for user input
st.sidebar.header("User Input")
st.sidebar.write("Please upload a video file to summarize or analyze.")
st.sidebar.write("Supported formats: mp4, avi, mov, mkv")
st.sidebar.write("Maximum file size: 200 MB.")
st.sidebar.write("For size more than 200 MB, use cloud.")
st.sidebar.write("Note: The processing may take some time depending on the file size.")

# Creating agent
@st.cache_resource
def create_agent():
    return Agent(
        name="video_analyzer",
        description="This agent summarizes and analyzes video using the LLM.",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[DuckDuckGo()], # used for searching information, basically a RAG process
        markdown=True,
    )

# Initialize the agent
multimodal_agent = create_agent()

# Upload video file
# File uploader in sidebar
video_file = st.sidebar.file_uploader(
    "Upload a video file",
    type=["mp4", "avi", "mov", "mkv"],
    label_visibility="collapsed",
    help="Upload a video file to summarize and analyze.",
    accept_multiple_files=False,
)

# File upload check
if video_file is not None:
    # Save the uploaded file to a temporary location
    temp_video_path = tempfile.mktemp(suffix=".mp4")
    with open(temp_video_path, "wb") as temp_video:
        temp_video.write(video_file.read())

    # Display the uploaded video in streamlit
    st.subheader("Uploaded Video")
    st.video(temp_video_path, format="video/mp4", start_time=0)
    
    # Create columns for the buttons: streamlit layout
    col1, col2 = st.columns(2)
    
    # Summarize button in first column
    with col1:
        if st.button("Summarize Video", key="summarize_video_button"):
            try:
                with st.spinner("Processing video and generating summary..."):
                    # Upload and process video file : upload, process, and analyze the video can be
                    # done using opencv or ffmpeg, but here we are using the API directly
                    processed_video = upload_file(temp_video_path)
                    while processed_video.state.name == "PROCESSING":
                        time.sleep(1)
                        processed_video = get_file(processed_video.name)

                    # summarization prompt: currently hardcoded, but can be made dynamic
                    # based on user input or other parameters
                    summary_prompt = """
                    Please provide a comprehensive summary of this video. Include:
                    1. Main topic and key points
                    2. Important details and context
                    3. Any conclusions or takeaways
                    
                    Format the summary in clear sections with bullet points where appropriate.
                    """

                    # processing AI agent 
                    response = multimodal_agent.run(summary_prompt, videos=[processed_video])

                # Display the result in streamlit
                st.subheader("Video Summary")
                st.markdown(response.content)

            except Exception as error:
                st.error(f"An error occurred during summarization: {error}")
    
    # Add a divider
    st.divider()
    
    # User input for analysis
    user_query = st.text_area(
        "Enter your query about the video:",
        placeholder="Ask specific questions or request insights about the video content.",
        help="Provide a detailed query to guide the AI analysis."
    )

    # Analyze button
    if st.button("Analyze Video", key="analyze_video"):
        if not user_query:
            st.warning("Please provide a query to analyze the video.")
        else:
            try:
                with st.spinner("Analyzing the video and generating insights..."):
                    # Upload and process video file
                    processed_video = upload_file(temp_video_path)
                    while processed_video.state.name == "PROCESSING":
                        time.sleep(1)
                        processed_video = get_file(processed_video.name)

                    # Generate a prompt for the AI agent
                    analysis_prompt = (
                        f"Examine the uploaded video and provide insights based on the following query:\n"
                        f"{user_query}\n"
                        f"Include relevant context and actionable details in your response."
                    )

                    # Use the AI agent to analyze the video
                    analysis_result = multimodal_agent.run(analysis_prompt, videos=[processed_video])

                # Display the analysis result
                st.subheader("Analysis Result")
                st.markdown(analysis_result.content)

            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")
else:
    st.info("Please upload a video file to get started.")

# Clean up temp file when session ends
def cleanup():
    if "temp_video_path" in locals():
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)

# Register cleanup function
import atexit
atexit.register(cleanup)

# Customize text area height
st.markdown(
    """
    <style>
    .stTextArea textarea {
        min-height: 120px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

