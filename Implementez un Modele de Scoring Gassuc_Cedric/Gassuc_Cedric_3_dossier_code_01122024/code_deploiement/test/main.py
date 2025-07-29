import streamlit as st
import pandas as pd
import requests

# URL de l'API déployée
URL_BASE = 'https://api-scoring-415253312919.europe-west9.run.app'

def envoyer_pour_prediction(donnees):
    """ Envoie les données à l'API et récupère les prédictions. """
    try:
        response = requests.post(f"{URL_BASE}/predire", json=donnees)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur API : {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Erreur de connexion à l'API : {e}")
        return None

def main():
    st.title("Application de prédiction de prêt")
    st.write("Téléversez un fichier CSV contenant les données d'un ou plusieurs clients.")

    fichier = st.file_uploader("Choisissez un fichier CSV", type='csv')
    
    if fichier is not None:
        donnees = pd.read_csv(fichier)

        st.subheader("Données chargées")
        st.dataframe(donnees)

        if st.button("Lancer la prédiction"):
            resultats = []

            for index, row in donnees.iterrows():
                donnees_api = row.to_dict()
                prediction = envoyer_pour_prediction(donnees_api)
                
                if prediction:
                    resultats.append({
                        "Client": index + 1,
                        "Prédiction": prediction.get("prediction"),
                        "Probabilité": round(prediction.get("probabilite_pret", 0), 4),
                        "Décision": prediction.get("decision", "Indisponible")
                    })
                else:
                    resultats.append({
                        "Client": index + 1,
                        "Prédiction": "Erreur",
                        "Probabilité": "Erreur",
                        "Décision": "Erreur"
                    })

            st.subheader("Résultats des prédictions")
            st.dataframe(pd.DataFrame(resultats))
        else:
            st.info("Cliquez sur 'Lancer la prédiction' pour obtenir les résultats.")

if __name__ == "__main__":
    main()