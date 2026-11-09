chunks = [
    "The waiting period is 30 days from the policy start date.",
    "Claims must be filed within 15 days of the incident.",
    "The policy covers hospital stays, but not cosmetic surgery.",
]

STOP_WORDS = {"the", "is", "of", "a", "what", "how", "when", "i"}

def words(text):
    text = text.lower()
    for mark in ["?", ".", ",", "!"]:
        text = text.replace(mark, "")
    return set(text.split()) - STOP_WORDS

def score(question, chunk):
    return len(words(question) & words(chunk))

def retrieve(question):
    best_score = 0
    best_chunk = None
    for chunk in chunks:
        sc = score(question, chunk)
        if sc > best_score:
            best_score = sc
            best_chunk = chunk
    return best_chunk

def build_prompt(question):
    chunk = retrieve(question)
    if chunk is None:
        return None
    return (
        "Answer the question using ONLY the policy text below. "
        "If the answer is not in the text, say you don't know.\n\n"
        "Policy text: " + chunk + "\n\n"
        "Question: " + question
    )

def answer(question):
    prompt = build_prompt(question)
    if prompt is None:
        return "I could not find this in the policy."
    return prompt