from langchain.prompts import PromptTemplate
from api.utils.langchain_llm import llm

def refine_response(question, feedback, initial_response, medical_note):
    refiner_prompt = PromptTemplate.from_template("""
    You are a medical expert specialized in obstetrics and fetal monitoring.
                                                  
    Question:
    {question}
                                                  
    Initial Response:
    {initial_response}

    Feedback:
    {feedback}

    Medical Note:
    {medical_note}

    Based on the question, feedback and the medical note, refine the initial response to make it accurate, detailed and relevant to the question.
    Important:
    - Your refined response should address all the issues mentioned in the feedback and ensure it directly answers the question.
    - Your refined response should strictly be in plain text without any markdown or formatting.
    - If the initial response is correct, you can simply rephrase it to make it clearer and more concise.
    - If the initial response is incorrect, provide a corrected version based on the feedback and the medical note.
    - Do not include any personal pronouns or references to yourself in the refined response.
    - Remember, your aim is not to just correct the initial response, but to provide a comprehensive and accurate answer to the question based on the medical note and the feedback provided.
    - Your refined response should be clear, concise, and directly related to the question asked.

    Your refined response:
    """)

    chain = refiner_prompt | llm
    result = chain.invoke({
        "question": question,
        "feedback": feedback,
        "initial_response": initial_response,
        "medical_note": medical_note
    })
    return result.content
