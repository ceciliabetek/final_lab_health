# CODE DESCRIPTION:

# 🏥 Patient Satisfaction Analysis in Healthcare Facilities

## 📌 Project Overview

This project aims to analyze the determinants of patient satisfaction in healthcare facilities using hospital-level data. The objective is to understand how different aspects of care—particularly quality indicators from HCAHPS surveys—impact overall patient satisfaction.

The analysis focuses on identifying key drivers of satisfaction, evaluating hospital performance, and providing data-driven recommendations to improve healthcare quality.

---

## 🎯 Objectives

* Identify key factors influencing patient satisfaction
* Analyze the relationship between quality of care and satisfaction
* Compare satisfaction across hospital types and services
* Build Key Performance Indicators (KPIs) to monitor performance
* Provide actionable insights for healthcare stakeholders

---

## ❓ Research Questions

### Core Questions

* What is the overall level of patient satisfaction across hospitals?
* How does quality of care influence patient satisfaction?
* Do hospitals with emergency services have different satisfaction levels?
* Does hospital type affect patient satisfaction?

### Additional Questions

* Which aspects of care (HCAHPS questions) are most associated with satisfaction?
* What percentage of hospitals achieve high satisfaction (rating ≥ 4)?
* Is there consistency between quality scores and satisfaction ratings?
* Are there hospitals with high quality but low satisfaction?
* How much variation exists in patient satisfaction across hospitals?
* Is there a statistically significant relationship between hospital type and satisfaction?
* Is the difference in satisfaction between emergency and non-emergency hospitals significant?

---

## 📊 Dataset Description

The dataset contains hospital-level patient experience data, including:

* **Hospital overall rating** (1–5 scale)
* **HCAHPS Question** (patient survey questions)
* **HCAHPS Answer Percent** (percentage of positive responses)
* **Hospital Type**
* **Emergency Services**
* **Facility Name**

⚠️ Some variables from the initial project proposal (e.g., age, gender, billing, length of stay) were not available and therefore excluded from the analysis.

---

## 🧹 Data Preparation

Data cleaning steps included:

* Handling missing values
* Filtering relevant columns
* Converting data types (string → numeric)
* Removing invalid entries ("Not Available", "Not Applicable")
* Restructuring the dataset (pivoting HCAHPS questions into columns)

This transformation allowed for more accurate analysis of individual care dimensions.

---

## 📈 Key Performance Indicators (KPIs)

The following KPIs were developed:

1. **Average Patient Satisfaction**
2. **Distribution of Satisfaction Ratings**
3. **Average HCAHPS Score by Question**
4. **Satisfaction by Emergency Services**
5. **Satisfaction by Hospital Type**
6. **Key Drivers of Satisfaction (Correlation Analysis)**
7. **Satisfaction Variability (Standard Deviation)**
8. **Quality vs Satisfaction Relationship**
9. **Recommendation Rate**
10. **Communication Score (Doctors & Nurses)**
11. **Cleanliness Score**
12. **Responsiveness Score**
13. **Pain Management Score**
14. **Medication Explanation Score**
15. **Quietness Score**
16. **Composite Experience Score**
17. **Satisfaction Gap (Quality vs Perception)**
18. **Top vs Bottom Hospitals Comparison**

---

## 📊 Data Visualization

Different types of visualizations were used depending on the data:

* **Bar charts** → distribution of ratings, grouped comparisons
* **Histograms** → distribution of continuous variables
* **Grouped bar plots** → comparison across categories
* **Correlation plots** → identifying drivers of satisfaction
* **KPI comparison charts** → overview of patient experience dimensions

⚠️ Boxplots were avoided for discrete variables (e.g., ratings), following best practices.

---

## 🔍 Key Findings

* The average patient satisfaction is moderate (~3.0), indicating room for improvement.
* There is **no strong correlation** between overall quality scores and satisfaction.
* Hospitals with emergency services tend to have slightly lower satisfaction levels.
* Critical Access Hospitals generally perform better than Acute Care Hospitals.
* Communication, cleanliness, and responsiveness are key drivers of satisfaction.
* A significant **gap exists between measured quality and perceived satisfaction**.
* There is noticeable variability across hospitals, indicating inconsistent performance.

---

## 🧪 Statistical Analysis

The following tests were conducted:

* **T-test** → Emergency vs Non-Emergency hospitals
* **Chi-square test** → Hospital type vs satisfaction
* **Correlation analysis** → Quality vs satisfaction

Results show statistically significant differences in several cases, although practical impact may vary.

---

## 📊 Dashboard (Tableau)

A Tableau dashboard was created to visualize:

* Key KPIs (top panel)
* Distribution of satisfaction ratings
* Drivers of satisfaction
* Emergency services comparison
* Hospital type comparison
* Quality vs satisfaction relationship

Interactive filters allow exploration by hospital characteristics.

---

## ⚠️ Limitations

* Lack of demographic and financial variables
* Potential imbalance in group sizes
* Survey-based data may include subjective bias
* Some KPIs depend on correct filtering of survey responses

---

## 💡 Recommendations

* Improve communication between healthcare staff and patients
* Focus on responsiveness and patient support
* Address gaps between perceived and measured quality
* Standardize practices across hospitals to reduce variability
* Use patient feedback to guide operational improvements

---

## 👥 Stakeholders

This analysis benefits:

* Hospitals and healthcare providers
* Healthcare staff
* Policy makers
* Insurance companies

---

## 🛠️ Tools Used

* Python (Pandas, Matplotlib, Seaborn)
* Jupyter Notebook
* Tableau

---

## 📌 Conclusion

This project highlights that patient satisfaction is influenced by multiple factors beyond measurable quality indicators. While hospitals may perform well on specific aspects of care, overall patient perception depends on a broader experience.

Improving patient-centered care requires addressing both clinical quality and emotional, organizational, and communication-related factors.

---
