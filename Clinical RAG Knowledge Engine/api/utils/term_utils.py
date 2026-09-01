from api.exceptions import ApplicationError
from api.utils.langchain_llm import extract_medical_terms, verify_terms_with_umls

def extract_terms(file_content):
    """Extract medical terms from the file content."""
    try:
        return extract_medical_terms(file_content)
    except Exception as e:
        raise ApplicationError(f"Failed to extract terms: {e}", status_code=500)

def verify_terms(terms):
    """Verify extracted terms using UMLS."""
    try:
        return verify_terms_with_umls(terms)
    except Exception as e:
        raise ApplicationError(f"Failed to verify terms with UMLS: {e}", status_code=500)