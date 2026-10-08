# ============================================
# Project 3: AI Research Assistant
# Stage 1 - Project Foundation
# ============================================

import os

import streamlit as st
from dotenv import load_dotenv


# ============================================
# 1. Load environment variables
# ============================================

load_dotenv()


# ============================================
# 2. Get the Tavily API key
# ============================================

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


# ============================================
# 3. Streamlit page configuration
# ============================================

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔎",
    layout="wide"
)


# ============================================
# 4. Application title
# ============================================

st.title("🔎 AI Research Assistant")

st.write(
    "An AI-powered research assistant that will search "
    "the web and help generate research-based answers."
)


# ============================================
# 5. API key status
# ============================================

if TAVILY_API_KEY:
    st.success("Tavily API key loaded successfully.")
else:
    st.error(
        "Tavily API key was not found. "
        "Please add TAVILY_API_KEY to your .env file."
    )


# ============================================
# 6. Research question
# ============================================

research_question = st.text_input(
    "Enter your research question:",
    placeholder="Example: What are the latest developments in AI agents?"
)


# ============================================
# 7. Initial button
# ============================================

if st.button("Start Research"):

    if not research_question.strip():
        st.warning("Please enter a research question.")

    elif not TAVILY_API_KEY:
        st.error("Tavily API key is missing.")

    else:
        st.info(
            "The research engine will be connected in the next major stage."
        )

        st.write("Research question:")
        st.write(research_question)