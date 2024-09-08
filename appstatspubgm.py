import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd
from io import BytesIO

# Titre de l'application
st.title("Application de Génération de Statistiques - PUBG Mobile")

# Fonction d'OCR pour extraire le texte des images
def ocr_extract(image):
    text = pytesseract.image_to_string(image)
    return text

# Fonction pour traiter les données et les transformer en tableau
def process_ocr_data(ocr_text):
    rows = ocr_text.split("\n")
    data = []
    for row in rows:
        # Filtrer les lignes non pertinentes
        if any(char.isdigit() for char in row):
            columns = row.split()  # Séparer les colonnes (tu peux ajuster en fonction du format de tes images)
            data.append(columns)
    
    # Transformer en DataFrame Pandas
    df = pd.DataFrame(data, columns=["Player", "Kills", "Assists", "Damage", "Survival Time"])
    return df

# Interface utilisateur pour uploader l'image
uploaded_file = st.file_uploader("Choisissez un screenshot à uploader", type=["png", "jpg", "jpeg", "webp", "jfif"])

if uploaded_file is not None:
    # Ouvrir l'image
    image = Image.open(uploaded_file)
    st.image(image, caption="Screenshot uploaded.", use_column_width=True)

    # Extraire le texte de l'image
    st.write("Extraction du texte à partir de l'image...")
    ocr_text = ocr_extract(image)

    # Afficher le texte extrait
    st.write("Texte OCR extrait :")
    st.text(ocr_text)

    # Traiter le texte OCR et générer un tableau
    st.write("Tableau des statistiques généré :")
    df_stats = process_ocr_data(ocr_text)
    st.write(df_stats)

    # Permettre à l'utilisateur de télécharger les données en Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_stats.to_excel(writer, index=False)
        writer.save()
    processed_data = output.getvalue()

    st.download_button(label="Télécharger les statistiques en Excel",
                       data=processed_data,
                       file_name="stats_pubgm.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
