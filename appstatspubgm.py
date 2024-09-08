import os
import json
import streamlit as st
from google.cloud import vision
from PIL import Image  # Pillow library to handle images
from io import BytesIO  # To handle binary image data

# Récupérer les credentials Google Cloud depuis les secrets Streamlit
google_credentials = st.secrets["google_cloud_key"]

# Écrire les credentials dans un fichier temporaire
with open("google_credentials.json", "w") as f:
    json.dump(google_credentials, f)

# Définir la variable d'environnement pour utiliser le fichier JSON des credentials Google Cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_credentials.json"

# Initialiser le client Google Cloud Vision
client = vision.ImageAnnotatorClient()

# Fonction pour utiliser l'API Google Cloud Vision pour détecter du texte dans une image
def ocr_google_cloud(image):
    try:
        # Transformation de l'image en format binaire
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()

        # Utilisation de Google Cloud Vision pour détecter le texte dans l'image
        image_data = vision.Image(content=img_bytes)
        response = client.text_detection(image=image_data)
        texts = response.text_annotations

        # Retourne le texte principal détecté
        return texts[0].description if texts else "Aucun texte détecté"
    
    except Exception as e:
        st.error(f"Erreur lors de l'extraction du texte : {e}")
        return ""

# Interface pour l'upload d'image
uploaded_file = st.file_uploader("Choisissez un screenshot à uploader", type=["png", "jpg", "jpeg", "webp", "jfif"])

if uploaded_file is not None:
    # Affichage de l'image uploadée
    image = Image.open(uploaded_file)
    st.image(image, caption="Image uploadée.", use_column_width=True)

    # Extraction du texte avec Google Cloud Vision
    st.write("Extraction du texte avec Google Cloud Vision...")
    ocr_text = ocr_google_cloud(image)

    # Afficher le texte extrait
    st.write("Texte extrait :")
    st.text(ocr_text)
