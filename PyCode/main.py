import os
import nltk

from google import genai
from dotenv import load_dotenv
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


# ============================================================
# 1. NLTK SETUP
# ============================================================

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)

STOP_WORDS = set(stopwords.words("english"))


# ============================================================
# 2. LOAD GEMINI API KEY
# ============================================================

load_dotenv()

API_KEY=os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("API KEY not found in .env!")
else:
    # print("Key is loade successfully!")
    pass

# ============================================================
# 3. LOAD KNOWLEDGE BASE
# ============================================================

Knowledge_base_path = '../Complete_knowlade_base/data.txt'
def load_knowlade_base():
    try:
        with open(Knowledge_base_path, 'r', encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        return ""
    except Exception as e:
        print(f"Error loading knowledge base: {e}")
        return ""

# x=load_knowlade()
# print(x)

# ============================================================
# 4. NLP — EXTRACT KEYWORDS
# ============================================================

def extract_key_words(question):
    # Convert question into lowercase tokens
    tokens=word_tokenize(question.lower())
    # return tokens

# print(extract_key_words("What is YASH your return policy ?"))
    
    key_words = []
    # Keep only meaningful words
    for token in tokens:
        if token.isalnum() and token not in STOP_WORDS:
            key_words.append(token)
    return key_words

# print(extract_key_words("hey i want to know about iphone 13 air how much will it cost"))

# ============================================================
# 5. RETRIEVAL — FIND RELEVANT INFORMATION
# ============================================================

def get_relevent_data(question, top_k=5):

    # Get keywords from user question
    keywords = extract_key_words(question)

    # Load complete knowledge base
    full_knowledge = load_knowlade_base()

    scored_lines = []

    # Check every line in knowledge base
    for line in full_knowledge:
        line_lower = line.lower()

        score = 0

        # Count keyword matches
        for keyword in keywords:
            if keyword in line_lower:
                score +=1
        # Keep lines that contain keywords
        if score > 0:
            scored_lines.append((score,line))

    # Sort by highest score
    scored_lines.sort(
        key=lambda x: x[0],
        reverse=True
    )

     # Select top relevant lines
    relevant_data = [
        line
        for score, line in scored_lines[:top_k]
    ]

    return "".join(relevant_data)

# ============================================================
# 6. AUGMENTATION + GENERATION
# ============================================================

def ask_ai(question):
    # --------------------------------------------------------
    # RETRIEVAL
    # --------------------------------------------------------

    relevent_data = relevent_data(question)
    if not relevent_data:
        print(
            "\nAI: I couldn't find relevant information "
            "in the Apple knowledge base.\n"
        )

        return
        


