# FHR-Notes-LLM

This project is designed to analyze medical terms and retrieve their definitions using the UMLS API. Follow the steps below to set up and run the project.

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.11 or higher
- Git
- Poetry (Python dependency management tool)

---

## Setup Instructions

### 1. Clone the Repository

Use the following command to clone the repository:

```bash
git clone <repository-url>
```

### 2. Navigate to Project Directory

```bash
cd "FHR Project"
```

### 3. Install the dependencies using Poetry

```bash
poetry install
```

This will create a virtual environment and install all required packages specified in `pyproject.toml`.

---

### 4. Set up Environment Variables

```bash
GEMINI_API_KEY="YOUR-GEMINI-API-KEY-HERE"
UMLS_API_KEY="YOUR-UMLS-API-KEY-HERE"
```

---

### Running the Project

### 5. Activate the Poetry Shell

This command activates the virtual environment created by Poetry.

```bash
poetry shell
```

### 6. Apply Migrations

```bash
python manage.py migrate
```

### 7. Start the Server

```bash
python manage.py runserver
```

---

### How to test

1. Open Postman

2. Enter the URL as `http://127.0.0.1:8000/api/upload/`

3. Select method as `POST`.

4. Go to the `BODY` tab.

5. Insert a new key with the name `file`.

6. Select the type as `File`.

7. In the `VALUE` section upload one of the medical notes (`.txt` format)

8. Send the request.

The output should be similar to this:

```
{
    "extracted_terms": [
        "obstetrics",
        "c-section",
        "anesthesia",
        "spinal",
        "uterus",
        "lower segment transverse",
        "xiphoid",
        "electrosurgery",
        "laser",
        "oxygen",
        "nasal cannula",
        "lateral",
        "foley",
        "urethra",
        "pathology",
        "telfa",
        "tegaderm",
        "normal saline",
        "antibiotics",
        "prophylaxis"
    ],
    "verified": {
        "obstetrics": "A medical-surgical specialty concerned with management and care of women during pregnancy, parturition, and the puerperium.",
        "c-section": "Extraction of the FETUS by means of abdominal HYSTEROTOMY.",
        "anesthesia": "Treatment with a pharmacological substance that produces a loss of feeling.",
        "spinal": "Of or relating to the spine or spinal cord.",
        "uterus": "A hollow, thick-walled, muscular organ located within the pelvic cavity of a woman. Within the uterus the fertilized egg implants and the fetus develops during pregnancy.",
        "xiphoid": "The smallest and most inferior triangular protrusion of the STERNUM or breastbone that extends into the center of the RIBCAGE.",
        "electrosurgery": "Division of tissues by a high-frequency current applied locally with a metal instrument or needle. (Stedman, 25th ed)",
        "laser": "Laser plant",
        "oxygen": "An element with atomic symbol O, atomic number 8, and atomic weight 16.",
        "nasal cannula": "Nasal Cannula",
        "lateral": "Situated at or extending to the side.",
        "foley": "A flexible plastic tube inserted into the bladder to provide continuous urinary drainage. A balloon on the bladder end is inflated (with air or fluid) so that the catheter cannot pull out but is retained in the bladder as an \"indwelling\" catheter.",
        "urethra": "membranous canal conveying urine from the bladder to the exterior of the body.",
        "pathology": "The medical science, and specialty practice, concerned with all aspects of disease, but with special reference to the essential nature, causes, and development of abnormal conditions, as well as the structural and functional changes that result from the disease processes. Informally used to mean the result of such an examination.",
        "telfa": "Telfa Dressing 3x8\"",
        "tegaderm": "Tegaderm Dressing",
        "normal saline": "A crystalloid solution that contains 9.0g of SODIUM CHLORIDE per liter of water. It has a variety of uses, including: as a CONTACT LENS SOLUTION, in OPHTHALMIC SOLUTIONS and NASAL LAVAGE, in wound irrigation, and for FLUID THERAPY.",
        "antibiotics": "substances produced by microorganisms or biomimetics that can inhibit or suppress the growth of other microorganisms; frequently used without reference to the microbial origins of the original substance.",
        "prophylaxis": "taking advance measures against the occurrence of something possible or probable; prefer NTs."
    }
}
```
