import pandas as pd

# load telemetry data
telemetry = pd.read_csv("output/cleaned_telemetry.csv")

# load employee data
employees = pd.read_csv("output/employees.csv")

# merge datasets
df = telemetry.merge(
    employees,
    left_on="user_email",
    right_on="email",
    how="left"
)

print(df.head())
print(df.columns)

df.to_csv("output/telemetry_with_users.csv", index=False)