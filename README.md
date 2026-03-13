# Claude Code Analytics Platform

An end-to-end data pipeline, interactive dashboard, and REST API designed to process raw telemetry data from Claude Code sessions and translate it into actionable business insights regarding developer patterns, tool reliability, and financial ROI.

## Architecture Overview

The platform is designed with a modular, sequential data pipeline that processes raw simulated continuous streams into aggregated metrics:

1. **`parse.py` (Ingestion & Cleaning):** Reads raw, nested JSONL log batches (`telemetry_logs.jsonl`) and extracts critical event attributes (tokens, cost, tool successes, prompt lengths) into a flat `cleaned_telemetry.csv`.
2. **`prepare_data.py` (Enrichment):** Joins the cleaned telemetry data with user metadata (`employees.csv`) to map events to specific engineering practices, locations, and seniority levels.
3. **`analytics.py` (Data Science & Aggregation):** The core calculation engine. It extracts deep insights such as:
   - **Practice ROI:** Cost per successful tool execution by department.
   - **Level Efficiency:** Successes per dollar spent by seniority level.
   - **Predictive Analytics (Bonus):** Calculates a 7-day Exponential Moving Average (EMA) and 14-day trajectory to forecast future API costs based on recent momentum.
4. **`dashboard.py` (Visualization):** A Streamlit application providing interactive, stakeholder-specific tabs (Executive Summary, Tool Performance, Developer Patterns, and Predictive Trends) using Plotly.
5. **`api.py` (Programmatic Access - Bonus):** A FastAPI layer providing REST endpoints to access the aggregated metrics programmatically.

## Dependencies

The project relies on standard data science and web frameworks. You can install them using:

```bash
pip install pandas numpy streamlit plotly fastapi uvicorn
```
(Note: Built with Python 3.10+)

## Setup & Execution Instructions

[cite_start]Follow these steps in order to process the data and spin up the interfaces[cite: 31].

### 1. Run the Data Pipeline
Execute the scripts in sequence to build the datasets:
```bash
python3 parse.py
python3 prepare_data.py
python3 analytics.py
```

Verify that the `output/` directory is now populated with aggregated CSVs  
(e.g., `practice_roi.csv`, `daily_cost_trend.csv`).

### 2. Launch the Interactive Dashboard

To view the visualizations and predictive trends:

```bash
python3 -m streamlit run dashboard.py
```

The dashboard will automatically open in your default web browser.

### 3. Launch the API Server

To access the data programmatically via REST endpoints:

```bash
python3 -m uvicorn api:app --reload
```

**Interactive Docs:**  
Navigate to `http://127.0.0.1:8000/docs` or `http://127.0.0.1:8000/redoc`

**Raw Endpoint Example:**  
`http://127.0.0.1:8000/api/v1/metrics/roi`


## LLM Usage Log (AI-First Philosophy)

In alignment with the **AI-First Philosophy**, LLMs were heavily utilized to accelerate development, architect the data transformations, and write boilerplate code.

### AI Tools Used
- **LLM Assistant** (Conversational AI for architectural brainstorming and code generation)

---

### Key Prompts & Iterations

**Prompt:**  
*"I have parsed the basic token counts. How can we make the analysis more interesting and actionable for managers?"*

**Result:**  
The AI suggested shifting from raw volume metrics to **efficiency metrics** (e.g., *Cost per Successful Tool*, *Successes per Dollar by Seniority*), which drove the logic implemented in `analytics.py`.

---

**Prompt:**  
*"I am getting a SettingWithCopy warning and a Division by Zero error when calculating the ROI."*

**Result:**  
The AI provided robust **Pandas error-handling techniques** (`errors='coerce'`, `replace(0, np.nan)`, and safe `.copy()` declarations) to ensure pipeline stability against messy synthetic data.

---

**Prompt:**  
*"How do you do the prediction? Maybe use some academic predictive theories?"*

**Result:**  
Transitioned from a simple rolling average to an **Exponential Moving Average (EMA)** to smooth high-variance simulated daily spikes and project more realistic forward trends.

---

**Prompt:**  
*"Can we also add this: Create API endpoints for programmatic access to the processed data."*

**Result:**  
Generated a **FastAPI implementation** to expose the processed CSV outputs as **RESTful endpoints**.

---

### Validation Process

**Data Verification**  
Printed intermediate DataFrames (`df.head()`) in the terminal to ensure JSON arrays were flattened correctly and joins were accurate.

**Visual QA**  
Validated the predictive regression by confirming that the **Plotly line chart** correctly overlays the historical bar charts.

**Endpoint Testing**  
Manually accessed the `http://127.0.0.1:8000` endpoints in the browser to verify that the JSON payload matched the expected **Pandas dictionary orientation**.
