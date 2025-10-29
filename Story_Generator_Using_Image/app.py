f="""
=============================================================================
AI STORY GENERATOR - STREAMLIT WEB APPLICATION
=============================================================================

PROJECT OVERVIEW:
    An interactive web application that transforms uploaded images into 
    creative stories and converts them into natural-sounding audio narration
    using Google's Gemini AI technology.

MAIN FEATURES:
    1. Image Upload System
       - Supports JPG, JPEG, and PNG formats
       - Allows 1-10 images per story
       - Visual gallery display of uploaded images
    
    2. Story Generation
       - 10 different story genres (Comedy, Horror, Adventure, etc.)
       - AI analyzes images and creates coherent narratives
       - 700-1000 word stories with proper structure
       - Persistent display using Streamlit session state
    
    3. Audio Narration
       - Text-to-Speech conversion of generated stories
       - Natural-sounding voice (Kore - female voice)
       - WAV format audio with embedded player
       - Automatic cleanup of temporary files

APPLICATION ARCHITECTURE:
    ┌─────────────────────────────────────────────────┐
    │              USER INTERFACE (Streamlit)         │
    ├─────────────────────────────────────────────────┤
    │  Sidebar                    Main Content Area   │
    │  ├─ Image Uploader          ├─ Title & Desc    │
    │  ├─ Story Type Selector     ├─ Image Gallery   │
    │  ├─ Generate Story Btn      ├─ Story Display   │
    │  └─ Generate Audio Btn      └─ Audio Player    │
    ├─────────────────────────────────────────────────┤
    │           BACKEND LOGIC (Story_Generation.py)   │
    │  ├─ generate_story_from_images()               │
    │  └─ generate_audio_from_generated_story()      │
    ├─────────────────────────────────────────────────┤
    │              GOOGLE GEMINI AI API               │
    │  ├─ gemini-2.5-pro (Story Generation)          │
    │  └─ gemini-2.5-flash-preview-tts (Audio)       │
    └─────────────────────────────────────────────────┘

TECHNOLOGY STACK:
    - Frontend Framework: Streamlit 
    - Image Processing: Pillow (PIL)
    - AI Model: Google Gemini (gemini-2.5-pro & TTS)
    - Audio Format: WAV (16-bit PCM, 24kHz, Mono)
    - State Management: Streamlit Session State

WORKFLOW:
    1. User uploads 1-10 images
    2. User selects story genre from dropdown
    3. User clicks "Generate Story" button
       → Images sent to Gemini AI with genre-specific prompt
       → AI analyzes images and creates narrative
       → Story displayed in styled card on main page
       → Story saved in session state for persistence
    4. User clicks "Generate Audio" button
       → Story text sent to Gemini TTS model
       → Raw PCM audio converted to WAV format
       → Audio player displayed with narration
       → Temporary file cleaned up after playback

USER EXPERIENCE FEATURES:
    ✓ Responsive grid layout for image display
    ✓ Loading spinners during AI processing
    ✓ Error handling with user-friendly messages
    ✓ Styled story display with custom HTML/CSS
    ✓ Embedded audio player for narration
    ✓ Persistent story display across interactions

SECURITY & BEST PRACTICES:
    - API keys stored in environment variables (.env file)
    - Input validation (image count limit, file type check)
    - Comprehensive error handling with try-except blocks
    - Automatic cleanup of temporary audio files
    - User feedback for all operations (success/error states)

DEPENDENCIES:
    - streamlit: Web application framework
    - Pillow (PIL): Image processing and manipulation
    - Story_Generation: Custom module with AI functions
    - traceback: Detailed error logging
    - os: File system operations

USAGE:
    Run this application with:
        streamlit run app.py
    
    Then navigate to:
        http://localhost:8501

NOTES:
    - Requires valid Google API key in .env file
    - Internet connection required for AI API calls
    - Recommended: 4GB+ RAM for smooth operation
    - Audio generation may take 10-30 seconds

=============================================================================
"""

# 1. --- Importing libraries ---

f="""
1. streamlit (st): Main framework for creating the web interface
2. PIL.Image: Used to open and process uploaded image files
3. Story_Generation: Custom module containing AI story and audio generation functions
4. traceback: For detailed error logging and debugging
5. os: For file system operations (checking file existence, deleting temp files)
"""

import streamlit as st
from PIL import Image
from Story_Generation import generate_story_from_images, generate_audio_from_generated_story
import traceback
import os

# 2. --- Page Configuration ---

f="""
Configure the Streamlit page settings:
1. page_title: Sets the browser tab title
2. page_icon: Sets the browser tab icon (emoji)
This must be the first Streamlit command in the script
"""

st.set_page_config(
    page_title="AI Story Generator 🎭",
    page_icon="📖"
)

# 3. --- Sidebar ---

f="""
The sidebar contains all user input controls:
- Image uploader
- Story type selector
- Action buttons
"""

f="""
Creates a header in the sidebar to organize the input controls
"""

st.sidebar.header("✨ Story Generator Settings")

# 4. --- Upload images ---

f="""
File uploader widget that:
1. Accepts only image files (jpg, jpeg, png)
2. Allows multiple file uploads
3. Returns a list of uploaded files or None if nothing uploaded
"""

uploaded_images = st.sidebar.file_uploader(
    "Upload 1-10 images (JPG, JPEG, or PNG):",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# 5. --- Limit the number of uploaded images ---

f="""
Validation logic:
1. Check if user uploaded any images AND if count exceeds 10
2. Show warning message if limit exceeded
3. Truncate the list to only first 10 images
This prevents API overload and maintains performance
"""

if uploaded_images and len(uploaded_images) > 10:
    st.sidebar.warning("⚠️ You can upload a maximum of 10 images only!")
    uploaded_images = uploaded_images[:10]

# 6. --- Choose story type ---

f="""
Dropdown menu for selecting story genre:
1. Provides 10 different story types
2. Returns selected value as string
3. Default selection is "Comedy" (first in list)
"""

story_type = st.sidebar.selectbox(
    "Select Story Type:",
    [
        "Comedy",
        "Thriller",
        "Moral",
        "Horror",
        "Emotional",
        "Adventurous",
        "Action",
        "Mysterious",
        "Fantasy",
        "Fairy Tale"
    ]
)

# 7. --- Generate button ---

f="""
Two buttons for triggering different actions:
1. generate_button: Returns True when clicked, False otherwise
2. generate_audio_button: Returns True when clicked, False otherwise
These buttons trigger their respective code blocks below
"""

generate_button = st.sidebar.button("✨ Generate Story")
generate_audio_button = st.sidebar.button("🔊 Generate Audio from Story")

# 8. --- Main Content Area ---

f="""
Main page content displayed in the center of the screen:
1. Title using large heading (st.title)
2. Description text explaining the app functionality
"""

st.title("📖 AI Story Generator from Images")
st.write("Upload your images, choose a story type, and let AI craft a unique story and audio for you! 🚀")

# 9. --- Display uploaded images ---

f="""
If user has uploaded images, display them in a grid:
1. Check if uploaded_images exists and is not empty
2. Create a subheader
3. Create 5 columns for grid layout
4. Loop through each image and display in columns (wraps to next row after 5)
5. use_container_width=True makes images responsive to column width
"""

if uploaded_images:
    st.subheader("🖼️ Uploaded Images:")
    cols = st.columns(5)
    for idx, img in enumerate(uploaded_images):
        with cols[idx % 5]:
            st.image(img, use_container_width=True)

# 10. --- Story Generation Logic ---

f="""
This block executes ONLY when "Generate Story" button is clicked:
1. Validate that images are uploaded
2. Show loading spinner during generation
3. Convert uploaded files to PIL Image objects
4. Call AI generation function
5. Store result in session state for persistence
6. Handle any errors that occur
"""

if generate_button:

    f="""
    If no images uploaded, show warning and stop execution
    """
    if not uploaded_images:
        st.warning("Please upload at least one image before generating the story.")

    else:
        f="""
        Wraps the generation logic to catch and display any errors gracefully
        """

        try:
            f="""
            Shows animated spinner with custom message while code inside executes
            f-string formats story_type and image count into message
            """

            with st.spinner(f"Generating a **{story_type}** story based on {len(uploaded_images)} image(s) wait few minutes... ⏳"):

                f="""
                List comprehension that:
                1. Loops through each uploaded_image file
                2. Opens it using PIL.Image.open()
                3. Creates a list of PIL Image objects
                These objects are required by the AI model
                """
                pil_images = [Image.open(uploaded_image) for uploaded_image in uploaded_images]

                f="""
                Calls custom function from Story_Generation.py:
                - Input: list of PIL images + story type string
                - Output: generated story text as string
                - This makes API call to Google Gemini AI
                """
                generated_story = generate_story_from_images(pil_images, story_type)

                f="""
                Check if story was successfully generated:
                - If empty/None: show error
                - If valid: save to session state
                """
                if not generated_story:
                    st.error("⚠️ No story generated. Please try again.")
                else:
                    # SAVE TO SESSION so audio can access it later

                    f="""
                    st.session_state is a dictionary that persists data across reruns:
                    - Key: "generated_story"
                    - Value: the generated story text
                    - This allows audio generation button to access the story later
                    - Data persists even after page interactions/reruns
                    """
                    st.session_state["generated_story"] = generated_story

            f="""
            If any error occurs in the try block:
            1. Catch the exception as variable 'e'
            2. Display error message with details
            3. str(e) converts exception to readable string
            """
        except Exception as e:
            st.error(f"❌ An error occurred during story generation:\n\n**{str(e)}**")

# 11. --- Always show story if exists ---

f="""
This section displays the story WHENEVER it exists in session state:
1. Checks if "generated_story" key exists in session state
2. If yes, displays it in a styled card using custom HTML/CSS
3. Persists across page interactions (unlike variables which reset)
"""

if "generated_story" in st.session_state:

    f="""
    st.markdown with unsafe_allow_html=True allows custom HTML/CSS:
    
    f-string formatting:
    - {'story_type'}: Inserts selected story type into heading
    - {st.session_state["generated_story"].replace('\\n', '<br>')}: 
      * Gets story from session state
      * Replaces line breaks with HTML <br> tags
      * Preserves formatting in HTML
    
    CSS styling:
    - background-color: Dark theme background
    - padding: Space inside the card
    - border-radius: Rounded corners
    - box-shadow: Drop shadow for depth
    - border-left: Colored accent bar on left
    - line-height: Space between text lines
    - font-size: Text size
    - font-family: Professional fonts
    """

    st.markdown(
        f"""
        <div style="
            background-color:#1e1e2f;
            color:#f5f5f5;
            padding:2rem;
            border-radius:15px;
            box-shadow:0 4px 20px rgba(0, 0, 0, 0.3);
            line-height:1.7;
            font-size:1.05rem;
            font-family:'Segoe UI', 'Helvetica Neue', sans-serif;
            border-left:6px solid #8b5cf6;">
            <h3 style="color:#8b5cf6; margin-top:0;">📜 {story_type} Story</h3>
            <p>{st.session_state["generated_story"].replace('\n', '<br>')}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# 12. --- Audio Generation Logic ---

f="""
This block executes ONLY when "Generate Audio" button is clicked:
1. Validates that a story exists
2. Calls audio generation function
3. Saves audio to temporary file
4. Displays audio player
5. Cleans up temporary file
6. Handles errors
"""

if generate_audio_button:

    f="""
    Audio can only be generated from existing story text:
    - If no story in session state: show warning
    - If story exists: proceed with audio generation
    """

    if "generated_story" not in st.session_state:
        st.warning("⚠️ Please generate a story first before creating audio.")
    else:
        f="""
        Wraps audio generation logic to catch and display errors
        """

        try:
            f="""
            Shows spinner while audio is being generated
            Audio generation can take 10-30 seconds
            """

            with st.spinner("🎤 Generating audio narration... please wait few minutes."):
                
                f="""
                Calls function from Story_Generation.py:
                - Input: story text from session state
                - Output: file path to temporary WAV file
                - Makes API call to Google Gemini TTS
                - Converts PCM audio to WAV format
                """
                audio_path = generate_audio_from_generated_story(st.session_state["generated_story"])

                f="""
                Check if audio file was created successfully:
                1. audio_path exists (not None)
                2. File exists at that path (os.path.exists checks filesystem)
                """
                if audio_path and os.path.exists(audio_path):

                    # Check file size
                    f="""
                    os.path.getsize returns file size in bytes
                    Commented out display, but useful for debugging
                    Expected size: 2-5 MB for typical story
                    """
                    file_size = os.path.getsize(audio_path)
                    
                    # Read the file and create BytesIO
                    f="""
                    1. Open file in binary read mode ('rb')
                    2. Read entire file content as bytes
                    3. Store in audio_bytes variable
                    4. 'with' statement automatically closes file after reading
                    """
                    with open(audio_path, 'rb') as f:
                        audio_bytes = f.read()
                    
                    # Determine format from file extension
                    f="""
                    Check file extension to set correct MIME type:
                    - .mp3 → "audio/mp3"
                    - .wav → "audio/wav"
                    - default → "audio/wav" (our function returns .wav)
                    """
                    if audio_path.endswith('.mp3'):
                        audio_format = "audio/mp3"
                    elif audio_path.endswith('.wav'):
                        audio_format = "audio/wav"
                    else:
                        audio_format = "audio/wav"  # default
                    
                    f="""
                    st.audio creates embedded audio player:
                    - Input: audio file bytes
                    - format: tells browser how to decode the audio
                    - Browser renders play/pause controls
                    """
                    st.audio(audio_bytes, format=audio_format)
                    st.success("✅ Audio narration generated successfully!")
                    
                    # Clean up temp file
                    f="""
                    Delete temporary audio file from disk:
                    1. try-except prevents errors if file already deleted
                    2. os.unlink() deletes the file
                    3. Frees up disk space
                    4. pass means "do nothing" if deletion fails
                    """
                    try:
                        os.unlink(audio_path)
                    except:
                        pass
                else:
                    f="""
                    If function returned None or file doesn't exist:
                    - Show error message
                    - Prompt user to check console for details
                    """
                    st.error("⚠️ Failed to generate audio. Check the console for details.")

            f="""
            If any error occurs in the try block:
            1. Display error message with exception details
            2. Show full traceback for debugging
            3. st.code displays formatted code/error text
            """
        except Exception as e:
            st.error(f"❌ An unexpected error occurred while generating audio:\n\n**{str(e)}**")
            st.code(traceback.format_exc())
