import json
import pandas as pd

rows = []

with open("output/telemetry_logs.jsonl") as f:
    for line in f:
        record = json.loads(line)

        for event in record["logEvents"]:
            message_json = json.loads(event["message"])
            attrs = message_json.get("attributes", {})

            row = {
                "timestamp": attrs.get("event.timestamp"),
                "user_email": attrs.get("user.email"),
                "session_id": attrs.get("session.id"),
                "event_name": attrs.get("event.name"),
                "model": attrs.get("model"),
                "input_tokens": attrs.get("input_tokens"),
                "output_tokens": attrs.get("output_tokens"),
                "cost_usd": attrs.get("cost_usd"),
                "tool_name": attrs.get("tool_name"),
                "duration_ms": attrs.get("duration_ms"),
                "success": attrs.get("success"),
                "prompt_length": attrs.get("prompt_length"),
                "decision": attrs.get("decision")
            }

            rows.append(row)

df = pd.DataFrame(rows)

print(df.head())

df.to_csv("output/cleaned_telemetry.csv", index=False)
print("Saved cleaned telemetry data.")