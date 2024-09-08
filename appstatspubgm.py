import os
import json
import streamlit as st
from google.cloud import vision
from PIL import Image  # Pillow library to handle images
from io import BytesIO  # To handle binary image data
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

# Fonction pour extraire les données spécifiques à partir du texte OCR
def extract_player_data(ocr_text):
    # Utilise des expressions régulières pour capturer les informations demandées.
    # Exemple : Nom du joueur, Kills, Assists, Dégâts, Durée de survie
    # Ce regex va chercher les noms de joueurs et les statistiques.
    
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

# Interface pour l'upload d'image
uploaded_file = st.file_uploader("Choisissez un screenshot à uploader", type=["png", "jpg", "jpeg", "webp", "jfif"])

if uploaded_file is not None:
    # Affichage de l'image uploadée
    image = Image.open(uploaded_file)
    st.image(image, caption="Image uploadée.", use_column_width=True)

    # Extraction du texte avec Google Cloud Vision
    st.write("Extraction du texte avec Google Cloud Vision...")
    ocr_text = ocr_google_cloud(image)

    # Afficher le texte extrait brut (optionnel)
    st.write("Texte brut extrait :")
    st.text(ocr_text)

    # Extraire les données du joueur
    player_stats = extract_player_data(ocr_text)

    # Afficher les données extraites
    if player_stats:
        st.write("Données extraites :")
        for player in player_stats:
            st.write(f"Joueur : {player['player_name']}, Kills : {player['kills']}, Assists : {player['assists']}, Dégâts : {player['damage']}, Temps de survie : {player['survival_time']} Min")
    else:
        st.write("Aucune donnée valide trouvée.")
