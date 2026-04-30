import os
import pandas as pd
import streamlit as st
import joblib

st.set_page_config(
    page_title="Bank Customer Churn Dashboard",
    page_icon="🏦",
    layout="wide"
)

MODEL_CANDIDATES = [
    "bank_churn_model.pkl",
    "bank_churn_model.joblib",
]

FEATURE_IMPORTANCE_CANDIDATES = [
    "feature_importance.csv",
    "feature_importance.xlsx",
    "feature_importance.xls",
]


@st.cache_resource
def load_model():
    for file_name in MODEL_CANDIDATES:
        if os.path.exists(file_name):
            return joblib.load(file_name), file_name
    raise FileNotFoundError(
        "Model file not found. Keep one of these in the same folder as app.py: "
        + ", ".join(MODEL_CANDIDATES)
    )


@st.cache_data
def load_feature_importance():
    for file_name in FEATURE_IMPORTANCE_CANDIDATES:
        if os.path.exists(file_name):
            if file_name.endswith(".csv"):
                df = pd.read_csv(file_name)
            else:
                df = pd.read_excel(file_name)

            df.columns = [str(col).strip() for col in df.columns]

            if "Feature" not in df.columns or "Importance" not in df.columns:
                if len(df.columns) >= 2:
                    df = df.iloc[:, :2].copy()
                    df.columns = ["Feature", "Importance"]
                else:
                    raise ValueError(
                        "Feature importance file must contain at least two columns."
                    )

            df["Feature"] = df["Feature"].astype(str)
            df["Importance"] = pd.to_numeric(df["Importance"], errors="coerce")
            df = df.dropna(subset=["Importance"]).sort_values(
                by="Importance", ascending=False
            )
            return df, file_name

    raise FileNotFoundError(
        "Feature importance file not found. Keep one of these in the same folder as app.py: "
        + ", ".join(FEATURE_IMPORTANCE_CANDIDATES)
    )


def get_risk_label(probability: float):
    if probability < 0.30:
        return "Low Risk", "success"
    elif probability < 0.70:
        return "Medium Risk", "warning"
    return "High Risk", "error"


def get_recommendation(probability, is_active, num_products, geography, age):
    if probability < 0.30:
        return "Customer is low risk. No immediate retention action is needed."

    recommendations = []

    if not is_active:
        recommendations.append("Launch an engagement campaign to increase account activity.")

    if num_products <= 1:
        recommendations.append("Offer cross-sell options such as savings, cards, or loan products.")

    if geography == "Germany":
        recommendations.append("Review region-specific retention strategy because churn risk is often higher in Germany.")

    if age >= 50:
        recommendations.append("Provide personalized relationship support for older customers.")

    if not recommendations:
        recommendations.append("Monitor this customer closely and offer a personalized retention incentive.")

    if probability >= 0.70:
        return "High-risk customer. " + " ".join(recommendations)

    return "Medium-risk customer. " + " ".join(recommendations)


def build_input_dataframe(
    credit_score,
    geography,
    gender,
    age,
    tenure,
    balance,
    num_products,
    has_card,
    is_active,
    salary,
):
    balance_salary_ratio = balance / (salary + 1)
    product_density = num_products / (tenure + 1)
    engagement_product_interaction = is_active * num_products
    age_tenure_interaction = age * tenure

    input_df = pd.DataFrame(
        {
            "CreditScore": [credit_score],
            "Geography": [geography],
            "Gender": [gender],
            "Age": [age],
            "Tenure": [tenure],
            "Balance": [balance],
            "NumOfProducts": [num_products],
            "HasCrCard": [has_card],
            "IsActiveMember": [is_active],
            "EstimatedSalary": [salary],
            "BalanceSalaryRatio": [balance_salary_ratio],
            "ProductDensity": [product_density],
            "EngagementProductInteraction": [engagement_product_interaction],
            "AgeTenureInteraction": [age_tenure_interaction],
        }
    )

    return input_df


# -----------------------
# Load files
# -----------------------
try:
    model, model_file_used = load_model()
except Exception as e:
    st.error(f"Unable to load model: {e}")
    st.stop()

try:
    feature_importance, feature_file_used = load_feature_importance()
except Exception as e:
    st.error(f"Unable to load feature importance file: {e}")
    st.stop()


# -----------------------
# Sidebar inputs
# -----------------------
st.sidebar.header("Customer Input")

credit_score = st.sidebar.slider("Credit Score", 300, 900, 650)
geography = st.sidebar.selectbox("Geography", ["France", "Germany", "Spain"])
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
age = st.sidebar.slider("Age", 18, 92, 35)
tenure = st.sidebar.slider("Tenure", 0, 10, 5)
balance = st.sidebar.number_input("Balance", min_value=0.0, max_value=300000.0, value=50000.0, step=1000.0)
num_products = st.sidebar.slider("Number of Products", 1, 4, 2)
has_card = st.sidebar.selectbox("Has Credit Card", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
is_active = st.sidebar.selectbox("Is Active Member", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
salary = st.sidebar.number_input("Estimated Salary", min_value=0.0, max_value=300000.0, value=70000.0, step=1000.0)

input_df = build_input_dataframe(
    credit_score=credit_score,
    geography=geography,
    gender=gender,
    age=age,
    tenure=tenure,
    balance=balance,
    num_products=num_products,
    has_card=has_card,
    is_active=is_active,
    salary=salary,
)

# -----------------------
# Prediction
# -----------------------
try:
    prediction = int(model.predict(input_df)[0])

    if hasattr(model, "predict_proba"):
        probability = float(model.predict_proba(input_df)[0][1])
    else:
        probability = float(prediction)
except Exception as e:
    st.error(f"Prediction failed: {e}")
    st.stop()

risk_label, risk_message_type = get_risk_label(probability)
predicted_class = "Churn" if prediction == 1 else "Retain"
recommendation = get_recommendation(
    probability=probability,
    is_active=is_active,
    num_products=num_products,
    geography=geography,
    age=age,
)

# -----------------------
# Main app
# -----------------------
st.title("Predictive Modeling and Risk Scoring for Bank Customer Churn")
st.caption("Interactive dashboard for churn prediction, risk scoring, and explainability.")

st.subheader("Customer Input Data")
st.dataframe(input_df, hide_index=True, use_container_width=True)

metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("Churn Probability", f"{probability:.2%}")
metric_col2.metric("Predicted Class", predicted_class)
metric_col3.metric("Risk Category", risk_label)

st.progress(float(probability))

st.subheader("Prediction Summary")
if risk_message_type == "success":
    st.success(f"{risk_label}: The customer is unlikely to churn.")
elif risk_message_type == "warning":
    st.warning(f"{risk_label}: The customer needs monitoring and possible engagement action.")
else:
    st.error(f"{risk_label}: Immediate retention action is recommended.")

st.subheader("Recommendation")
if probability < 0.30:
    st.success(recommendation)
elif probability < 0.70:
    st.warning(recommendation)
else:
    st.error(recommendation)

st.subheader("Top 5 Important Features")
top5 = feature_importance.head(5).copy()
st.bar_chart(top5.set_index("Feature"), use_container_width=True)

with st.expander("View Full Feature Importance Table"):
    st.dataframe(feature_importance, hide_index=True, use_container_width=True)

st.subheader("What-if Analysis")
st.write("Change the values in the sidebar to observe how the churn probability changes in real time.")

analysis_points = []
if is_active == 0:
    analysis_points.append("Inactive membership increases churn risk.")
if num_products <= 1:
    analysis_points.append("Low product ownership may reduce customer stickiness.")
if geography == "Germany":
    analysis_points.append("Customers in Germany may show relatively higher churn risk patterns.")
if age >= 50:
    analysis_points.append("Older customers may require stronger relationship management.")
if balance > 100000:
    analysis_points.append("High balance customers are important for targeted retention strategy.")

if analysis_points:
    for point in analysis_points:
        st.info(point)
else:
    st.info("This customer profile does not currently show additional warning signals beyond the calculated risk score.")

st.markdown("---")
st.caption(
    f"Loaded model: {model_file_used} | Loaded feature importance: {feature_file_used}"
)
st.caption("Developed for bank customer churn prediction using Machine Learning and Streamlit.")
