import os
import json
import streamlit as st
from PIL import Image
import pandas as pd
from io import BytesIO
from google.cloud import vision

# Configuration du titre de l'application
st.title("Application de Génération de Statistiques - PUBG Mobile")

# Récupérer les informations d'authentification depuis les secrets GitHub ou environnement
google_credentials = os.getenv("VISION_OCR_STATS_PUBGM")

# Créer un fichier temporaire pour les credentials Google Cloud
if google_credentials:
    with open("google_credentials.json", "w") as f:
        f.write(google_credentials)

# Définir la variable d'environnement pour Google Cloud Vision
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_credentials.json"

# Initialiser le client de Google Cloud Vision
client = vision.ImageAnnotatorClient()

# Fonction pour extraire le texte d'une image via Google Cloud Vision
def ocr_google_cloud(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()

    image = vision.Image(content=img_bytes)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # Si du texte est détecté, renvoyer le texte principal
    if texts:
        return texts[0].description
    else:
        return ""

# Fonction pour traiter les données OCR et les transformer en tableau
def process_ocr_data(ocr_text):
    rows = ocr_text.split("\n")
    data = []
    for row in rows:
        # Exemple de filtrage des lignes contenant des informations pertinentes
        if any(char.isdigit() for char in row):  # Filtrer les lignes avec des chiffres
            columns = row.split()  # Séparer en colonnes
            data.append(columns)

    # Créer un DataFrame Pandas avec les colonnes souhaitées
    df = pd.DataFrame(data, columns=["Player", "Kills", "Assists", "Damage", "Survival Time"])
    return df

# Interface utilisateur pour uploader une image
uploaded_file = st.file_uploader("Choisissez un screenshot à uploader", type=["png", "jpg", "jpeg", "webp", "jfif"])

# Si un fichier est uploadé
if uploaded_file is not None:
    # Ouvrir et afficher l'image
    image = Image.open(uploaded_file)
    st.image(image, caption="Screenshot uploaded.", use_column_width=True)

    # Extraire le texte de l'image via Google Cloud Vision API
    st.write("Extraction du texte à partir de l'image via Google Cloud Vision...")
    ocr_text = ocr_google_cloud(image)

    # Afficher le texte extrait
    st.write("Texte OCR extrait :")
    st.text(ocr_text)

    # Traiter le texte OCR et générer un tableau
    st.write("Tableau des statistiques généré :")
    df_stats = process_ocr_data(ocr_text)
    st.write(df_stats)

    # Permettre à l'utilisateur de télécharger le tableau en fichier Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_stats.to_excel(writer, index=False)
        writer.save()
    processed_data = output.getvalue()

    st.download_button(label="Télécharger les statistiques en Excel",
                       data=processed_data,
                       file_name="stats_pubgm.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
