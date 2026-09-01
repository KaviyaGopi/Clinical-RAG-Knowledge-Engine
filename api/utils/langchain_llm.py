import ast
import os
import re
import requests
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

UMLS_API_KEY = os.getenv("UMLS_API_KEY")
UMLS_AUTH_ENDPOINT = "https://utslogin.nlm.nih.gov"
UMLS_API_ENDPOINT = "https://uts-ws.nlm.nih.gov"

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0,
)

prompt_template = PromptTemplate.from_template("""
You are a medical assistant specialized in obstetrics and fetal monitoring.

Medical note:
{note}

First, carefully read through the above medical note.

Now, extract ONLY the specific medical terms that are explicitly mentioned in this note. 
If any terms appear to be misspelled, correct their spelling before including them in the list.
DO NOT include any terms that don't appear in the note.
DO NOT use the category names or examples below unless they are explicitly written in the note.

The terms might relate to these categories, but extract ONLY what's in the note:
- Fetal heart monitoring
- Maternal conditions
- Labor and delivery
- Medications
- Complications
- Other clinical terms

Your response should ONLY contain a Python list of terms found in the text, with corrected spellings if necessary:
""")

def extract_medical_terms(text):
    cleaned_text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    cleaned_text = cleaned_text.replace('```python', '').replace('```', '')

    print(f"Analyzing text (preview): {cleaned_text[:200]}...")

    if len(cleaned_text.strip()) < 20:
        print("WARNING: Text is too short or empty")
        return []

    chain = prompt_template | llm
    response = chain.invoke({"note": cleaned_text})

    print(f"Raw LLM response: {response.content[:200]}...")
    try:
        list_pattern = r'\[(.*?)\]'
        match = re.search(list_pattern, response.content, re.DOTALL)
        if match:
            list_content = match.group(1)
            try:
                full_list = f"[{list_content}]"
                terms = ast.literal_eval(full_list)
                return [term.strip() for term in terms if term.strip()]
            except:
                return [term.strip().strip('"\'') for term in list_content.split(',') if term.strip()]
        else:
            lines = response.content.split('\n')
            terms = []
            for line in lines:
                if not line.strip() or line.strip().startswith('#') or ':' in line.strip():
                    continue
                if ',' not in line:
                    terms.append(line.strip())
                else:
                    terms.extend([t.strip() for t in line.split(',') if t.strip()])
            return [term.strip().strip('"\'') for term in terms if term.strip()]
    except Exception as e:
        print(f"Error parsing LLM response: {e}")
        return [term.strip() for term in response.content.split(",") if term.strip()]

def get_umls_tgt():
    try:
        auth_res = requests.post(
            f"{UMLS_AUTH_ENDPOINT}/cas/v1/api-key",
            data={"apikey": UMLS_API_KEY},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        if auth_res.status_code == 201:
            print("Successfully retrieved TGT.")
            return auth_res.headers["location"]
        else:
            print(f"Failed to retrieve TGT. Response: {auth_res.text}")
            return None
    except Exception as e:
        print(f"Error retrieving TGT: {e}")
        return None

def get_umls_service_ticket(tgt):
    try:
        res = requests.post(tgt, data={"service": "http://umlsks.nlm.nih.gov"})
        if res.status_code == 200:
            print("Successfully retrieved Service Ticket.")
            return res.text
        else:
            print(f"Failed to retrieve Service Ticket. Response: {res.text}")
            return None
    except Exception as e:
        print(f"Error retrieving Service Ticket: {e}")
        return None
    
def get_umls_service_ticket_with_retry(tgt, retries=3, delay=2):
    for attempt in range(retries):
        try:
            res = requests.post(tgt, data={"service": "http://umlsks.nlm.nih.gov"}, timeout=2)
            if res.status_code == 200:
                return res.text
            else:
                print(f"Attempt {attempt + 1}: Failed to retrieve Service Ticket. Response: {res.text}")
        except Exception as e:
            print(f"Attempt {attempt + 1}: Error retrieving Service Ticket: {e}")
        time.sleep(delay)
    return None

def verify_terms_with_umls(terms):
    tgt = get_umls_tgt()
    if not tgt:
        print("Failed to retrieve TGT. Cannot proceed with UMLS verification.")
        return {}

    verified = {}

    for term in terms:
        ticket = get_umls_service_ticket(tgt)
        if not ticket:
            print(f"Failed to retrieve Service Ticket for term '{term}'. Skipping.")
            continue

        try:
            res = requests.get(
                f"{UMLS_API_ENDPOINT}/rest/search/current",
                params={"string": term, "ticket": ticket},
                headers={"Accept": "application/json"}
            )
            results = res.json().get("result", {}).get("results", [])
            if results:
                concept_ui = results[0].get("ui")
                standardized_name = results[0].get("name")
                if concept_ui:
                    ticket = get_umls_service_ticket(tgt)
                    if not ticket:
                        print(f"Failed to retrieve Service Ticket for term '{term}' (definitions). Skipping.")
                        continue
                    definitions_res = requests.get(
                        f"{UMLS_API_ENDPOINT}/rest/content/current/CUI/{concept_ui}/definitions",
                        params={"ticket": ticket},
                        headers={"Accept": "application/json"}
                    )
                    if definitions_res.status_code == 401:
                        print(f"Unauthorized error for term '{term}'. Invalid Service Ticket.")
                        continue

                    definitions_data = definitions_res.json().get("result", [])
                    if definitions_data:
                        english_definitions = [
                            definition.get("value")
                            for definition in definitions_data
                            if definition.get("rootSource") in {"MSH", "NCI", "CSP"}
                        ]
                        if english_definitions:
                            verified[term] = english_definitions[0]
                        else:
                            print(f"Term '{term}' has no English definition in UMLS; using standardized name.")
                            verified[term] = standardized_name or "Definition not available"
                    else:
                        print(f"Term '{term}' has no definition in UMLS; using standardized name.")
                        verified[term] = standardized_name or "Definition not available"
                else:
                    print(f"Term '{term}' has no unique identifier in UMLS.")
            else:
                print(f"No results found for term '{term}' in UMLS.")
        except Exception as e:
            print(f"Error querying UMLS for term '{term}': {e}")

    verified_with_definitions = {k: v for k, v in verified.items() if v != "Definition not available"}
    return verified_with_definitions

def get_all_umls_terms(tgt):
    return []

def ask_llm(question, context_dict):
    medical_note_content = context_dict.get("Medical Note Content", "")
    verified_definitions = {k: v for k, v in context_dict.items() if k != "Medical Note Content"}
    definitions_text = "\n".join([f"{term}: {definition}" for term, definition in verified_definitions.items()])
    qa_template = PromptTemplate.from_template("""
You are a medical assistant specialized in obstetrics and fetal heart rate analysis. Use the following information to answer the user's question:

1. Medical Note Content: This provides detailed context about the patient's condition, history, and procedures.
2. Verified Medical Terms: These terms and their meanings have been verified using UMLS and may contain definitions or explanations.

When answering the question:
- If the question is related to the verified terms, prioritize using them to provide a detailed and accurate answer.
- If the question is not covered by the verified terms, use the medical note content to provide a comprehensive response.
- Always aim to provide a clear and concise answer based on the available information.
- If the answer is found from the medical note content, please highlight the relevant part of the note in your response. To do this, use a format similar to this: This information can be found in this part of the medical note: [insert relevant part of the note here].

Important:
- If you use the verified terms in your answer, include the relevant term(s) explicitly.
- Do not indicate whether you used your own knowledge or the verified terms in your response.
- Your answer should be in plain text without any markdown or formatting.
- Do not include any personal pronouns or references to yourself in the answer.

Medical Note Content:
{medical_note_content}

Verified Terms:
{definitions_text}

Question:
{question}
    """)

    # Pass the variables to the prompt template
    chain = qa_template | llm
    result = chain.invoke({
        "medical_note_content": medical_note_content,
        "definitions_text": definitions_text,
        "question": question
    })
    return result.content
