import streamlit as st
from streamlit import caching
import pandas as pd
from datetime import datetime, date
from streamlit_server_state import server_state, server_state_lock

def cache_clear_dt(dummy):
   clear_dt = date.today()
   return clear_dt
if cache_clear_dt("dummy")<date.today():
   caching.clear_cache()

with server_state_lock["n_init"]:  # Lock the "count" state for thread-safety
    if "n_init" not in server_state:
        server_state.n_init = 0
#st.session_state.n_init=0    #A ne pas réctiver
#if 'n_init' not in st.session_state:
	#st.session_state.n_init = 0

#if st.session_state.n_init ==7:
	#st.session_state.n_init = 0

with server_state_lock["liste_num"]:  # Lock the "count" state for thread-safety
    if "liste_num" not in server_state:
        server_state.liste_num = []
#if 'liste_num' not in st.session_state:
    #st.session_state.liste_num = []
now=datetime.now()
#n_init = 0
#liste_num=[]
#@st.cache
def main():
    global n_init
    st.title("Application de gestion de Queue INNOV Salon")
    st.subheader("Version Test")
    
    with st.form(key='myform'):
        Prenom = st.text_input("Prénom")
        num_tel = st.text_input("Votre numéro de téléphone")
        submit_button = st.form_submit_button("Valider")
        
    if submit_button:
        st.info("Résultats")
        #num_tel = input("Merci d'indiquer votre numéro de téléphone ? : ")
        if num_tel in server_state.liste_num:
            st.write("Vous ne pouvez pas vous inscrire, vous êtes déjà sur la liste")
        else:
            st.write("ICI")
            server_state.liste_num.append(str(num_tel))
            now=datetime.now()
            with server_state_lock.n_init:
                server_state.n_init=server_state.n_init+1
            #dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            dt_jour=now.strftime("%d/%m/%Y")
            dt_heure = now.strftime("%H:%M:%S")
            st.write("Bonjour "+Prenom)
            st.write("Nous sommes le ",dt_jour)
            st.write("Il est : ", dt_heure)
            st.write("Vous êtes le numéro "+str(server_state.n_init))
            
if __name__=='__main__':
    main()