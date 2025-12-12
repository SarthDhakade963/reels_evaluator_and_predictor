import json
import logging
import os
from google import genai
import streamlit as st
from PIL import Image
from google.genai import types

from rubric_prompt import rubric_prompt
from rubric_schema import FULL_RUBRIC_SCHEMA
from dotenv import load_dotenv

load_dotenv()
try:

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Failed to initialize Gemini Client: {e}")
    client = None

MODEL_NAME = 'gemini-2.5-flash'


def evaluate_video(frames):
    if client is None:
        return {"error": "Gemini client failed to initialize."}

    pil_images = [Image.fromarray(frame) for frame in frames]

    prompt_parts = [
        rubric_prompt,
        "Video frames for analysis:",
        *pil_images,
        "TASK:  1. Return JSON.",
    ]

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=FULL_RUBRIC_SCHEMA,
        temperature=0.0
    )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt_parts,
            config=config,
        )

        result = response.text
        return json.loads(result)

    except json.JSONDecodeError as e:
        error_msg = f"LLM returned invalid JSON: {e}"
        logging.error(f"{error_msg}. Raw response: {response.text[:200]}...")
        st.error(f"{error_msg}. Check your prompt and schema.")
        return {"error": error_msg}
    except Exception as e:
        st.error(f"Error during Gemini evaluation: {e}")
        return {"error": str(e)}
