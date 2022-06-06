import streamlit as st
from streamlit import caching
import pandas as pd
from datetime import datetime, date

def cache_clear_dt(dummy):
   clear_dt = date.today()
   return clear_dt
if cache_clear_dt("dummy")<date.today():
   caching.clear_cache()

#st.session_state.n_init=0    
if 'n_init' not in st.session_state:
	st.session_state.n_init = 0

if st.session_state.n_init ==7:
	st.session_state.n_init = 0 
if 'liste_num' not in st.session_state:
    st.session_state.liste_num = []
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
        if num_tel in st.session_state.liste_num:
            st.write("Vous ne pouvez pas vous inscrire, vous êtes déjà sur la liste")
        else:
            
            st.session_state.liste_num.append(str(num_tel))
            now=datetime.now()
            st.session_state.n_init=st.session_state.n_init+1
            #dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            dt_jour=now.strftime("%d/%m/%Y")
            dt_heure = now.strftime("%H:%M:%S")
            st.write("Bonjour "+Prenom)
            st.write("Nous sommes le ",dt_jour)
            st.write("Il est : ", dt_heure)
            st.write("Vous êtes le numéro "+str(st.session_state.n_init))
            #results = Prenom+Nom+'@gmail.com'
            #st.write(results)
        
if __name__=='__main__':
    main()