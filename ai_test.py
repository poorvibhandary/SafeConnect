from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="unitary/toxic-bert"
)

result = classifier("You are stupid and ugly")

print(result)