# 🧠 RAG Using NLP Without Vector Database

> A beginner-friendly **Retrieval-Augmented Generation (RAG)** project that uses **NLP-based keyword retrieval** and **Google Gemini** to answer questions from a custom knowledge base — without embeddings or a vector database.

🔗 **GitHub Repository:** [RAG_Using_NLP_without_VectorDb](https://github.com/y-ash2103/Simple_RAG_Using_NLP_without_VectorDb)

---

## 📌 Overview

This project demonstrates how a simple RAG system can be built from scratch using traditional NLP techniques.

Instead of using:

* ❌ Embeddings
* ❌ Vector databases
* ❌ FAISS
* ❌ ChromaDB
* ❌ Pinecone
* ❌ LangChain

this project uses **NLTK keyword extraction and keyword matching** to retrieve relevant information from a `.txt` knowledge base.

The retrieved information is then provided to **Google Gemini**, which generates the final answer.

This makes the project especially useful for beginners who want to understand the fundamental idea behind RAG before moving to embedding-based retrieval.

---

## 🤖 What is RAG?

**RAG = Retrieval-Augmented Generation**

A RAG system combines:

```text
Retrieval + Context + Generation
```

Instead of asking an AI model to answer a question entirely from its own knowledge, the system first retrieves relevant information from an external knowledge base and provides that information to the model.

### Traditional RAG

```text
Documents
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector Database
    ↓
Similarity Search
    ↓
Relevant Context
    ↓
LLM
    ↓
Answer
```

### This Project

```text
data.txt
    ↓
Read Knowledge Base
    ↓
User Question
    ↓
NLTK Keyword Extraction
    ↓
Keyword Matching
    ↓
Score Each Line
    ↓
Sort by Score
    ↓
Select Top-K Lines
    ↓
Relevant Context
    ↓
Gemini
    ↓
Answer
```

---

## 🎯 Project Objective

The main objective of this project is to understand the basic working of RAG without immediately jumping into complex vector databases and embedding models.

It demonstrates the three major RAG stages:

### 1. Retrieval

Find information from the knowledge base that is relevant to the user's question.

### 2. Augmentation

Add the retrieved information to the prompt.

### 3. Generation

Send the augmented prompt to Gemini and generate the final answer.

---

## 🛠️ Technologies Used

| Technology       | Purpose                         |
| ---------------- | ------------------------------- |
| 🐍 Python        | Main programming language       |
| 🧠 NLTK          | NLP and keyword extraction      |
| 🤖 Google Gemini | Answer generation               |
| 📄 TXT           | Knowledge base                  |
| 🔐 python-dotenv | Environment variable management |

---

## 📂 Project Structure

```text
RAG_Using_NLP_without_VectorDb/
│
├── Complete_knowlade_base/
│   └── data.txt
│
├── PyCode/
│   └── main.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

> File names may vary depending on your local project structure.

---

## 🔄 How the System Works

### Step 1 — User asks a question

For example:

```text
What is the iPhone return policy?
```

---

### Step 2 — NLTK extracts keywords

The question is converted into tokens.

```text
"What is the iPhone return policy?"
```

becomes something similar to:

```python
["iphone", "return", "policy"]
```

Common English stopwords such as:

```text
what
is
the
```

are removed.

---

### Step 3 — Search the knowledge base

The system reads the `data.txt` file line by line.

For every line, it checks whether the extracted keywords are present.

Example:

```text
iPhone products can be returned within 14 days.
```

Matches:

```text
iphone  ✓
return  ✓
policy  ✗
```

Therefore:

```text
Score = 2
```

---

### Step 4 — Rank the results

Every matching line receives a score.

For example:

```text
Score 3 → The iPhone return policy requires proof of purchase.
Score 2 → iPhone products can be returned within 14 days.
Score 1 → iPhone has a one-year warranty.
```

The results are sorted from highest score to lowest score.

```python
scored_lines.sort(
    key=lambda x: x[0],
    reverse=True
)
```

The system then selects the top relevant lines.

---

### Step 5 — Augment the prompt

The retrieved information is inserted into the Gemini prompt.

Conceptually:

```text
Knowledge Base:
------------------------------
Relevant line 1
Relevant line 2
Relevant line 3
------------------------------

User Question:
What is the iPhone return policy?
```

---

### Step 6 — Gemini generates the answer

Google Gemini receives:

```text
Retrieved Context
        +
User Question
```

and generates the final response.

The prompt instructs Gemini to use only the retrieved knowledge.

---

## 🧩 Core Retrieval Logic

The retrieval system follows this basic logic:

```python
keywords = extract_keywords(question)

all_data = load_knowledge_base()

scored_lines = []

for line in all_data:

    score = 0

    for keyword in keywords:

        if keyword in line.lower():

            score += 1

    if score > 0:

        scored_lines.append(
            (score, line)
        )
```

Then:

```python
scored_lines.sort(
    key=lambda x: x[0],
    reverse=True
)
```

And finally:

```python
relevant_data = [
    line
    for score, line in scored_lines[:top_k]
]
```

This gives Gemini the most keyword-relevant information.

---

## 🌟 Example

### User

```text
What is AppleCare?
```

### Retrieval

The system searches the knowledge base for keywords such as:

```text
applecare
```

and retrieves relevant lines.

### Gemini

Gemini receives the retrieved information and generates an answer based only on that context.

Example style:

```text
🍎 AppleCare is Apple's additional service and support program.

Iske through additional technical support aur service coverage
mil sakti hai. Coverage aapke specific AppleCare plan par depend
karti hai.
```

---

## 🚫 What This Project Does NOT Use

This project intentionally does not use:

```text
❌ Text embeddings
❌ Vector databases
❌ FAISS
❌ ChromaDB
❌ Pinecone
❌ Weaviate
❌ Semantic similarity
❌ LangChain
```

The retrieval mechanism is based on:

```text
NLP
+
Keyword Matching
+
Scoring
+
Ranking
```

---

## ⚖️ Advantages

### ✅ Beginner Friendly

The entire retrieval process can be understood without advanced mathematics.

### ✅ Easy to Debug

You can print the keywords, scores, and retrieved lines to understand exactly what the retriever is doing.

### ✅ No Vector Database

There is no need to configure or maintain a vector database.

### ✅ Low Complexity

The project uses basic Python, NLTK, and Gemini.

### ✅ Good Learning Project

It provides a simple foundation for understanding RAG before moving to embeddings.

---

## ⚠️ Limitations

Because this project uses keyword matching, it has some important limitations.

### 1. No Semantic Understanding

For example:

```text
price
```

and

```text
cost
```

may have similar meanings to humans, but keyword matching does not understand that relationship.

### 2. Exact Keyword Dependency

If the user's wording is very different from the knowledge-base wording, relevant information may not be retrieved.

### 3. Simple Ranking

The score is simply based on the number of matching keywords.

```text
More matching keywords
        ↓
Higher score
        ↓
Higher retrieval priority
```

### 4. Not Designed for Large Knowledge Bases

Searching every line of a very large document can become inefficient.

These limitations are exactly why modern RAG systems commonly use embeddings and vector or other semantic retrieval methods.

---

## 🔐 Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Do **not** upload your actual API key to GitHub.

Make sure `.env` is included in `.gitignore`.

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/y-ash2103/Simple_RAG_Using_NLP_without_VectorDb.git
```

### 2. Open the project

```bash
cd Simple_RAG_Using_NLP_without_VectorDb
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS/Linux

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Add your Gemini API key

Create:

```text
.env
```

and add:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## ▶️ Run the Project

Run your Python file:

```bash
python main.py
```

or use the appropriate path for your project structure.

You should see something similar to:

```text
==================================================
             APPLE AI ASSISTANT
==================================================

Ask questions about Apple products.
Type 'exit' to quit.

You:
```

Now ask your question.

Example:

```text
You: What is the return policy for iPhone?
```

---

## 🧪 Example Questions

Try questions such as:

```text
What is the return policy?
```

```text
What is AppleCare?
```

```text
What is the warranty policy?
```

```text
Can I cancel my order?
```

```text
What is Apple Trade In?
```

```text
What are the Mac products?
```

```text
What is the iPhone service policy?
```

---

## 🧠 RAG Architecture

```text
                    USER
                     │
                     ▼
              ┌──────────────┐
              │   Question   │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │     NLTK     │
              │   NLP        │
              └──────┬───────┘
                     │
                     ▼
             ┌───────────────┐
             │    Keywords   │
             └───────┬───────┘
                     │
                     ▼
          ┌─────────────────────┐
          │     data.txt        │
          │  Knowledge Base     │
          └──────────┬──────────┘
                     │
                     ▼
          ┌─────────────────────┐
          │  Keyword Matching   │
          │       + Score       │
          └──────────┬──────────┘
                     │
                     ▼
          ┌─────────────────────┐
          │    Top-K Results    │
          └──────────┬──────────┘
                     │
                     ▼
          ┌─────────────────────┐
          │   Retrieved Context │
          └──────────┬──────────┘
                     │
                     ▼
          ┌─────────────────────┐
          │   Gemini Prompt     │
          │ Context + Question  │
          └──────────┬──────────┘
                     │
                     ▼
              ┌──────────────┐
              │    Gemini    │
              │ 2.5 Flash    │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │    Answer    │
              └──────────────┘
```

---

## 🚀 Future Improvements

This project can be extended step by step.

### Level 1 — Improve NLP Retrieval

* TF-IDF
* Stemming
* Lemmatization
* Better text preprocessing
* Fuzzy matching

### Level 2 — Embedding-Based RAG

Replace keyword matching with:

```text
Text
 ↓
Embeddings
 ↓
Vector representation
 ↓
Similarity search
 ↓
Relevant context
 ↓
Gemini
```

### Level 3 — Vector Database

The project can later be extended using:

```text
FAISS
ChromaDB
Pinecone
Weaviate
```

### Level 4 — User Interface

A Streamlit interface can be added:

```text
User
 ↓
Streamlit UI
 ↓
RAG Pipeline
 ↓
Gemini
 ↓
Answer
```

---

## 📚 Learning Path

If you are learning RAG, a useful progression is:

```text
1. Keyword-Based RAG
        ↓
2. TF-IDF Retrieval
        ↓
3. Embeddings
        ↓
4. Vector Similarity
        ↓
5. Vector Database
        ↓
6. Advanced RAG
```

This project represents the **first stage** of that journey.

---

## 🎓 Why I Built This

This project was created as a learning exercise to understand the fundamental architecture of **Retrieval-Augmented Generation** without hiding the retrieval process behind frameworks or vector databases.

The goal is to understand:

```text
How do we retrieve information?
        ↓
How do we provide it to an LLM?
        ↓
How does the LLM generate an answer?
```

Once these fundamentals are clear, more advanced RAG architectures become much easier to understand.

---

## 👨‍💻 Author

**Yash**

GitHub: [@y-ash2103](https://github.com/y-ash2103)

---

## ⭐ If You Found This Useful

If this project helped you understand the basics of RAG, consider giving the repository a ⭐ on GitHub.

---

## 📄 License

This project is intended primarily for educational and learning purposes.
