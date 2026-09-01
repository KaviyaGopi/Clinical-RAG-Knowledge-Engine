from api.utils.cache_utils import get_cached_data
from api.utils.langchain_llm import llm
from api.utils.llm_utils import query_llm
from langchain.prompts import PromptTemplate

def answer_question(question):

    verified_definitions = get_cached_data("verified_definitions")
    medical_note_content = get_cached_data("medical_note_content")

    if not verified_definitions or not medical_note_content:
        raise ValueError("No medical note or verified definitions found. Please upload a medical note first.")

    if not isinstance(verified_definitions, dict):
        raise ValueError("Verified definitions are not in the correct format.")

    context_dict = {
        "Medical Note Content": medical_note_content,
        **verified_definitions
    }

    return query_llm(question, context_dict)

def review_initial_response(initial_response, medical_note, verified_definitions):
    reviewer_prompt = PromptTemplate.from_template("""
    You are a medical assistant specialized in obstetrics and fetal monitoring.

    Initial Response:
    {initial_response}

    Medical Note:
    {medical_note}

    Verified Definitions:
    {verified_definitions}

    You are a medical expert specialized in obstetrics and fetal heart rate analysis.
    Analyze the initial response based on the medical note and the verified definitions.
    Understand the context and the medical terms used in the initial response.
    Provide feedback on the accuracy and relevance of the initial response.
    Identify any inaccuracies or misinterpretations in the initial response and provide feedback.
    Your feedback should strictly be in plain text without any markdown or formatting.
    Do not include any personal pronouns or references to yourself in the feedback.

    Your feedback:
    """)

    definitions_text = "\n".join([f"{term}: {definition}" for term, definition in verified_definitions.items()])

    chain = reviewer_prompt | llm
    result = chain.invoke({
        "initial_response": initial_response,
        "medical_note": medical_note,
        "verified_definitions": definitions_text
    })
    return result.content
