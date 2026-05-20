import pandas as pd
from pathlib import Path

### Import spreadsheet
Excel_path = Path("Scoping_review_notes_on_papers.xlsx")
assert Excel_path.exists(), Excel_path
df_main = pd.read_excel(Excel_path, sheet_name="Sheet1")

### Don't include rows with no spatial scale i.e. excluded papers 
df_main = df_main.dropna(subset=["Spatial scale"])  

### Spatial scale
### Analyse the finest spatial scale studied in each paper
### Spatial scales defined according to WHO spatial scale definitions
Global_keywords = ["global", "continent"]
Regional_keywords = ["nuts", "health and human service region",
                         "us department of health", "multiple regions", "climate region"]
National_keywords = ["country", "national", "federal unit", "countries"]
Subnational_keywords = ["state", "province", "prefacture", 
                         "county", "counties", "district", "municipality",
                         "region", "city", "cities", "town", "village", "ward",
                         "health zone", "health board", "service point", "primary care",
                         "grid", "cell", "idealised towsn"]

### Take spatial scale entry and classify into finest scale category
def finest_scale(entry):
    text = str(entry).lower()
    def matches(keywords):
        return any(kw in text for kw in keywords)
    if matches(Subnational_keywords):
        return "Sub-national"
    if matches(National_keywords):
        return "National"
    if matches(Regional_keywords):
        return "Regional"
    if matches(Global_keywords):
        return "Global"
    return "Unclassified"

### Apply define spatial scale function to each row of spreadsheet
df_main["spatial_scale_category"] = df_main["Spatial scale"].apply(finest_scale)

spatial_counts = df_main["spatial_scale_category"].value_counts()
print(f"\nSpatial scale distribution (n={len(df_main)}):")
print(spatial_counts.to_string())
