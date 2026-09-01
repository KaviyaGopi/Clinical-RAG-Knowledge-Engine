from langchain.prompts import PromptTemplate
from api.utils.langchain_llm import llm

def generate_initial_response(question, medical_note):
    generator_prompt = PromptTemplate.from_template("""
    You are a medical assistant specialized in obstetrics and fetal monitoring.

    Medical Note:
    {medical_note}

    Question:
    {question}
    
    You are a medical assistant specialized in obstetrics and fetal heart rate analysis.
    Based on your knowledge and the medical note, provide a detailed and accurate response to the question.
    Important:
    - Your response should strictly be in plain text without any markdown or formatting.
    - Do not include any personal pronouns or references to yourself in the response.
    - Do not mention something like "The patient indicated that" or "The patient said that". Instead, use a format similar to this: This information can be found in this part of the medical note: [insert relevant part of the note here].
    - Your answer should be clear, concise, and directly related to the question asked.
    - You may include other relevant information from the medical note that may not be directly related to the question but is important for a comprehensive understanding of the patient's condition, but indicate this if you do so.

    Your response:
    """)

    chain = generator_prompt | llm
    result = chain.invoke({
        "medical_note": medical_note,
        "question": question
    })
    return result.content
