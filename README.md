# ☀️ Performance Ratio (PR) Analysis Dashboard

A Streamlit web application built to visualize solar power plant Performance Ratio (PR) data. This project demonstrates data processing and the creation of an interactive dashboard.

## Live Application

The live, interactive dashboard can be accessed here:

➡️ [Link to Live App](https://pr-analysis.streamlit.app/)

## Graph Image 
<img width="1389" height="690" alt="output" src="https://github.com/user-attachments/assets/609b7146-77a2-4528-b430-4fbce14dcfbb" />

## ✨ Core Features

* **Interactive Date Filter**: The key feature is the sidebar filter that allows you to select a custom date range. The entire visualization dynamically updates to display the data for the selected period.
* **Data Visualization**: The main graph plots several key metrics:
    * The daily Performance Ratio (PR).
    * A 30-day moving average to show trends.
    * A target budget PR for performance comparison.
* **Contextual Insights**: Data points are color-coded based on daily solar irradiance (GHI), providing a quick visual reference for how weather conditions impact performance.

## 🛠️ How to Run Locally

1.  **Prerequisites**:
    * Python 3.x
    * A `processed_data.csv` file in the project directory.
    * A `requirements.txt` file.
2.  **Installation**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the App**:
    ```bash
    streamlit run app.py
    ```
