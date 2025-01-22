import os
import json
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from flask import Flask, request, jsonify

app = Flask(__name__)

# Charger les données depuis un fichier JSON
try:
    with open("data/data.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}
    print("Fichier data.json non trouvé, vérifiez l'existence du fichier.")

# Initialiser le pipeline avec un modèle plus léger
MODEL_NAME = "typeform/distilbart-mnli-12-1"  # Modèle plus léger
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

def classify_message(message):
    classifier = pipeline("zero-shot-classification", model=model, tokenizer=tokenizer, device=-1)
    labels = ["études", "projets", "expériences", "compétences"]
    classification = classifier(message, labels)
    return classification["labels"][0]  # Étiquette principale

@app.route("/", methods=["POST"])
def chatbot():
    user_message = request.json.get("message", "").lower()

    # Réponses simples prédéfinies
    if "bonjour" in user_message or "salut" in user_message:
        return jsonify({"response": "Bonjour ! Je suis votre assistant numérique. Que souhaitez-vous savoir ?"})
    elif "merci" in user_message:
        return jsonify({"response": "Avec plaisir ! N'hésitez pas si vous avez d'autres questions."})
    elif "au revoir" in user_message or "bye" in user_message:
        return jsonify({"response": "Au revoir ! Revenez quand vous voulez."})
    else:
        # Classifier l'intention
        top_label = classify_message(user_message)

        # Logique des réponses basées sur les données JSON
        if top_label == "études":
            studies = "\n".join(
                [f"- {study['degree']} ({study['year']}) à {study['institution']}" for study in data.get("studies", [])]
            )
            response = f"Voici un aperçu de mes études :\n{studies}" if studies else "Je n'ai pas d'informations sur mes études pour l'instant."
        elif top_label == "projets":
            response = "Je n'ai pas encore ajouté de projets, mais cela viendra bientôt !"  # Placeholder
        elif top_label == "expériences":
            experiences = "\n".join(
                [f"- {exp['year']} : {exp['role']} chez {exp['company']} ({exp['description']})" for exp in data.get("experiences", [])]
            )
            response = f"Voici un aperçu de mes expériences professionnelles :\n{experiences}" if experiences else "Je n'ai pas d'informations sur mes expériences pour l'instant."
        elif top_label == "compétences":
            skills = ", ".join(data.get("skills", {}).get("technical", []))
            response = f"Voici mes compétences techniques : {skills}." if skills else "Je n'ai pas encore ajouté mes compétences techniques."
        else:
            response = "Désolé, je ne comprends pas votre demande. Essayez de poser une question sur mes études, projets, ou compétences."

        return jsonify({"response": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
