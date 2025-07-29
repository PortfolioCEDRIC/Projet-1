import requests, json

# URL de base de l'API
url_base = 'https://api-scoring-415253312919.europe-west9.run.app'

# url_base = "http://127.0.0.1:8080"

# Test du endpoint d'accueil
response = requests.get(f"{url_base}/")
print(response.status_code, response.text)
print("Réponse du endpoint d'accueil:", response.text)

# Données d'exemple pour la prédiction
donnees_predire = {
    "AMT_INCOME_TOTAL": 200000.0,
    "AMT_CREDIT": 150000.0,
    "AMT_ANNUITY": 25000.5,
    "NAME_EDUCATION_TYPE": 2.0,
    "DAYS_BIRTH": -12000.0,
    "DAYS_EMPLOYED": -3650.0,
    "FLAG_WORK_PHONE": 1,
    "FLAG_PHONE": 1,
    "CNT_FAM_MEMBERS": 3.0,
    "REGION_RATING_CLIENT": 2.0,
    "REGION_RATING_CLIENT_W_CITY": 1.0,
    "HOUR_APPR_PROCESS_START": 10,
    "REG_CITY_NOT_LIVE_CITY": 0,
    "LIVE_CITY_NOT_WORK_CITY": 1,
    "EXT_SOURCE_2": 0.512,
    "EXT_SOURCE_3": 0.689,
    "OBS_60_CNT_SOCIAL_CIRCLE": 2.0,
    "DEF_60_CNT_SOCIAL_CIRCLE": 0.0,
    "DAYS_LAST_PHONE_CHANGE": -500.0,
    "FLAG_DOCUMENT_3": 1,
    "FLAG_DOCUMENT_6": 0,
    "FLAG_DOCUMENT_8": 0,
    "AMT_REQ_CREDIT_BUREAU_HOUR": 0.0,
    "AMT_REQ_CREDIT_BUREAU_DAY": 0.0,
    "AMT_REQ_CREDIT_BUREAU_WEEK": 1.0,
    "AMT_REQ_CREDIT_BUREAU_MON": 0.0,
    "AMT_REQ_CREDIT_BUREAU_QRT": 0.0,
    "AMT_REQ_CREDIT_BUREAU_YEAR": 3.0,
    "categorie_enfants": 2.0,
    "INTERVAL_age_client": 4.0,
    "company_seniority_year": 5.0,
    "update_ID": 1.0,
    "Population_Segment": 1.0,
    "souscription_au_pret": 3.0,
    "CREDIT_INCOME_PERCENT": 2.1,
    "ANNUITY_INCOME_PERCENT": 0.23,
    "CREDIT_TERM": 12.5,
    "DAYS_EMPLOYED_PERCENT": 0.15,
    "WEEKDAY_APPR_PROCESS_START_MONDAY": False,
    "WEEKDAY_APPR_PROCESS_START_SATURDAY": False,
    "WEEKDAY_APPR_PROCESS_START_SUNDAY": False,
    "WEEKDAY_APPR_PROCESS_START_THURSDAY": False,
    "WEEKDAY_APPR_PROCESS_START_TUESDAY": True,
    "WEEKDAY_APPR_PROCESS_START_WEDNESDAY": False,
    "NAME_HOUSING_TYPE_House_apartment": True,
    "NAME_HOUSING_TYPE_Municipal_apartment": False,
    "NAME_HOUSING_TYPE_Office_apartment": False,
    "NAME_HOUSING_TYPE_Rented_apartment": False,
    "NAME_HOUSING_TYPE_With_parents": False,
    "NAME_FAMILY_STATUS_Married": True,
    "NAME_FAMILY_STATUS_Separated": False,
    "NAME_FAMILY_STATUS_Single_not_married": False,
    "NAME_FAMILY_STATUS_Widow": False,
    "NAME_INCOME_TYPE_Employ_": True, 
    "NAME_INCOME_TYPE_sans_emploi": False,
    "FLAG_OWN_CAR_Y": False,
    "CODE_GENDER_M": True,
    "NAME_CONTRACT_TYPE_Revolving_loans": False,
    "FLAG_OWN_REALTY_Y": True,
    "OCCUPATION_TYPE_Cleaning_staff": False,
    "OCCUPATION_TYPE_Cooking_staff": False,
    "OCCUPATION_TYPE_Core_staff": False,
    "OCCUPATION_TYPE_Drivers": False,
    "OCCUPATION_TYPE_HR_staff": False,
    "OCCUPATION_TYPE_High_skill_tech_staff": False,
    "OCCUPATION_TYPE_IT_staff": False,
    "OCCUPATION_TYPE_Laborers": True,
    "OCCUPATION_TYPE_Low_skill_Laborers": False,
    "OCCUPATION_TYPE_Managers": False,
    "OCCUPATION_TYPE_Medicine_staff": False,
    "OCCUPATION_TYPE_Private_service_staff": False,
    "OCCUPATION_TYPE_Realty_agents": False,
    "OCCUPATION_TYPE_Sales_staff": True,
    "OCCUPATION_TYPE_Secretaries": False,
    "OCCUPATION_TYPE_Security_staff": False,
    "OCCUPATION_TYPE_Waiters_barmen_staff": False,
    "EMERGENCYSTATE_MODE_Yes": False,
    "NAME_TYPE_SUITE_Family": False,
    "NAME_TYPE_SUITE_Group_of_people": False,
    "NAME_TYPE_SUITE_Other_A": False,
    "NAME_TYPE_SUITE_Other_B": False,
    "NAME_TYPE_SUITE_Spouse_partner": True,
    "NAME_TYPE_SUITE_Unaccompanied": True
}

# Envoi de la requête POST
response = requests.post(f"{url_base}/predire", json=donnees_predire)

# Résultat propre
if response.status_code == 200:
    resultat = response.json()
    print("Prédiction :", resultat["prediction"])
    print("Probabilité :", resultat["probabilite_pret"])
    print("decision :", resultat["decision"])
else:
    print("Erreur:", response.status_code, response.text)

