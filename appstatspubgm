import streamlit as st
import pandas as pd
from datetime import datetime

# Titre de l'application
st.title("Application de Génération de Statistiques - PUBG Mobile")

# Demander la date du match
date_input = st.text_input("Entrez la date du match (dd/mm/yyyy) :")
if date_input:
    try:
        match_date = datetime.strptime(date_input, '%d/%m/%Y')
        week_number = match_date.isocalendar()[1]
        month_name = match_date.strftime('%B')
        st.write(f"Semaine : {week_number}, Mois : {month_name}")
    except ValueError:
        st.error("Format de date invalide. Utilisez le format dd/mm/yyyy.")

# Demander la map associée
map_name = st.selectbox("Sélectionnez la carte :", ["Erangel", "Miramar", "Sanhok", "Vikendi"])

# Initialiser les données des joueurs
player_data = {
    "Player": [],
    "Kills": [],
    "Assists": [],
    "Damage": [],
    "Survival Time (min)": []
}

# Demander la correspondance des joueurs
num_players = st.number_input("Nombre de joueurs :", min_value=1, max_value=4, value=4)
for i in range(1, num_players + 1):
    player_name = st.text_input(f"Nom du joueur GUILDPLAYER{i} :", key=f'player{i}')
    kills = st.number_input(f"Éliminations pour {player_name} :", min_value=0, key=f'kills{i}')
    assists = st.number_input(f"Assists pour {player_name} :", min_value=0, key=f'assists{i}')
    damage = st.number_input(f"Dégâts pour {player_name} :", min_value=0, key=f'damage{i}')
    survival_time = st.number_input(f"Temps de survie pour {player_name} (min) :", min_value=0.0, key=f'survival{i}')

    # Ajouter les données du joueur au dictionnaire
    if player_name:
        player_data["Player"].append(player_name)
        player_data["Kills"].append(kills)
        player_data["Assists"].append(assists)
        player_data["Damage"].append(damage)
        player_data["Survival Time (min)"].append(survival_time)

# Générer un tableau des statistiques des joueurs
if st.button("Générer les statistiques"):
    df = pd.DataFrame(player_data)
    st.write("Statistiques des joueurs :")
    st.write(df)

    # Permettre de télécharger les données sous forme de fichier Excel
    excel_data = df.to_excel(index=False)
    st.download_button(
        label="Télécharger les statistiques en Excel",
        data=excel_data,
        file_name='stats_pubgm.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
