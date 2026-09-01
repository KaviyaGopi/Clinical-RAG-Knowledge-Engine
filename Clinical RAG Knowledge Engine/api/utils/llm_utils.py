from api.exceptions import ApplicationError
from api.utils.langchain_llm import ask_llm

def query_llm(question, context_dict):
    """Query the LLM with a question and context."""
    try:
        return ask_llm(question, context_dict)
    except Exception as e:
        raise ApplicationError(f"Failed to process the question: {e}", status_code=500)