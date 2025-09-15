import os 
import zipfile
import pandas as pd

source_folder = r'C:\Rajat_errsaij\Raw'
destination_folder = r'C:\Rajat_errsaij\input_extracted_file'

os.makedirs(destination_folder, exist_ok=True)

for file_name in os.listdir(source_folder):
    if file_name.endswith('.zip'):
        zip_path = os.path.join(source_folder, file_name)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            print(f'📦 Checking contents of: {file_name}')
            for file in zip_ref.namelist():
                print(f'  Found: {file}')
                if file.endswith('.csv'):
                    full_path = zip_ref.extract(file, destination_folder)
                    print(f'  ✅ Extracted: {full_path}')

                    try:
                        df = pd.read_csv(full_path, skiprows=8)
                        df.to_csv(full_path, index=False)
                        print(f'  ✂️ Removed first 8 rows from: {file}')
                    except Exception as e:
                        print(f'  ⚠️ Failed to process {file}: {e}')

print("\n✅ All CSV files have been extracted and cleaned (first 8 rows removed).")
