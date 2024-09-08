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
    Lt+b+c9qGCmwfhl6ZDuq3k0l1XkxPGfKvh9dtKqjhaB4lOo8ePQ/4oCSdH90mRhp
    6uOx4kBjuNrgagX1GFJvFOX+P204AXGtJ04Hsw92y20eAgohWRk4rmYH7MZZ6Rwi
    s1fOnHf/td3eoawE8+rvQsrwmIeHPcXmyBT2RelG8RH9+8NIclQJnk1Bf68iDT0P
    9P25XsF+jUYzRGOkKg1XIoTLh4BHMTt4+R4cSkwQlsgXJLJEq/EMLfm4Z12atPcy
    RTGzCNNYhPIqHcyqUyrD3LOE8h1unBMaVHwV97bkNhii40tyPYGfMLA1UFq+5akO
    W0hrBdCjAgMBAAECggEADWWA4Y28MlqX7K4L7ivUhgGth1ZP6v+rVaxI6aGK8or2
    Qx4E1q6S9YuwOirkN5bm09EqGIwUib+Cj/EsVxzD4x5umwlixV2ESf6mkK0YVlY9
    9oxwu8QoZeayxr5POjhQ5vbq1qZ4lL90qO9jxGxT/15TysxDl+l4TbKmSH7UuTSP
    866HDDNnxKc9phSVmRqREx3+7VaohmLw01axTGIG5gO3+Lo2Fg2fjD9b2UHJnPtT
    UsAbcEamyoSzkgyhY+OWZHDmdF2QaAfIkQHgGPfAVlWetUXT+fCBaHnCmGuzR3B7
    7r9cr/enzQNztc9x+uv31s4Bpux7GAJxeVuyfv8BuQKBgQDe55Z0dqbNGJnTHMW/
    FsiSVe3WgrJiaiwYfpRU6Tg94AElx2v67J3H0pnGRdwG7vjFs8kBO0SnnNIEE+Be
    VeRhfatNm1rwOBqyPD5u+ToU9ig/2JLK6zouGg2OjySWOWeJzaeDn+NSIsOfcp5Z
    JTbd/m7voihWd3ameDNLqqj3twKBgQDI+xZXcUKMsQTsqN2npdeRwMyt406bmlzE
    7hD5e24J+FKRx4fZA0k+Oj6L+XewT9r2wuu6RraZUdykPGgGJE63M+xnkkFnia3i
    VmSX0g2KsKOR+SNB2P6WqYuh90R8fDH3TQSPlb/nzwHfOmppH3Y/EPjWavDOHWlS
    TNKGfNQ2dQKBgFNbT4xmAqKYHI4yKFD5eDAhKjwZzBO5mJvgWiAWxw18g3FZTiwb
    6DUdsJvQ7CM7opRsUzK+s0HrBy63MCSXAjzi/fibrDpBANq+ZKqjUPEdzJdzqhFw
    PeWXoJI7PXdgKDQEUCyM0jmY/obWGhlELWx/BYVfoq4TJq/CK4yUWXOpAoGAOYsK
    XobjEv0r98ZxkCp/ig+1iqPmQc70eL3gxk18uAYNPgfu8UdrlRGADvuiNSzn+Hbe
    nzrX1RYHIk7ZScjjcLjBGvZZG5fj3UX3DzDpB6iDbKv0WEoUunZYsErnpOy6MaAv
    ihzKEUjHtG45QVfstynY1StRPvJU0WeFb1QWPnECgYEA2p6P7Hq0tgfWYDuJDUdJ
    vOdbre8hI8mftRaxcuQVp006+IgVLw33QTyDbx3KGHRhuPbLSc2g2yUhVolwVEWC
    6OmltMe93ihGwXOxHAzYjdZo02Jo/zatiB8hkXEBcQubnbfRRzOaUhuGvMfHux9k
    N/glorth5VvDYdCffW16SYk=
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

# Créer un dictionnaire pour mapper les en-têtes
headers_mapping = {
    "PLAYER_NAME": ["Player", "nom_joueur"],
    "KILLS": ["Eliminations", "tueries"],
    "ASSISTS": ["Assists", "assistances"],
    "DAMAGE": ["Damage", "degats"],
    "SURVIVAL_TIME": ["Survived", "temps_survie"],
    # ajouter d'autres correspondances ici
}

# Créer un dictionnaire pour mapper les pseudos
pseudos_mapping = {
    "GUILDPLAYER1": "Wagner",
    "GUILDPLAYER2": "John",
    # ajouter d'autres correspondances ici
}

# Modifier la fonction extract_player_data pour remplacer les en-têtes et les pseudos
def extract_player_data(ocr_text):
    player_data = []
    # Utiliser une expression régulière pour extraire les en-têtes et les valeurs
    regex_pattern = r"(?P<header>[A-Z_]+):\s+(?P<value>\S+)"
    matches = re.finditer(regex_pattern, ocr_text)

    data = {}
    for match in matches:
        header = match.group("header")
        value = match.group("value")
        # Vérifier si l'en-tête extrait correspond à l'une des correspondances dans la liste
        for key, values in headers_mapping.items():
            if header in values:
                header = key
                break
        # Remplacer le pseudo par le pseudo correspondant dans le dictionnaire
        if header == "PLAYER_NAME":
            value = pseudos_mapping.get(value, value)
        data[header] = value

        # Si nous avons toutes les informations nécessaires pour un joueur, ajouter les données à la liste
        if set(headers_mapping.keys()).issubset(data.keys()):
            player_data.append(data)
            data = {}

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
                "Players": player["PLAYER_NAME"],
                "Date": date,
                "Month": month,
                "Year": year,
                "Week": week,
                "Kills": player["KILLS"],
                "Assist": player["ASSISTS"],
                "Damage": player["DAMAGE"],
                "Survival time": player["SURVIVAL_TIME"]
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
