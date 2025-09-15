import pandas as pd
import glob
import os

# 1. Read and merge all CSV files in the input directory
data_folder = r"C:\Rajat_errsaij\input_extracted_file"
all_files = glob.glob(os.path.join(data_folder, "*.csv"))

# Read and concatenate
df_list = []
for f in all_files:
    df_list.append(pd.read_csv(f, low_memory=False))

merged_df = pd.concat(df_list, ignore_index=True)

# 2. Select only the required columns
cols = [
    'Device Name', 'IP Address', 'Interface Name', 'Time',
    'In Traffic bps', 'In Utilization (%)',
    'Out Traffic bps', 'Out Utilization (%)', 'Interface Description'
]
merged_df = merged_df[cols]

# 3. Create "Resource Name" by concatenating Interface Name and IP Address
merged_df['Resource Name'] = (
    merged_df['Interface Name'].astype(str) + '/' + merged_df['IP Address'].astype(str)
)

# Reorder columns if desired
merged_df = merged_df[
    ['Resource Name'] + cols
]

# 4. Load the lookup CSV and pull "Speed(MB)"
lookup_path = r"C:\Rajat_errsaij\Cisco_PM_ChildSite_Nationwide_20250428_060010_648\Cisco_PM_ChildSite_Nationwide_20250428_060010_648.csv"
lookup_df = pd.read_csv(lookup_path, low_memory=False)
lookup_df.rename(columns={'Resource name': 'Resource Name'}, inplace=True)

# Merge with lookup, keep only matching rows
merged_lookup = merged_df.merge(
    lookup_df[['Resource Name', 'Speed(MB)']],
    on='Resource Name',
    how='left'
)

# 5. Drop rows where Speed(MB) is NaN (lookup failed)
cleaned_df = merged_lookup.dropna(subset=['Speed(MB)']).copy()

# 6. Aggregate per Resource Name
aggregated = (
    cleaned_df.groupby('Resource Name', as_index=False)
    .agg({
        'Device Name': 'first',
        'IP Address': 'first',
        'Interface Name': 'first',
        'Time': 'first',
        'Speed(MB)': 'first',
        'In Traffic bps': 'max',
        'In Utilization (%)': 'max',
        'Out Traffic bps': 'max',
        'Out Utilization (%)': 'max',
        'Interface Description': 'first'
    })
)

# 7. Save results
output_dir = r"C:\Rajat_errsaij\output"
os.makedirs(output_dir, exist_ok=True)

cleaned_df.to_csv(os.path.join(output_dir, 'merged_with_speed.csv'), index=False)
aggregated.to_csv(os.path.join(output_dir, 'aggregated_summary.csv'), index=False)

print("Merged file saved to 'merged_with_speed.csv'.")
print("Aggregated summary saved to 'aggregated_summary.csv'.")
