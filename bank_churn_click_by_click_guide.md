# Bank Customer Churn Project — Click-by-Click Guide

This guide is tailored to your uploaded project brief and dataset.

## 1) What your project is asking you to deliver

Your project brief requires four big outputs:
1. A predictive churn model
2. Churn probability / risk scoring
3. Explainable churn drivers
4. A Streamlit dashboard

The uploaded brief explicitly asks for a predictive model, churn probability scores, explainability, and a Streamlit web app. fileciteturn0file0

## 2) What I found in your CSV

- Rows: 10,000
- Columns: 14
- Missing values: none
- Target column: `Exited`
- Class balance: about **20.4% churn** and **79.6% retained**
- `Year` is constant (`2025`) for all rows, so remove it
- `CustomerId` and `Surname` should also be removed because they are not useful for prediction

## 3) Best workflow to complete the project

Use this order:
1. Setup Python environment
2. Run EDA
3. Do preprocessing + feature engineering
4. Train multiple models
5. Compare model metrics
6. Save best model
7. Build Streamlit dashboard
8. Write report and executive summary

---

## 4) Step-by-step setup in VS Code

### Step 1 — Create a project folder
- On your desktop, create a folder named `Bank_Churn_Project`

### Step 2 — Copy files into that folder
Put these files inside that folder:
- `European_Bank.csv`
- `train_churn_model.py`
- `app.py`
- `requirements.txt`

### Step 3 — Open the folder in VS Code
- Open **VS Code**
- Click **File** → **Open Folder**
- Select `Bank_Churn_Project`
- Click **Select Folder**

### Step 4 — Open terminal in VS Code
- Click **Terminal** → **New Terminal**

### Step 5 — Create virtual environment
In terminal, run:

```bash
python -m venv venv
```

### Step 6 — Activate environment
If you are on Windows PowerShell:

```bash
venv\Scripts\Activate.ps1
```

If you are on Windows Command Prompt:

```bash
venv\Scripts\activate
```

### Step 7 — Install packages

```bash
pip install -r requirements.txt
```

---

## 5) Train the model

### Step 8 — Run training script
In the same terminal, run:

```bash
python train_churn_model.py
```

### Step 9 — Check output files
After the script runs, you should see an `outputs` folder with:
- `bank_churn_model.joblib`
- `model_metrics.csv`
- `feature_importance.csv`
- `metadata.json`

### Step 10 — Which model to present
Use this story in your report:
- **Logistic Regression** = baseline and interpretable benchmark
- **Decision Tree** = easy to explain visually
- **Random Forest** = good business choice because it catches more churners
- **Gradient Boosting** = strongest ROC-AUC in testing

A practical final choice is:
- **Random Forest** if you want stronger churn detection / recall
- **Gradient Boosting** if you want strongest ranking power / ROC-AUC

---

## 6) What to write in your EDA section

Create charts for:
- churn count
- churn by geography
- churn by gender
- churn by active membership
- churn by number of products
- churn by age group
- churn by balance distribution

### Important data observations you can mention
- Germany has the highest churn rate in this dataset
- Inactive members churn much more than active members
- Age is a very strong churn signal
- Customers with 2 products have much lower churn than customers with 1, 3, or 4 products
- `HasCrCard` is much weaker than active membership and product usage

---

## 7) Feature engineering to mention in report

You should mention these created features because your brief asks for them: fileciteturn0file0
- `BalanceSalaryRatio`
- `ProductDensity`
- `EngagementProductInteraction`
- `AgeTenureInteraction`
- `TenureByAge`

Why they matter:
- They capture customer relationship strength
- They improve predictive power beyond raw demographics
- They support business-focused interpretation

---

## 8) Metrics to show in the report

Your brief specifically highlights these evaluation metrics: accuracy, precision, recall, F1-score, and ROC-AUC. fileciteturn0file0

In your report, add a comparison table like this:
- Model name
- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC

### How to explain them simply
- **Accuracy**: overall correctness
- **Precision**: among predicted churners, how many truly churned
- **Recall**: among true churners, how many the model found
- **F1-score**: balance between precision and recall
- **ROC-AUC**: ability to separate churners from non-churners

---

## 9) Build the Streamlit app

### Step 11 — Run the dashboard
In terminal, run:

```bash
streamlit run app.py
```

### Step 12 — What your dashboard will show
The app includes:
- customer churn risk calculator
- churn probability chart
- feature importance dashboard
- what-if scenario simulator

These items match the Streamlit requirements in your brief. fileciteturn0file0

### Step 13 — What to test in the app
Try these scenarios:
- switch customer from inactive to active
- change number of products from 1 to 2
- increase age and check risk change
- compare Germany vs France or Spain

---

## 10) How to structure your final report

Use this section order:

### 1. Title
Predictive Modeling and Risk Scoring for Bank Customer Churn

### 2. Background
Explain why churn matters for CLV, revenue stability, and retention strategy. fileciteturn0file0

### 3. Problem Statement
Summarize that banks often lack accurate prediction, risk scores, and explainability. fileciteturn0file0

### 4. Objectives
Primary:
- predict churn
- assign risk scores
- identify churn drivers

Secondary:
- reduce false positives
- improve interpretability
- enable scenario analysis

### 5. Dataset Description
Describe each field briefly.

### 6. Data Preprocessing
Mention:
- removed `CustomerId`, `Surname`, `Year`
- one-hot encoded `Geography` and `Gender`
- scaled numeric variables
- stratified train-test split

### 7. Feature Engineering
Explain the derived features and why they help.

### 8. Exploratory Data Analysis
Insert charts and insights.

### 9. Model Building
Explain all 4 models.

### 10. Model Evaluation
Show metric comparison table and justify final model.

### 11. Explainability
Add feature importance chart.
Optional: add SHAP summary plot.

### 12. Business Recommendations
Examples:
- focus retention on older inactive customers
- prioritize Germany segment
- encourage cross-sell from 1 product to 2 products carefully
- use proactive offers for high-risk customers

### 13. Conclusion
Write that the project shifts churn analysis from reactive reporting to proactive customer retention.

---

## 11) Executive summary for stakeholder submission

Keep it very simple:
- the model predicts who is likely to leave
- each customer receives a churn probability score
- the dashboard supports faster retention decisions
- the most important drivers are age, product usage, active status, balance, and geography
- the solution helps target retention efforts instead of using broad campaigns

---

## 12) What to say if your teacher/interviewer asks “Why did you choose this model?”

Use this answer:

> I started with Logistic Regression as a baseline because it is easy to interpret. Then I tested Decision Tree, Random Forest, and Gradient Boosting to improve predictive performance. I selected the final model by comparing recall, F1-score, and ROC-AUC because churn prediction is a class-imbalanced problem and accuracy alone would be misleading.

---

## 13) Final submission checklist

Before submitting, make sure you have:
- research paper / report
- EDA charts
- model comparison table
- final trained model
- feature importance output
- Streamlit dashboard working
- executive summary
- recommendations section

---

## 14) Strong final project title for your PPT or report

**Predictive Modeling and Risk Scoring for Bank Customer Churn Using Machine Learning and Explainable Analytics**
