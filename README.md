# Video Summarizer & Analyzer

This application processes video files and provides comprehensive summaries and targeted analysis based on user queries.

## Features

- **Video Summarization**: Generate comprehensive summaries of video content
- **Custom Analysis**: Get specific insights by asking questions about the video
- **Web Search Integration**: Uses DuckDuckGo search for additional context
- **User-Friendly Interface**: Built with Streamlit for easy interaction - View Model
- **Multiple Video Formats**: Supports mp4, avi, mov, mkv formats

## Requirements

- Python 3.7+
- Google AI Studio API key

## Setup Instructions

1. Clone this repository

   ```
   git clone https://github.com/NeelB28/Video_Summarizer.git
   cd Video_Summarizer
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory

4. Add your Google AI Studio API key to the `.env` file:

   ```
   GOOGLE_API_KEY="your-api-key-here"
   ```

5. Run the application:
   ```
   streamlit run app.py
   ```

## How to Use

1. **Start the application** using the command above
2. **Upload a video file** using the sidebar upload button (max 200MB)
3. **Generate a summary** by clicking the "Summarize Video" button
4. **Ask specific questions** in the text area
5. **Generate targeted analysis** by clicking the "Analyze Video" button

## How It Works

The application uses Google's Gemini multimodal AI model to process video content. When you upload a video:

1. The file is temporarily stored and displayed in the interface
2. When summarizing, the AI processes the video and generates a comprehensive overview
3. For analysis, your specific query guides the AI to focus on particular aspects of the content
4. The DuckDuckGo tool provides additional contextual information when needed

## Limitations

- Maximum video size: 200MB
- Processing time varies based on video length and complexity
- Requires an active internet connection
- API rate limits may apply based on your Google AI Studio plan

## Troubleshooting

- **API Key Issues**: Ensure your Google AI Studio API key is correctly set in the `.env` file
- **Video Format Errors**: Only mp4, avi, mov, and mkv formats are supported
- **Processing Failures**: Very large or complex videos may fail to process
- **Slow Performance**: Processing time depends on video size and complexity

## Credits

- Built with [Streamlit](https://streamlit.io/)
- AI powered by [Google Gemini](https://ai.google.dev/)
- RAG functionality via [DuckDuckGo Search](https://duckduckgo.com/)
- Developed using [Phidata](https://phidata.com/) for agent creation
