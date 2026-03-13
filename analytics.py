import pandas as pd

df = pd.read_csv("output/telemetry_with_users.csv")

print(df.head())

df["total_tokens"] = df["input_tokens"].fillna(0) + df["output_tokens"].fillna(0)
df['success_bool'] = df['success'].astype(str).str.lower() == 'true'

#Metric 1: Total token usage per user

tokens_per_user = (
    df.groupby("user_email")["total_tokens"]
    .sum()
    .sort_values(ascending=False)
)

print(tokens_per_user.head())

#Metric 2: Total tokens by engineer level

tokens_by_level = (
    df.groupby("level")["total_tokens"]
    .sum()
    .sort_values(ascending=False)
)

print(tokens_by_level)

#Metric 3: Number of sessions per user

sessions_per_user = (
    df.groupby("user_email")["session_id"]
    .nunique()
    .sort_values(ascending=False)
)

print(sessions_per_user.head())

#Metric 4: Event distribution

events_count = df["event_name"].value_counts()
print(events_count)

#Metric 5: Tool Reliability

tool_results = df[df["event_name"] == "tool_result"].copy()
tool_results["success_bool"] = tool_results["success"].astype(str).str.lower() == "true"

tool_performance = (
    tool_results.groupby("tool_name")["success_bool"]
    .mean()
    .sort_values()
)
print("\nTool Success Rates (Lowest to Highest)")
print(tool_performance)

#Metric 6: ROI by Engineering Practice

practice_roi = df.groupby('practice').agg({
    'cost_usd': 'sum',
    'success_bool': lambda x: x[df.loc[x.index, 'event_name'] == 'tool_result'].sum()
}).rename(columns={'success_bool': 'successful_tools'})
practice_roi['cost_per_success'] = practice_roi['cost_usd'] / practice_roi['successful_tools']

#Metric 7: Efficiency by Engineering Level
level_efficiency = df.groupby('level').agg({
    'cost_usd': 'sum',
    'success_bool': lambda x: x[df.loc[x.index, 'event_name'] == 'tool_result'].sum()
}).rename(columns={'success_bool': 'successful_tools'})
level_efficiency['success_per_dollar'] = level_efficiency['successful_tools'] / level_efficiency['cost_usd']

import numpy as np
from datetime import timedelta


# Metric 8: Temporal Heatmap 
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
df = df.dropna(subset=['timestamp'])
df['hour'] = df['timestamp'].dt.hour
hourly_usage = df.groupby('hour').size()

import numpy as np
from datetime import timedelta


# BONUS: Predictive Analytics (Exponential Smoothing) 
df['date'] = df['timestamp'].dt.date
daily_cost = df.groupby('date')['cost_usd'].sum().reset_index()
daily_cost['date'] = pd.to_datetime(daily_cost['date'])
daily_cost = daily_cost.sort_values('date')

# Exponential Moving Average (EMA) to smooth out the daily spikes
daily_cost['trend'] = daily_cost['cost_usd'].ewm(span=7, adjust=False).mean()

# Calculate the slope/momentum of the last 7 days
recent_trend = daily_cost['trend'].tail(7).values
slope = (recent_trend[-1] - recent_trend[0]) / 7

# Forecast the next 14 days based on that recent momentum
forecast_days = 14
last_date = daily_cost['date'].max()
future_dates = [last_date + timedelta(days=i) for i in range(1, forecast_days + 1)]

# Project the trend line forward
future_trend = [recent_trend[-1] + (slope * i) for i in range(1, forecast_days + 1)]

# Combine into a single dataframe
future_df = pd.DataFrame({
    'date': future_dates,
    'cost_usd': np.nan,  # Future costs are unknown
    'trend': future_trend
})

trend_df = pd.concat([daily_cost, future_df], ignore_index=True)


tokens_per_user.to_csv("output/tokens_per_user.csv")
tokens_by_level.to_csv("output/tokens_by_level.csv")
sessions_per_user.to_csv("output/sessions_per_user.csv")
events_count.to_csv("output/events_distribution.csv")
tool_performance.to_csv("output/tool_performance.csv")
practice_roi.to_csv("output/practice_roi.csv")
level_efficiency.to_csv("output/level_efficiency.csv")
hourly_usage.to_csv("output/hourly_usage.csv")
trend_df.to_csv("output/daily_cost_trend.csv", index=False)