f="""
=============================================================================
AI STORY GENERATION MODULE
=============================================================================
This module provides two main functions:
1. Generate creative stories from images using Google Gemini AI
2. Convert generated stories into natural-sounding speech audio

Dependencies: google-generativeai, python-dotenv, Pillow
=============================================================================
"""

# 1. --- Importing libraries ---

f="""
Each import serves a specific purpose:
1. dotenv.load_dotenv - Loads environment variables from .env file
2. google.genai - Main Google Generative AI SDK for accessing Gemini models
3. google.genai.types - Type definitions for configuring API requests
4. io.BytesIO - Creates file-like objects in memory (for audio processing)
5. tempfile - Creates temporary files that auto-delete after use
6. wave - Python's built-in library for reading/writing WAV audio files
7. os - Operating system interface (for accessing environment variables)
"""

from dotenv import load_dotenv
import google.genai as genai
from google.genai import types
from io import BytesIO
import tempfile
import wave
import os

# 2. --- Load API keys from .env file ---

f="""
What this does:
1. Looks for a file named ".env" in the current directory
2. Reads all variables in format: VARIABLE_NAME=value
3. Makes them available via os.getenv() function
4. Keeps sensitive data (API keys) out of source code

Example .env file content:
GOOGLE_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Security benefit:
- .env file is added to .gitignore (not uploaded to GitHub)
- API keys remain private and secure
"""

load_dotenv()

# 3. --- Fetch Google API key securely ---

f="""
Process:
1. os.getenv("GOOGLE_API_KEY") searches for this environment variable
2. Returns the value as a string if found
3. Returns None if variable doesn't exist
4. Stored in variable 'api_key' for later use

Why use environment variables?
- Never hardcode API keys in source code
- Different keys for development/production
- Easy to change without modifying code
"""

api_key = os.getenv("GOOGLE_API_KEY")

# 4. --- Validate API key exists, raise error if missing to prevent API call failures ---

f="""
Validation logic:
1. "if not api_key" checks if api_key is None or empty string
2. Both None and "" are "falsy" values in Python
3. If falsy, raise ValueError exception
4. ValueError stops program execution immediately
5. Prevents API calls without proper authentication

This is a "fail-fast" approach:
- Better to crash early with clear error message
- Than to fail later with cryptic API authentication errors
"""

if not api_key:
    raise ValueError("!!!API KEY NOT FOUND!!!")

# 5. --- Initialize the Gemini client using the provided API key ---

f="""
What this creates:
1. genai.Client() creates an authenticated connection to Google's API
2. api_key parameter provides authentication credentials
3. Client object is stored in 'client' variable
4. This client will be used for all API calls (story & audio generation)

The client object provides access to:
- Text generation models (Gemini Pro)
- Vision models (for image analysis)
- Text-to-Speech models (for audio)
- Chat models (for conversations)
"""

client = genai.Client(api_key=api_key)

# 6. --- Initialize the Gemini Model for Text and Speech generation ---

f="""
Two different models for two different purposes:

MODEL 1: gemini-2.5-pro
- Purpose: Generate creative story text from images
- Capabilities:
  * Analyzes multiple images simultaneously
  * Understands context and relationships between images
  * Writes coherent, creative narratives
  * Supports multimodal input (text + images)
- "Pro" means: Higher quality, more capable (but slower & costlier)

MODEL 2: gemini-2.5-flash-preview-tts
- Purpose: Convert text to natural-sounding speech
- Capabilities:
  * Text-to-Speech (TTS) synthesis
  * Multiple voice options
  * Natural prosody and intonation
  * Returns raw audio data
- "Flash" means: Faster response, optimized for speed
- "preview" means: Still in testing, may change
- "tts" means: Text-To-Speech specialized model
"""

model_name_1 = 'gemini-2.5-pro'
model_name_2 = 'gemini-2.5-flash-preview-tts'

# 7. --- Function to define prompt ---

f="""
Function: story_prompt(story_type)

Purpose:
    Generates comprehensive instructions for the AI to create a story

Parameter:
    story_type (str) - Genre of story (e.g., "Comedy", "Horror", "Adventure")

Returns:
    str - Multi-line prompt with all instructions for the AI

Why we need this function:
    - AI models need clear, detailed instructions
    - Better prompts = better story quality
    - Reusable across different story types
    - Maintains consistent story structure
"""

def story_prompt(story_type):
    prompt = f"""
        You are a professional and skilled storyteller. Your job is to write a **{story_type} story** using the uploaded images as your inspiration.
        Use simple and easy to understand english
        **Instructions:**
        1. Look carefully at all the uploaded images. Imagine what could be happening in each one.  
        2. Write a story that connects all the images **in order**. Each image should feel like one scene in the story.  
        3. The story must have **at least 7 clear paragraphs**:
        - **Paragraph 1:** Begin the story — set the place, time, and main character(s).  
        - **Paragraphs 2-5:** Build the story using ideas from each image. Keep the flow natural and smooth.  
        - **Paragraph 6:** Add an important or surprising moment (the climax).  
        - **Paragraph 7:** End with a meaningful or emotional ending.  
        4. Match the **tone and feeling** to the selected story type:  
        - Horror → spooky and mysterious  
        - Comedy → light and funny  
        - Adventure → exciting and bold  
        - Emotional → touching and heartfelt  
        - Thriller → full of suspense  
        - Moral → gives a life lesson  
        - Fantasy → magical and creative  
        - Fairy Tale → simple and dreamlike  
        - Action → fast and powerful  
        - Mystery → curious and clever  
        5. Don't describe the images directly. Instead, **turn what you see into a smooth story** that feels natural and human.  
        6. Write in **simple, clear, and beautiful English** that anyone can enjoy reading.  
        7. The story should be **500-700 words** long and **feel complete**.

        Now write the full story using these images as inspiration.
        """
    
    return prompt

# 8. --- Function to generate story ---

f="""
Function: generate_story_from_images(images, story_type)

Purpose:
    Sends images to Gemini AI and receives a generated story

Parameters:
    images (list) - List of PIL Image objects to analyze
    story_type (str) - Genre of story to generate

Returns:
    str - Complete generated story text

Process Flow:
    1. Receive images and story type from user
    2. Create detailed prompt using story_prompt() function
    3. Send both images and prompt to Gemini API
    4. Wait for AI to analyze images and write story
    5. Extract and return the generated text
"""

def generate_story_from_images(images, story_type):
    response = client.models.generate_content(
        model=model_name_1,
        contents=[images, story_prompt(story_type)]
    )

    return response.text

# 9. --- function to generate audio ---

f="""
Function: generate_audio_from_generated_story(story_text)

Purpose:
    Converts story text into natural-sounding speech audio file

Parameter:
    story_text (str) - The story text to convert to speech

Returns:
    str - File path to temporary WAV audio file
    None - If generation fails

Process Overview:
    1. Validate and truncate text if too long
    2. Send text to Gemini TTS model
    3. Receive raw PCM audio data
    4. Convert PCM to WAV format (add headers)
    5. Save to temporary file
    6. Return file path for playback

Technical Challenge Solved:
    Gemini returns raw PCM audio (just the samples)
    But browsers need WAV format (samples + headers)
    This function bridges that gap
"""

def generate_audio_from_generated_story(story_text: str):
    f="""
    Generate speech from the story using Gemini and return audio file.
    Converts raw PCM to WAV format for playback.
    """
    try:        
        response = client.models.generate_content(
            model=model_name_2,
            contents=[story_text],
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name="Kore"
                        )
                    )
                )
            )
        )

        # Extract audio data
        audio_part = response.candidates[0].content.parts[0]
        
        if hasattr(audio_part, 'inline_data'):
            # audio_data is already bytes (not base64 string)
            audio_data = audio_part.inline_data.data
            
            # Gemini returns raw PCM data (audio/L16;codec=pcm;rate=24000)
            # We need to wrap it in WAV format
            
            # Create a WAV file with proper headers
            audio_buffer = BytesIO()
            
            with wave.open(audio_buffer, 'wb') as wav_file:
                wav_file.setnchannels(1)        # Mono
                wav_file.setsampwidth(2)        # 16-bit (L16 = Linear 16-bit PCM)
                wav_file.setframerate(24000)    # Sample rate from mime_type
                wav_file.writeframes(audio_data)  # Write raw PCM data
            
            # Reset buffer to beginning
            audio_buffer.seek(0)
                    
            # Save to temp file for Streamlit
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_file.write(audio_buffer.getvalue())
            temp_file.flush()
            temp_file.close()
            
            return temp_file.name
        else:
            print("❌ No inline_data found in response")
            return None

    except Exception as e:
        print(f"❌ Error generating audio: {e}")
        import traceback
        traceback.print_exc()
        return None

