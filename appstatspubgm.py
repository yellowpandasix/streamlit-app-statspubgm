import os
import json
import pandas as pd
import streamlit as st
from google.cloud import vision
from PIL import Image
from io import BytesIO
import re

# Credentials Google Cloud directement dans le code
google_credentials = {
    "type": "service_account",
    "project_id": "statspubgm",
    "private_key_id": "b0ca8e3cea59248c1a7c0fb5b11d19e947af4962",
    "private_key": """-----BEGIN PRIVATE KEY-----
    MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCu/44PiyL1K/Ky
    [TON CONTENU ICI]
    -----END PRIVATE KEY-----""",
    "client_email": "vision-api-service-account@statspubgm.iam.gserviceaccount.com",
    "client_id": "114232901550525951093",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/vision-api-service-account%40statspubgm.iam.gserviceaccount.com"
}

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
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()

        image_data = vision.Image(content=img_bytes)
        response = client.text_detection(image=image_data)
        texts = response.text_annotations

        return texts[0].description if texts else "Aucun texte détecté"
    
    except Exception as e:
        st.error(f"Erreur lors de l'extraction du texte : {e}")
        return ""

# Fonction pour extraire les données spécifiques à partir du texte OCR
def extract_player_data(ocr_text):
    player_data = []
    regex_pattern = r"(?P<player_name>[A-Za-z0-9]+)\s+(?P<kills>\d+)\s+(?P<assists>\d+)\s+(?P<damage>\d+)\s+(?P<survival_time>[0-9]+[.,]?[0-9]*)\s+Min"
    matches = re.finditer(regex_pattern, ocr_text)

    for match in matches:
        data = {
            "player_name": match.group("player_name"),
            "kills": match.group("kills"),
            "assists": match.group("assists"),
            "damage": match.group("damage"),
            "survival_time": match.group("survival_time"),
        }
        player_data.append(data)
    
    return player_data

# Créer un tableau pour stocker les résultats
final_data = []

# Demander les informations globales de la partie
date = st.text_input("Entrez la date du match (dd/mm/yyyy):")
month = st.selectbox("Sélectionnez le mois :", ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"])
year = st.text_input("Entrez l'année :")
week = st.text_input("Entrez la semaine :")

# Interface pour l'upload d'image
uploaded_file = st.file_uploader("Choisissez un screenshot à uploader", type=["png", "jpg", "jpeg", "webp", "jfif"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Image uploadée.", use_column_width=True)

    st.write("Extraction du texte avec Google Cloud Vision...")
    ocr_text = ocr_google_cloud(image)

    st.write("Texte brut extrait :")
    st.text(ocr_text)

    player_stats = extract_player_data(ocr_text)

    if player_stats:
        for player in player_stats:
            final_data.append({
                "Players": player["player_name"],
                "Date": date,
                "Month": month,
                "Year": year,
                "Week": week,
                "Kills": player["kills"],
                "Assist": player["assists"],
                "Damage": player["damage"],
                "Survival time": player["survival_time"]
            })
        st.write("Données ajoutées au tableau.")
    else:
        st.write("Aucune donnée valide trouvée.")

# Afficher le tableau final
if final_data:
    df = pd.DataFrame(final_data)
    st.write("Tableau final des statistiques :")
    st.dataframe(df)

    # Téléchargement du tableau en fichier Excel
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(df)
    st.download_button("Télécharger le tableau en CSV", data=csv, file_name="statistiques_pubgm.csv", mime="text/csv")
