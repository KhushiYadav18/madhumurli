import os
import json
import requests
from datetime import datetime, timedelta
from tqdm import tqdm

# Define available languages and their respective URL paths
languages = {
    "hi": "hindi",
    "bn": "bengali",
    "as": "assamese",
    "gu": "gujarati",
    "kn": "kannada",
    "ml": "malayalam",
    "mr": "marathi",
    "ne": "nepali",
    "or": "odia",
    "pa": "punjabi",
    "si": "sinhala",
    "te": "telugu",
    "ta_my": "tamil_chennai",
    "ta": "tamil_srilanka"
}

# Define the base URL pattern
base_url = "https://madhubanmurli.org/murlis/{lang}/pdf/murli-{year}-{month:02d}-{day:02d}.pdf"

# Set the date range
start_date = datetime(2017, 1, 1)
end_date = datetime(2025, 3, 26)

# Create a main directory to store PDFs
main_dir = "madhubanmurli_pdfs"
os.makedirs(main_dir, exist_ok=True)

# Metadata file path
metadata_file = os.path.join(main_dir, "metadata.json")

# Load existing metadata if available
if os.path.exists(metadata_file):
    with open(metadata_file, "r", encoding="utf-8") as f:
        metadata = json.load(f)
else:
    metadata = []

total_days = (end_date - start_date).days + 1
total_files = total_days * len(languages)

with tqdm(total=total_files, desc="Downloading PDFs", unit="file") as pbar:
    current_date = start_date
    while current_date <= end_date:
        year, month, day = current_date.year, current_date.month, current_date.day
        
        for lang_code, lang_name in languages.items():
            url = base_url.format(lang=lang_code, year=year, month=month, day=day)
            save_dir = os.path.join(main_dir, lang_name, str(year))
            os.makedirs(save_dir, exist_ok=True)
            pdf_file = os.path.join(save_dir, f"murli-{year}-{month:02d}-{day:02d}.pdf")
            
            try:
                response = requests.get(url, stream=True)
                
                if response.status_code == 200:
                    with open(pdf_file, "wb") as f:
                        for chunk in response.iter_content(chunk_size=1024):
                            f.write(chunk)
                    
                    metadata.append({
                        "date": f"{year}-{month:02d}-{day:02d}",
                        "language": lang_name,
                        "url": url,
                        "path": pdf_file
                    })
                
            except Exception as e:
                print(f"⚠️ Error downloading {url}: {e}")
            
            pbar.update(1)  # Update progress bar

        current_date += timedelta(days=1)

# Save metadata to JSON file
with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=4, ensure_ascii=False)

print(f"📂 Metadata saved: {metadata_file}")
