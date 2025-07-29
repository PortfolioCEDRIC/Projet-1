from pydantic import BaseModel, Field
from typing import Optional
import numpy as np
import pandas as pd
import pickle
from flask import Flask, request, jsonify


# Charger le modèle sauvegardé
with open('modele_lgbm.pkl', 'rb') as f:
    modele = pickle.load(f)

# Création d'une classe qui va contenir le type de données
# Définition du schéma des données d'entrée avec Pydantic
# Cela garantit que les données reçues correspondent aux attentes du modèle
class DonneesEntree(BaseModel): 
        AMT_INCOME_TOTAL: float
        AMT_CREDIT: float
        AMT_ANNUITY: float
        NAME_EDUCATION_TYPE: float
        DAYS_BIRTH: float
        DAYS_EMPLOYED: float
        FLAG_WORK_PHONE: int
        FLAG_PHONE: int
        CNT_FAM_MEMBERS: float
        REGION_RATING_CLIENT: float
        REGION_RATING_CLIENT_W_CITY: float
        HOUR_APPR_PROCESS_START: int
        REG_CITY_NOT_LIVE_CITY: int
        LIVE_CITY_NOT_WORK_CITY: int
        EXT_SOURCE_2: float
        EXT_SOURCE_3: float
        OBS_60_CNT_SOCIAL_CIRCLE: float
        DEF_60_CNT_SOCIAL_CIRCLE: float
        DAYS_LAST_PHONE_CHANGE: float
        FLAG_DOCUMENT_3: int
        FLAG_DOCUMENT_6: int
        FLAG_DOCUMENT_8: int
        AMT_REQ_CREDIT_BUREAU_HOUR: float
        AMT_REQ_CREDIT_BUREAU_DAY: float
        AMT_REQ_CREDIT_BUREAU_WEEK: float
        AMT_REQ_CREDIT_BUREAU_MON: float
        AMT_REQ_CREDIT_BUREAU_QRT: float
        AMT_REQ_CREDIT_BUREAU_YEAR: float
        categorie_enfants: float
        INTERVAL_age_client: float
        company_seniority_year: float
        update_ID: float
        Population_Segment: float
        CREDIT_INCOME_PERCENT: float
        ANNUITY_INCOME_PERCENT: float
        CREDIT_TERM: float
        DAYS_EMPLOYED_PERCENT: float
        WEEKDAY_APPR_PROCESS_START_MONDAY: bool
        WEEKDAY_APPR_PROCESS_START_SATURDAY: bool
        WEEKDAY_APPR_PROCESS_START_SUNDAY: bool
        WEEKDAY_APPR_PROCESS_START_THURSDAY: bool
        WEEKDAY_APPR_PROCESS_START_TUESDAY: bool
        WEEKDAY_APPR_PROCESS_START_WEDNESDAY: bool
        NAME_HOUSING_TYPE_House_apartment: bool
        NAME_HOUSING_TYPE_Municipal_apartment: bool
        NAME_HOUSING_TYPE_Office_apartment: bool
        NAME_HOUSING_TYPE_Rented_apartment: bool
        NAME_HOUSING_TYPE_With_parents: bool
        NAME_FAMILY_STATUS_Married: bool
        NAME_FAMILY_STATUS_Separated: bool
        NAME_FAMILY_STATUS_Single_not_married: bool
        NAME_FAMILY_STATUS_Widow: bool
        NAME_INCOME_TYPE_Employ_: bool 
        NAME_INCOME_TYPE_sans_emploi: bool
        souscription_au_pret: float
        FLAG_OWN_CAR_Y: bool
        CODE_GENDER_M: bool
        NAME_CONTRACT_TYPE_Revolving_loans: bool
        FLAG_OWN_REALTY_Y: bool
        OCCUPATION_TYPE_Cleaning_staff: bool
        OCCUPATION_TYPE_Cooking_staff: bool
        OCCUPATION_TYPE_Core_staff: bool
        OCCUPATION_TYPE_Drivers: bool
        OCCUPATION_TYPE_HR_staff: bool
        OCCUPATION_TYPE_High_skill_tech_staff: bool
        OCCUPATION_TYPE_IT_staff: bool
        OCCUPATION_TYPE_Laborers: bool
        OCCUPATION_TYPE_Low_skill_Laborers: bool
        OCCUPATION_TYPE_Managers: bool
        OCCUPATION_TYPE_Medicine_staff: bool
        OCCUPATION_TYPE_Private_service_staff: bool
        OCCUPATION_TYPE_Realty_agents: bool
        OCCUPATION_TYPE_Sales_staff: bool
        OCCUPATION_TYPE_Secretaries: bool
        OCCUPATION_TYPE_Security_staff: bool
        OCCUPATION_TYPE_Waiters_barmen_staff: bool
        EMERGENCYSTATE_MODE_Yes: bool
        NAME_TYPE_SUITE_Family: bool
        NAME_TYPE_SUITE_Group_of_people: bool
        NAME_TYPE_SUITE_Other_A: bool
        NAME_TYPE_SUITE_Other_B: bool
        NAME_TYPE_SUITE_Spouse_partner: bool
        NAME_TYPE_SUITE_Unaccompanied: bool

# Initialisation de l'application Flask
app = Flask(__name__)

@app.route("/", methods=["GET"])
def accueil():
    """ Endpoint racine qui fournit un message de bienvenue. """
    return jsonify({"message": "Bienvenue sur l'API de Prediction sur l'accord d'un prêt Bancaire"})

@app.route("/predire", methods=["POST"])
def predire():
    """
    Endpoint pour les prédictions en utilisant le modèle chargé.
    Les données d'entrée sont validées et transformées en DataFrame pour le traitement par le modèle.
    """
    if not request.json:
        return jsonify({"erreur": "Aucune donnée reçue"}), 400
    try:
        donnees = DonneesEntree(**request.json)
        donnees_df = pd.DataFrame([donnees.model_dump()])
        
        proba = float(modele.predict(donnees_df)[0])
        prediction = int(proba >= 0.5)
        # Texte de décision
        decision =  "Refusé" if prediction == 1 else "Accordé"
        return jsonify({
            "prediction": prediction,
            "probabilite_pret": round(proba, 4),
            "decision": decision
        })
    except Exception as e:
        return jsonify({"erreur": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True) # Lancement de l'application sur le port 8080
