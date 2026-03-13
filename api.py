from fastapi import FastAPI, HTTPException
import pandas as pd
import os

app = FastAPI(
    title="Claude Code Telemetry API",
    description="Programmatic access to processed developer insights and telemetry data.",
    version="1.0.0"
)

# Helper function
def load_csv_data(filename):
    filepath = os.path.join("output", filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail=f"Data file {filename} not found. Please run analytics.py first.")
    return pd.read_csv(filepath).to_dict(orient="records")

@app.get("/", tags=["Health"])
def root():
    return {"status": "online", "message": "Welcome to the Claude Code Analytics API."}

@app.get("/api/v1/metrics/roi", tags=["Metrics"])
def get_practice_roi():
    """Returns the Cost per Successful Tool grouped by Engineering Practice."""
    return load_csv_data("practice_roi.csv")

@app.get("/api/v1/metrics/tools", tags=["Metrics"])
def get_tool_performance():
    """Returns the success rate of various Claude Code tools."""
    return load_csv_data("tool_performance.csv")

@app.get("/api/v1/metrics/forecast", tags=["Metrics"])
def get_cost_forecast():
    """Returns the historical daily costs and the 14-day exponential moving average forecast."""
    return load_csv_data("daily_cost_trend.csv")

@app.get("/api/v1/metrics/efficiency", tags=["Metrics"])
def get_level_efficiency():
    """Returns the number of successful tool executions per dollar spent, grouped by seniority level."""
    return load_csv_data("level_efficiency.csv")