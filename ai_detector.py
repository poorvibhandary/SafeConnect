from transformers import pipeline

# =========================
# LOAD TOXIC-BERT MODEL
# =========================

classifier = pipeline(
    "text-classification",
    model="unitary/toxic-bert"
)

# =========================
# AI DETECTION FUNCTION
# =========================

def detect_toxicity(message):

    text = message.lower().strip()

    # =========================
    # ONLINE GROOMING PHRASES
    # =========================

    grooming = [

        "send your photo",
        "send me your photo",
        "share your picture",
        "share your photo",
        "send me a selfie",
        "where do you live",
        "what is your address",
        "what school do you go to",
        "don't tell your parents",
        "keep this secret",
        "meet me",
        "come alone",
        "let's meet",
        "give me your number",
        "video call me",
        "come to my house",
        "i won't tell anyone"

    ]

    for phrase in grooming:

        if phrase in text:
            return "toxic", 0.99, "👤 Online Grooming"

    # =========================
    # CYBERBULLYING PHRASES
    # =========================

    bullying = [

        "go away",
        "nobody wants you",
        "leave us alone",
        "get lost",
        "stay away",
        "you don't belong",
        "everyone hates you",
        "no one likes you",
        "nobody likes you",
        "you're disgusting",
        "you are disgusting",
        "disguisting",
        "idiot",
        "stupid",
        "loser",
        "dumb",
        "ugly",
        "moron",
        "pathetic",
        "worthless",
        "shut up",
        "kill yourself",
        "i hate you",
        "you are useless",
        "cry baby",
        "freak",
        "weirdo"

    ]

    for phrase in bullying:

        if phrase in text:
            return "toxic", 0.99, "🚫 Cyberbullying"

    # =========================
    # TOXIC-BERT AI DETECTION
    # =========================

    result = classifier(message)

    label = result[0]["label"].lower()
    score = result[0]["score"]

    if label == "toxic" and score >= 0.50:
        return "toxic", score, "⚠ Toxic Language"

    # =========================
    # SAFE MESSAGE
    # =========================

    return "non-toxic", score, "✅ Safe"