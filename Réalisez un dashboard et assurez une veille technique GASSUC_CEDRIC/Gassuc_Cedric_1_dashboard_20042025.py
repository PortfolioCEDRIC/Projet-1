# streamlit_app.py
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

API_URL ="https://api-scoring-415253312919.europe-west9.run.app/predire"

st.title("Dashboard de Scoring Crédit")

@st.cache_data
def charger_clients_fichier(path="clients_comparaison.csv"):
    return pd.read_csv(path)

def collect_input():
    st.sidebar.header("Données du Client")
    input_data = {
        "AMT_INCOME_TOTAL": st.sidebar.number_input("Revenu total", value=100000.0),
        "AMT_CREDIT": st.sidebar.number_input("Montant du crédit", value=200000.0),
        "AMT_ANNUITY": st.sidebar.number_input("Montant de l'annuité", value=15000.0),
        "DAYS_BIRTH": st.sidebar.number_input("Âge (jours négatifs)", value=-12000.0),
        "DAYS_EMPLOYED": st.sidebar.number_input("Jours d'emploi", value=-3000.0),
        "EXT_SOURCE_2": st.sidebar.slider("EXT_SOURCE_2", 0.0, 1.0, 0.5),
        "EXT_SOURCE_3": st.sidebar.slider("EXT_SOURCE_3", 0.0, 1.0, 0.5),
        "NAME_EDUCATION_TYPE": st.sidebar.selectbox("Éducation (encodée)", [0.0, 1.0, 2.0]),
        "souscription_au_pret": st.sidebar.selectbox("Souscription au prêt", [0.0, 1.0]),
        
    }

    input_data["CREDIT_INCOME_PERCENT"] = input_data["AMT_CREDIT"] / (input_data["AMT_INCOME_TOTAL"] + 1e-6)
    input_data["ANNUITY_INCOME_PERCENT"] = input_data["AMT_ANNUITY"] / (input_data["AMT_INCOME_TOTAL"] + 1e-6)
    input_data["CREDIT_TERM"] = input_data["AMT_CREDIT"] / (input_data["AMT_ANNUITY"] + 1e-6)
    input_data["DAYS_EMPLOYED_PERCENT"] = input_data["DAYS_EMPLOYED"] / (input_data["DAYS_BIRTH"] + 1e-6)

    defaults = {
        "FLAG_WORK_PHONE": 1, "FLAG_PHONE": 1, "CNT_FAM_MEMBERS": 2.0,
        "REGION_RATING_CLIENT": 3.0, "REGION_RATING_CLIENT_W_CITY": 3.0,
        "HOUR_APPR_PROCESS_START": 10, "REG_CITY_NOT_LIVE_CITY": 0,
        "LIVE_CITY_NOT_WORK_CITY": 0, "OBS_60_CNT_SOCIAL_CIRCLE": 1.0,
        "DEF_60_CNT_SOCIAL_CIRCLE": 0.0, "DAYS_LAST_PHONE_CHANGE": -500.0,
        "FLAG_DOCUMENT_3": 1, "FLAG_DOCUMENT_6": 0, "FLAG_DOCUMENT_8": 0,
        "AMT_REQ_CREDIT_BUREAU_HOUR": 0.0, "AMT_REQ_CREDIT_BUREAU_DAY": 0.0,
        "AMT_REQ_CREDIT_BUREAU_WEEK": 0.0, "AMT_REQ_CREDIT_BUREAU_MON": 0.0,
        "AMT_REQ_CREDIT_BUREAU_QRT": 0.0, "AMT_REQ_CREDIT_BUREAU_YEAR": 0.0,
        "categorie_enfants": 0.0, "INTERVAL_age_client": 3.0,
        "company_seniority_year": 2.0, "update_ID": 999.0, "Population_Segment": 2.0
    }
    input_data.update(defaults)

    booleens = [
        "NAME_INCOME_TYPE_Employ_", "NAME_INCOME_TYPE_sans_emploi", "FLAG_OWN_CAR_Y",
        "CODE_GENDER_M", "NAME_CONTRACT_TYPE_Revolving_loans", "FLAG_OWN_REALTY_Y",
        "WEEKDAY_APPR_PROCESS_START_MONDAY", "WEEKDAY_APPR_PROCESS_START_SATURDAY",
        "WEEKDAY_APPR_PROCESS_START_SUNDAY", "WEEKDAY_APPR_PROCESS_START_THURSDAY",
        "WEEKDAY_APPR_PROCESS_START_TUESDAY", "WEEKDAY_APPR_PROCESS_START_WEDNESDAY",
        "NAME_HOUSING_TYPE_House_apartment", "NAME_HOUSING_TYPE_Municipal_apartment",
        "NAME_HOUSING_TYPE_Office_apartment", "NAME_HOUSING_TYPE_Rented_apartment",
        "NAME_HOUSING_TYPE_With_parents", "NAME_FAMILY_STATUS_Married",
        "NAME_FAMILY_STATUS_Separated", "NAME_FAMILY_STATUS_Single_not_married",
        "NAME_FAMILY_STATUS_Widow", "OCCUPATION_TYPE_Cleaning_staff",
        "OCCUPATION_TYPE_Cooking_staff", "OCCUPATION_TYPE_Core_staff",
        "OCCUPATION_TYPE_Drivers", "OCCUPATION_TYPE_HR_staff",
        "OCCUPATION_TYPE_High_skill_tech_staff", "OCCUPATION_TYPE_IT_staff",
        "OCCUPATION_TYPE_Laborers", "OCCUPATION_TYPE_Low_skill_Laborers",
        "OCCUPATION_TYPE_Managers", "OCCUPATION_TYPE_Medicine_staff",
        "OCCUPATION_TYPE_Private_service_staff", "OCCUPATION_TYPE_Realty_agents",
        "OCCUPATION_TYPE_Sales_staff", "OCCUPATION_TYPE_Secretaries",
        "OCCUPATION_TYPE_Security_staff", "OCCUPATION_TYPE_Waiters_barmen_staff",
        "EMERGENCYSTATE_MODE_Yes", "NAME_TYPE_SUITE_Family",
        "NAME_TYPE_SUITE_Group_of_people", "NAME_TYPE_SUITE_Other_A",
        "NAME_TYPE_SUITE_Other_B", "NAME_TYPE_SUITE_Spouse_partner",
        "NAME_TYPE_SUITE_Unaccompanied"
    ]
    for b in booleens:
        input_data[b] = False

    return input_data

donnees = collect_input()

# Slider interactif pour le seuil optimal
seuil_optimal = st.sidebar.slider(
    "Seuil de décision (probabilité max pour accepter le prêt)",
    min_value=0.0,
    max_value=1.0,
    value=0.515,
    step=0.005
)

if st.sidebar.button("Lancer la prédiction"):
    response = requests.post(API_URL, json=donnees)
    if response.status_code == 200:
        result = response.json()
        prediction = result["prediction"]
        decision = result["decision"]
        proba = result["probabilite_pret"]

        decision_finale = "✅ Accordé" if proba < seuil_optimal else "❌ Refusé"
        couleur_decision = "#4caf50" if proba < seuil_optimal else "#ff4d4d"
        

        st.markdown(
                f"<h3 style='color:{couleur_decision}; text-align:center;'>Décision (selon seuil {seuil_optimal:.3f}) : {decision_finale}</h3>",
                unsafe_allow_html=True)

        st.metric("Probabilité de non-remboursement", f"{proba * 100:.2f}%")


        if "feature_importance" in result:
            shap_dict = result["feature_importance"]
            df_shap = pd.DataFrame(shap_dict.items(), columns=["Variable", "Valeur SHAP"])
            df_shap["Impact absolu"] = df_shap["Valeur SHAP"].abs()
            df_shap = df_shap.sort_values("Impact absolu", ascending=True)

            st.subheader("Top 10 des variables influentes (SHAP individuel)")
            fig = px.bar(
                df_shap,
                x="Impact absolu",
                y="Variable",
                orientation="h",
                title="Variables ayant le plus influencé cette prédiction",
                labels={"Impact absolu": "Importance (valeur absolue)"}
            )
            st.plotly_chart(fig)

        if "shap_expected_value" in result:
            st.info(f"Valeur SHAP moyenne globale (baseline) : {result['shap_expected_value']:.4f}")

        st.subheader("📊 Comparaison des probabilités de défaut entre clients")

        df_autres = charger_clients_fichier()
        df_client = pd.DataFrame([{
            "ID": 0,
            "label": "Client courant",
            "probabilite": result["probabilite_pret"]
        }])

        df_autres["label"] = "Client " + df_autres["ID"].astype(str)
        if "probabilite" not in df_autres.columns:
            df_autres["probabilite"] = [0.2, 0.4, 0.6, 0.8, 1][:len(df_autres)]  # fallback

        df_compare = pd.concat([df_autres[["label", "probabilite"]], df_client], ignore_index=True)
        df_compare = df_compare.sort_values("probabilite", ascending=False)

        df_compare["color"] = df_compare["label"].apply(lambda x: "#4caf50" if x == "Client courant" else "#1f77b4")

        fig_compare = px.bar(
            df_compare,
            y="label",
            x="probabilite",
            orientation="h",
            text=df_compare["probabilite"].apply(lambda x: f"{x * 100:.1f}%"),
            color="label",
            color_discrete_map={row["label"]: row["color"] for _, row in df_compare.iterrows()},
            title="Probabilité de défaut de paiement par client"
        )

        fig_compare.update_layout(
            xaxis_title="Probabilité de défaut (%)",
            yaxis_title="Client",
            showlegend=False,
            xaxis_range=[0, 1]
        )

        st.plotly_chart(fig_compare)

    else:
        st.error(f"Erreur API : {response.text}")