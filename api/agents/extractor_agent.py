from api.utils.term_utils import extract_terms, verify_terms
from api.utils.cache_utils import cache_data

def process_medical_note(file_content):
    """
    Extract terms from the medical note and verify them using UMLS.
    Cache the results for later use.
    """
    extracted_terms = extract_terms(file_content)
    verified_definitions = verify_terms(extracted_terms)

    # Cache the results
    cache_data("verified_definitions", verified_definitions)
    cache_data("medical_note_content", file_content)

    return extracted_terms, verified_definitions