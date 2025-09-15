import pandas as pd
import os
import difflib
import sys
import re

# === 1. Define base paths ===
base_dir = r"C:\Rajat_errsaij\final_output"
input_files = [
    os.path.join(base_dir, 'aggregated_summary_1.csv'),
    os.path.join(base_dir, 'aggregated_summary_2.csv'),
    os.path.join(base_dir, 'aggregated_summary_3.csv'),
    os.path.join(base_dir, 'aggregated_summary_4.csv'),
    os.path.join(base_dir, 'aggregated_summary_5.csv'),
    os.path.join(base_dir, 'aggregated_summary_6.csv'),
    os.path.join(base_dir, 'aggregated_summary_7.csv')
]
output_path = os.path.join(base_dir, 'Cisco_TXN_final.csv')
logical_column = "Interface Description"

# === 2. Merge input CSVs ===
df_list = []
for file_path in input_files:
    if os.path.isfile(file_path):
        df_list.append(pd.read_csv(file_path))
    else:
        raise FileNotFoundError(f"❌ Input file not found: {file_path}")

merged_df = pd.concat(df_list, ignore_index=True)
merged_df.to_csv(output_path, index=False)
print(f"✅ Merged summary saved to: {output_path}")

# === 3. Read merged file with all columns as strings ===
try:
    df = pd.read_csv(output_path, dtype=str, low_memory=False)
except Exception as e:
    print(f"❌ Error reading merged file: {e}", file=sys.stderr)
    sys.exit(1)

# === 4. Clean column names and find the best match for the target column ===
df.columns = df.columns.str.strip()
matches = difflib.get_close_matches(logical_column, df.columns, n=1, cutoff=0.6)
if not matches:
    print(f"❌ Column '{logical_column}' not found. Available columns:\n  {df.columns.tolist()}", file=sys.stderr)
    sys.exit(1)

column_name = matches[0]
print(f"🛠  Cleaning column: '{column_name}'")
df[column_name] = df[column_name].str.strip('*#')

# === 5. Add VLAN Status column ===
if "Interface Name" in df.columns:
    df["VLAN Status"] = df["Interface Name"].apply(
        lambda x: "VLAN" if pd.notna(x) and re.search(r"\.\d+$", x.strip()) else "NON VLAN"
    )
    print("✅ 'VLAN Status' column added based on 'Interface Name'")
else:
    print("❌ 'Interface Name' column not found for VLAN Status determination.", file=sys.stderr)
    sys.exit(1)

# === 5.5 Remove rows where all five traffic/utilization columns are 0 ===
zero_columns = [
    "Speed(MB)",
    "In Traffic bps",
    "In Utilization (%)",
    "Out Traffic bps",
    "Out Utilization (%)"
]

missing_cols = [col for col in zero_columns if col not in df.columns]
if missing_cols:
    print(f"❌ Required columns not found for filtering: {missing_cols}", file=sys.stderr)
    sys.exit(1)

# Convert to numeric for filtering
for col in zero_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

initial_count = len(df)
df = df[~((df[zero_columns] == 0).all(axis=1))]
removed_count = initial_count - len(df)
print(f"🧹 Removed {removed_count} rows where all traffic/utilization columns were zero.")

# === 6. Overwrite the merged file with cleaned and updated content ===
try:
    df.to_csv(output_path, index=False)
    print(f"✅ Final output saved to:\n  {output_path}")
except Exception as e:
    print(f"❌ Error writing cleaned file: {e}", file=sys.stderr)
    sys.exit(1)
