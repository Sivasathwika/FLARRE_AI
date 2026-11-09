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

print(score("how long is the waiting period?", chunks[0]))
print(score("how long is the waiting period?", chunks[1]))

def retrieve(question):
    best_score = 0
    best_chunk = None
    for chunk in chunks:
        sc = score(question, chunk)
        if sc > best_score:
            best_score = sc
            best_chunk = chunk
    return best_chunk

print(retrieve("how long is the waiting period?"))
print(retrieve("when must I file a claim?"))
print(retrieve("what is the capital of France?"))

def build_prompt(question):
    chunk = retrieve(question)
    if chunk is None:
        return None
    return(
        "Answer the question using ONLY the policy text below. "
        "If the answer is not in the text, say you don't know.\n\n"
        "Reply as JSON with two keys: answer and source, where source is the exact policy text you used.\n"
        "Policy text: " + chunk + "\n\n"
        "Question: " + question
    )

print(build_prompt("how long is the waiting period?"))

def answer(question):
    prompt = build_prompt(question)
    if prompt is None:
        return "I could not find this in the policy."

    return prompt

print(answer("how long is the waiting period?"))
print(answer("what is the capital of France?"))

test_set = [
    ("how long is the waiting period?", chunks[0]),
    ("when must I file a claim?", chunks[1]),
    ("does the policy cover cosmetic surgery?", chunks[2]),
    ("how many days do I have to submit a claim?", chunks[1]),
    ("what is the capital of France?", None),
]


def hit_rate():
    correct = 0
    for test in test_set:
        question, chunk = test
        retrieved_chunk = retrieve(question)
        if retrieved_chunk == chunk:
            correct += 1
        else:
            print("FAILED: ", question)
    return correct/len(test_set)

print(hit_rate())

q = words("how many days do I have to submit a claim?")
for c in chunks:
    print(q & words(c), "->", score("how many days do I have to submit a claim?", c))