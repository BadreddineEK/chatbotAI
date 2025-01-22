import gradio as gr
import json
from transformers import pipeline

# Charger les données depuis un fichier JSON
try:
    with open("data/data.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}
    print("Fichier data.json non trouvé, vérifiez l'existence du fichier.")

# Initialiser le pipeline NLP
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def chatbot(user_message):
    user_message = user_message.lower()

    # Réponses simples prédéfinies
    if "bonjour" in user_message or "salut" in user_message:
        return "Bonjour ! Je suis votre assistant numérique. Que souhaitez-vous savoir ?"
    elif "merci" in user_message:
        return "Avec plaisir ! N'hésitez pas si vous avez d'autres questions."
    elif "au revoir" in user_message or "bye" in user_message:
        return "Au revoir ! Revenez quand vous voulez."
    else:
        # Utilisation du modèle pour classifier les intentions
        labels = ["études", "projets", "expériences", "compétences"]
        classification = classifier(user_message, labels)
        top_label = classification["labels"][0]

        # Logique des réponses basées sur les données JSON
        if top_label == "études":
            studies = "\n".join(
                [f"- {study['degree']} ({study['year']}) à {study['institution']}" for study in data.get("studies", [])]
            )
            return f"Voici un aperçu de mes études :\n{studies}" if studies else "Je n'ai pas d'informations sur mes études pour l'instant."
        elif top_label == "projets":
            return "Je n'ai pas encore ajouté de projets, mais cela viendra bientôt !"  # Placeholder
        elif top_label == "expériences":
            experiences = "\n".join(
                [f"- {exp['year']} : {exp['role']} chez {exp['company']} ({exp['description']})" for exp in data.get("experiences", [])]
            )
            return f"Voici un aperçu de mes expériences professionnelles :\n{experiences}" if experiences else "Je n'ai pas d'informations sur mes expériences pour l'instant."
        elif top_label == "compétences":
            skills = ", ".join(data.get("skills", {}).get("technical", []))
            return f"Voici mes compétences techniques : {skills}." if skills else "Je n'ai pas encore ajouté mes compétences techniques."

        # Si aucune réponse pertinente
        return "Désolé, je ne comprends pas votre demande. Essayez de poser une question sur mes études, projets, ou compétences."

# Interface Gradio
iface = gr.Interface(fn=chatbot, inputs="text", outputs="text", title="ChatbotAI")

if __name__ == "__main__":
    iface.launch()
