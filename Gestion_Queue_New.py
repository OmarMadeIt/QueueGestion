import streamlit as st
import sqlite3
import datetime

# Connexion à la base de données
conn = sqlite3.connect('clients.db')
c = conn.cursor()

# Création de la table clients si elle n'existe pas
c.execute('''CREATE TABLE IF NOT EXISTS clients
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             nom TEXT,
             telephone TEXT,
             date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

# Récupération du nombre de clients en attente
c.execute("SELECT COUNT(*) FROM clients")
result = c.fetchone()
num_attente = result[0] + 1

# Réinitialisation du numéro d'attente à minuit
maintenant = datetime.datetime.now()
minuit = maintenant.replace(hour=0, minute=0, second=0, microsecond=0)
if maintenant == minuit:
    c.execute("DELETE FROM clients")
    num_attente = 1

# Affichage de la page web
st.title("Salon de coiffure")

nom = st.text_input("Nom :")
telephone = st.text_input("Téléphone :")

if st.button("Soumettre"):
    # Ajout du client dans la base de données
    c.execute("INSERT INTO clients (nom, telephone) VALUES (?, ?)", (nom, telephone))
    conn.commit()

    # Affichage du numéro d'attente
    st.write("Votre numéro d'attente est :", num_attente)
