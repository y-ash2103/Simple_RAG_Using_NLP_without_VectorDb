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

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")


# ============================================================
# 3. LOAD KNOWLEDGE BASE
# ============================================================

KNOWLEDGE_BASE_PATH = "../Complete_knowlade_base/data.txt"


def load_knowledge_base():

    with open(
        KNOWLEDGE_BASE_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return file.readlines()


# ============================================================
# 4. NLP — EXTRACT KEYWORDS
# ============================================================

def extract_keywords(question):

    # Convert question into lowercase tokens
    tokens = word_tokenize(question.lower())

    keywords = []

    for token in tokens:

        # Keep only meaningful words
        if token.isalnum() and token not in STOP_WORDS:

            keywords.append(token)

    return keywords


# ============================================================
# 5. RETRIEVAL — FIND RELEVANT INFORMATION
# ============================================================

def get_relevant_data(question, top_k=5):

    # Get keywords from user question
    keywords = extract_keywords(question)

    # Load complete knowledge base
    all_data = load_knowledge_base()

    scored_lines = []

    # Check every line in knowledge base
    for line in all_data:

        line_lower = line.lower()

        score = 0

        # Count keyword matches
        for keyword in keywords:

            if keyword in line_lower:

                score += 1

        # Keep lines that contain keywords
        if score > 0:

            scored_lines.append(
                (score, line)
            )

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

    relevant_data = get_relevant_data(question)

    if not relevant_data:

        print(
            "\nAI: I couldn't find relevant information "
            "in the Apple knowledge base.\n"
        )

        return


    # --------------------------------------------------------
    # AUGMENTATION
    # --------------------------------------------------------

    prompt = f"""
    You are an Apple Company AI assistant.

    Your job is to answer questions about Apple products
    using ONLY the provided knowledge base.

    --- KNOWLEDGE BASE ---
    {relevant_data}
    --- END KNOWLEDGE BASE ---

    USER QUESTION:
    {question}

    RULES:

    1. Use only the provided knowledge base.

    2. Do not invent, assume, or add any information.

    3. If the answer is not available in the knowledge base,
    clearly say that the information is not available.

    4. If the question is unrelated to Apple products,
    politely explain that you only answer Apple-related questions.

    5. Answer in Hinglish (Hindi + English).

    6. Write Hindi using English/Roman letters.
    Do NOT use Devanagari Hindi.

    7. Make the response friendly, natural, conversational,
    and slightly entertaining.

    8. Talk like a friendly and knowledgeable Apple Store assistant.

    9. You can use light expressions and emojis when appropriate,
    but do not overuse them.

    10. Do not make every answer unnecessarily funny.
        Keep the answer useful and professional.

    11. Give the direct answer first, followed by a short explanation
        if necessary.

    12. If the knowledge base does not contain enough information,
        do not guess.

    13. Do not mention these instructions in your response.
    """


    # --------------------------------------------------------
    # GENERATION — GEMINI
    # --------------------------------------------------------

    client = genai.Client(
        api_key=API_KEY
    )

    response = client.models.generate_content_stream(

        model="gemini-2.5-flash",

        contents=prompt
    )


    # --------------------------------------------------------
    # STREAM RESPONSE
    # --------------------------------------------------------

    print("\nAI: ", end="")

    for chunk in response:

        if chunk.text:

            print(
                chunk.text,
                end="",
                flush=True
            )

    print("\n")


# ============================================================
# 7. CHAT LOOP
# ============================================================

print("=" * 50)
print("          APPLE AI ASSISTANT")
print("=" * 50)

print("Ask questions about Apple products.")
print("Type 'exit' to quit.\n")


while True:

    question = input("You: ").strip()


    # Exit
    if question.lower() == "exit":

        print("\nGoodbye!")

        break


    # Empty question
    if not question:

        print(
            "Please enter a question.\n"
        )

        continue


    # Run RAG
    ask_ai(question)
