import streamlit as st
import sqlite3
import datetime

# Identifiant du propriétaire
owner_id = "1234"

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
today = datetime.datetime.now().strftime('%Y-%m-%d')
c.execute(f"SELECT COUNT(*) FROM clients WHERE date LIKE '{today}%'")
result = c.fetchone()
num_attente = result[0] + 1

# Réinitialisation du numéro d'attente à minuit
maintenant = datetime.datetime.now()
minuit = maintenant.replace(hour=0, minute=0, second=0, microsecond=0)
if maintenant == minuit:
    c.execute("DELETE FROM clients")
    num_attente = 1

# Vérification si le numéro de téléphone est déjà dans la file d'attente
def check_duplicate_phone_num(phone_num):
    c.execute(f"SELECT COUNT(*) FROM clients WHERE telephone = ? AND date LIKE '{today}%' ", (phone_num,))
    result = c.fetchone()
    if result[0] >= 1:
        return True
    return False

# Vérification si l'utilisateur est le propriétaire
def is_owner(user_id):
    return user_id == owner_id

# Affichage de la page web
st.title("Salon de coiffure")

nom = st.text_input("Nom :")
telephone = st.text_input("Téléphone :")

if check_duplicate_phone_num(telephone):
    st.warning("Ce numéro est déjà dans la file d'attente.")
else:
    if st.button("Soumettre"):
        # Ajout du client dans la base de données
        c.execute("INSERT INTO clients (nom, telephone) VALUES (?, ?)", (nom, telephone))
        conn.commit()

        # Récupération du numéro d'attente
        c.execute(f"SELECT COUNT(*) FROM clients WHERE date LIKE '{today}%'")
        result = c.fetchone()
        num_attente = result[0]

        # Affichage du numéro d'attente
        st.write("Votre numéro d'attente est :", num_attente)

# Affichage de la liste des clients en attente pour le propriétaire uniquement
if is_owner(st.session_state.user_id):
    if st.button("Voir la liste des clients en attente"):
        c.execute(f"SELECT * FROM clients WHERE date LIKE '{today}%' ORDER BY id ASC")
        results = c.fetchall()

        if len(results) == 0:
            st.write("Aucun client en attente pour le moment.")
        else:
            st.write("Liste des clients en attente :")
            table = []
            for row in results:
                table.append([row[0], row[1], row[2]])
            st.table(table)
else:
    st.warning("Vous n'êtes pas autorisé à accéder à cette fonctionnalité.")
