# ============================================
# PROJECT 3 - AI RESEARCH ASSISTANT
# PART 39 - RESEARCH PROGRESS & AGENT ACTIVITY
# ============================================

# -----------------------------
# IMPORT LIBRARIES
# -----------------------------

import os
import json
from urllib.parse import urlparse

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from tavily import TavilyClient

from langchain_ollama import ChatOllama


# ============================================
# LOAD ENVIRONMENT VARIABLES
# ============================================

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")


# ============================================
# CHECK ENVIRONMENT VARIABLES
# ============================================

if not TAVILY_API_KEY:
    raise ValueError(
        "TAVILY_API_KEY is missing from .env"
    )

if not OLLAMA_MODEL:
    raise ValueError(
        "OLLAMA_MODEL is missing from .env"
    )


# ============================================
# INITIALIZE CLIENTS
# ============================================

tavily_client = TavilyClient(
    api_key=TAVILY_API_KEY
)

llm = ChatOllama(
    model=OLLAMA_MODEL,
    temperature=0.2
)


# ============================================
# CREATE FASTAPI APP
# ============================================

app = FastAPI(
    title="AI Research Assistant API",
    description="Agentic AI Research Assistant with Web Search",
    version="1.0.0"
)


# ============================================
# CORS
# ============================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ============================================
# REQUEST MODEL
# ============================================

class ResearchRequest(BaseModel):

    query: str

    mode: str = "quick"


# ============================================
# ROOT
# ============================================

@app.get("/")
def root():

    return {
        "message": "AI Research Assistant API is running"
    }


# ============================================
# HEALTH
# ============================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ============================================
# GET DOMAIN
# ============================================

def get_domain(url):

    try:

        domain = urlparse(url).netloc

        domain = domain.replace(
            "www.",
            ""
        )

        return domain

    except Exception:

        return "unknown"


# ============================================
# SOURCE QUALITY SCORE
# ============================================

def calculate_source_score(source):

    score = 0

    relevance = source.get(
        "score",
        0
    )

    score += relevance * 60


    content = source.get(
        "content",
        ""
    )

    if content:

        if len(content) > 300:
            score += 15

        if len(content) > 800:
            score += 10


    url = source.get(
        "url",
        ""
    )

    domain = get_domain(url)


    if domain.endswith(".edu"):

        score += 15

    elif domain.endswith(".gov"):

        score += 15

    elif domain.endswith(".org"):

        score += 8


    return round(
        score,
        2
    )


# ============================================
# REMOVE DUPLICATE SOURCES
# ============================================

def remove_duplicate_sources(sources):

    unique_sources = []

    seen_urls = set()

    seen_domains = set()


    for source in sources:

        url = source.get(
            "url",
            ""
        ).strip()

        domain = get_domain(url)


        if not url:
            continue


        if url in seen_urls:
            continue


        if domain in seen_domains:
            continue


        seen_urls.add(url)

        seen_domains.add(domain)

        unique_sources.append(
            source
        )


    return unique_sources


# ============================================
# PROCESS SOURCES
# ============================================

def process_sources(sources):

    unique_sources = remove_duplicate_sources(
        sources
    )


    for source in unique_sources:

        source["quality_score"] = (
            calculate_source_score(source)
        )


    unique_sources.sort(
        key=lambda item: item.get(
            "quality_score",
            0
        ),
        reverse=True
    )


    return unique_sources[:5]


# ============================================
# SEARCH WEB
# ============================================

def search_web(query):

    response = tavily_client.search(

        query=query,

        search_depth="advanced",

        max_results=8
    )


    results = response.get(
        "results",
        []
    )


    return process_sources(
        results
    )


# ============================================
# QUERY DECOMPOSITION
# ============================================

def decompose_query(query):

    prompt = f"""
You are a research planning AI.

The user wants to research:

{query}


Break this question into 2 to 4 smaller
research questions.

Each question must investigate a different
important aspect of the original question.

Rules:

1. Return ONLY a JSON array.
2. Do not include explanations.
3. Do not use Markdown.
4. Each item must be a complete question.
5. Do not create duplicate questions.


Example:

[
    "What are the benefits of AI agents?",
    "What are the risks of AI agents?",
    "What is the future of AI agents?"
]
"""


    response = llm.invoke(
        prompt
    )


    content = response.content.strip()


    # Remove Markdown code fences
    if content.startswith("```"):

        content = content.replace(
            "```json",
            ""
        )

        content = content.replace(
            "```",
            ""
        )

        content = content.strip()


    try:

        sub_questions = json.loads(
            content
        )

    except json.JSONDecodeError:

        sub_questions = [query]


    if not isinstance(
        sub_questions,
        list
    ):

        sub_questions = [query]


    cleaned_questions = []


    for question in sub_questions:

        if isinstance(
            question,
            str
        ):

            question = question.strip()

            if question:

                cleaned_questions.append(
                    question
                )


    if not cleaned_questions:

        cleaned_questions = [query]


    return cleaned_questions[:4]


# ============================================
# BUILD RESEARCH CONTEXT
# ============================================

def build_research_context(
    research_results
):

    context_parts = []


    for research_item in research_results:

        sub_question = research_item[
            "sub_question"
        ]

        sources = research_item[
            "sources"
        ]


        context_parts.append(
            f"""
========================================
RESEARCH QUESTION
========================================

{sub_question}
"""
        )


        for index, source in enumerate(
            sources,
            start=1
        ):

            title = source.get(
                "title",
                "Untitled Source"
            )

            url = source.get(
                "url",
                ""
            )

            content = source.get(
                "content",
                ""
            )


            content = content[:2500]


            context_parts.append(
                f"""
SOURCE {index}

Title:
{title}

URL:
{url}

Content:
{content}
"""
            )


    return "\n".join(
        context_parts
    )


# ============================================
# RESEARCH MODE INSTRUCTIONS
# ============================================

def get_mode_instructions(mode):

    if mode == "quick":

        return """
Provide a concise research answer.

Focus on:
- Important facts
- Key findings
- Direct explanation

Avoid unnecessary details.
"""


    elif mode == "deep":

        return """
Provide a detailed research report.

Use these sections:

1. Overview
2. Key Findings
3. Important Developments
4. Evidence from Sources
5. Limitations or Uncertainty
6. Conclusion
"""


    elif mode == "compare":

        return """
Compare information from different
research questions and sources.

Focus on:

1. Similarities
2. Differences
3. Conflicting information
4. Important evidence
5. Overall conclusion
"""


    return """
Provide a clear and accurate answer.
"""


# ============================================
# GENERATE FINAL ANSWER
# ============================================

def generate_research_answer(
    query,
    research_context,
    mode
):

    mode_instructions = get_mode_instructions(
        mode
    )


    prompt = f"""
You are an AI Research Assistant.

The original user question is:

{query}


The system performed multi-step research.

Research findings:

{research_context}


Research mode:

{mode}


Instructions:

{mode_instructions}


IMPORTANT RULES:

1. Use the research findings as primary
   evidence.

2. Do not invent facts.

3. Combine findings from different
   research questions.

4. Mention uncertainty when appropriate.

5. Use Markdown formatting.

6. Answer the original question.


Now produce the final research answer.
"""


    response = llm.invoke(
        prompt
    )


    return response.content

# ============================================
# GENERATE MARKDOWN REPORT
# ============================================

def generate_markdown_report(
    query,
    mode,
    sub_questions,
    answer,
    sources
):
    """
    Create a professional Markdown research report.
    """

    report = []

    # ----------------------------------------
    # Report title
    # ----------------------------------------

    report.append(
        "# AI Research Assistant Report"
    )

    report.append("")

    report.append(
        f"**Research Question:** {query}"
    )

    report.append("")

    report.append(
        f"**Research Mode:** {mode.title()}"
    )

    report.append("")

    report.append(
        f"**Total Research Questions:** "
        f"{len(sub_questions)}"
    )

    report.append("")

    report.append(
        f"**Total Sources:** {len(sources)}"
    )

    report.append("")

    report.append("---")

    report.append("")


    # ----------------------------------------
    # Research plan
    # ----------------------------------------

    report.append(
        "## Research Plan"
    )

    report.append("")

    for index, question in enumerate(
        sub_questions,
        start=1
    ):

        report.append(
            f"{index}. {question}"
        )

    report.append("")

    report.append("---")

    report.append("")


    # ----------------------------------------
    # AI Answer
    # ----------------------------------------

    report.append(
        "## Research Answer"
    )

    report.append("")

    report.append(answer)

    report.append("")

    report.append("---")

    report.append("")


    # ----------------------------------------
    # Sources
    # ----------------------------------------

    report.append(
        "## Sources"
    )

    report.append("")


    for index, source in enumerate(
        sources,
        start=1
    ):

        title = source.get(
            "title",
            "Untitled Source"
        )

        url = source.get(
            "url",
            ""
        )

        domain = source.get(
            "domain",
            ""
        )

        quality_score = source.get(
            "quality_score",
            0
        )

        sub_question = source.get(
            "sub_question",
            ""
        )


        report.append(
            f"### {index}. {title}"
        )

        report.append("")

        report.append(
            f"**Domain:** {domain}"
        )

        report.append("")

        report.append(
            f"**Quality Score:** {quality_score}"
        )

        report.append("")

        report.append(
            f"**Related Research Question:** "
            f"{sub_question}"
        )

        report.append("")

        report.append(
            f"**Source:** {url}"
        )

        report.append("")


    # ----------------------------------------
    # Footer
    # ----------------------------------------

    report.append("---")

    report.append("")

    report.append(
        "*Generated by AI Research Assistant*"
    )


    # Convert list into one Markdown string
    return "\n".join(report)

# ============================================
# RESEARCH ENDPOINT
# ============================================

@app.post("/research")
def research(
    request: ResearchRequest
):

    # ========================================
    # ACTIVITY 1
    # PLAN RESEARCH
    # ========================================

    sub_questions = decompose_query(
        request.query
    )


    # ========================================
    # STORE RESEARCH RESULTS
    # ========================================

    research_results = []


    # ========================================
    # SEARCH EACH SUB-QUESTION
    # ========================================

    for sub_question in sub_questions:

        sources = search_web(
            sub_question
        )


        research_results.append({

            "sub_question": sub_question,

            "sources": sources
        })


    # ========================================
    # BUILD CONTEXT
    # ========================================

    research_context = build_research_context(
        research_results
    )


    # ========================================
    # GENERATE ANSWER
    # ========================================

    answer = generate_research_answer(

        request.query,

        research_context,

        request.mode
    )


    # ========================================
    # FORMAT SOURCES
    # ========================================

    formatted_sources = []


    for research_item in research_results:

        sub_question = research_item[
            "sub_question"
        ]


        for source in research_item[
            "sources"
        ]:

            formatted_sources.append({

                "sub_question": sub_question,

                "title": source.get(
                    "title",
                    "Untitled Source"
                ),

                "url": source.get(
                    "url",
                    ""
                ),

                "content": source.get(
                    "content",
                    ""
                ),

                "score": source.get(
                    "score",
                    0
                ),

                "quality_score": source.get(
                    "quality_score",
                    0
                ),

                "domain": get_domain(
                    source.get(
                        "url",
                        ""
                    )
                )
            })


    # ========================================
    # AGENT ACTIVITY
    # ========================================

    activity = []


    # Planning activity
    activity.append({

        "step": 1,

        "type": "planning",

        "title": "Research Planning",

        "description": (
            "The AI decomposed the original "
            "question into smaller research questions."
        ),

        "status": "completed"
    })


    # Search activity
    for index, sub_question in enumerate(
        sub_questions,
        start=1
    ):

        activity.append({

            "step": index + 1,

            "type": "search",

            "title": (
                f"Researching Sub-question {index}"
            ),

            "description": sub_question,

            "status": "completed"
        })


    # Source processing
    activity.append({

        "step": len(activity) + 1,

        "type": "sources",

        "title": "Processing Sources",

        "description": (
            "Duplicate sources were removed "
            "and source quality was evaluated."
        ),

        "status": "completed"
    })


    # Final synthesis
    activity.append({

        "step": len(activity) + 1,

        "type": "synthesis",

        "title": "Generating Final Answer",

        "description": (
            "The AI combined the research findings "
            "into the final answer."
        ),

        "status": "completed"
    })

    # ========================================
# GENERATE REPORT
# ========================================

    report = generate_markdown_report(

        request.query,

        request.mode,

        sub_questions,

        answer,

        formatted_sources
)
    # ========================================
    # FINAL RESPONSE
    # ========================================

    return {

        "query": request.query,

        "mode": request.mode,

        "sub_questions": sub_questions,

        "answer": answer,

        "total_sub_questions": len(
            sub_questions
        ),

        "total_sources": len(
            formatted_sources
        ),

        "sources": formatted_sources,

        "activity": activity,
        
        "report": report
    }