import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).parent
DATASET_DIR = BASE_DIR / "Dataset"
OUTPUT_DIR = BASE_DIR / "Visualizations"
OUTPUT_DIR.mkdir(exist_ok=True)

# Find Excel dataset
files = list(DATASET_DIR.glob("*.xlsx"))

if not files:
    raise FileNotFoundError(
        "Excel file Dataset folder mein nahi mili."
    )

file_path = files[0]
df = pd.read_excel(file_path)

print("DATASET LOADED SUCCESSFULLY")
print("File:", file_path.name)

print("\nFIRST 5 ROWS")
print(df.head())

print("\nDATASET SHAPE")
print(df.shape)

print("\nCOLUMN NAMES")
print(df.columns.tolist())

print("\nDATA TYPES")
print(df.dtypes)

print("\nMISSING VALUES")
print(df.isnull().sum())

print("\nDUPLICATE ROWS")
print(df.duplicated().sum())

print("\nDESCRIPTIVE STATISTICS")
print(df.describe(include="all"))

# Save a cleaned copy without exact duplicate rows
clean_df = df.drop_duplicates().copy()
clean_df.to_csv(OUTPUT_DIR / "cleaned_retail_sales.csv", index=False)

print("\nCLEANED DATASET SAVED")
print("Rows before cleaning:", len(df))
print("Rows after removing duplicates:", len(clean_df))

# Identify numeric columns
numeric_cols = clean_df.select_dtypes(include="number").columns.tolist()

# Chart 1: Missing values
plt.figure(figsize=(10, 5))
clean_df.isnull().sum().plot(kind="bar")
plt.title("Missing Values by Column")
plt.xlabel("Column")
plt.ylabel("Missing Value Count")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "01_missing_values.png")
plt.close()

# Chart 2: Numeric distributions
if numeric_cols:
    clean_df[numeric_cols[0]].dropna().plot(kind="hist", bins=15)
    plt.title(f"Distribution of {numeric_cols[0]}")
    plt.xlabel(numeric_cols[0])
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "02_numeric_distribution.png")
    plt.close()

# Chart 3: Correlation heatmap
if len(numeric_cols) >= 2:
    plt.figure(figsize=(8, 6))
    sns.heatmap(clean_df[numeric_cols].corr(), annot=True, cmap="Blues")
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "03_correlation_heatmap.png")
    plt.close()

# Chart 4: First categorical column
categorical_cols = clean_df.select_dtypes(
    include=["object", "category"]
).columns.tolist()

if categorical_cols:
    counts = clean_df[categorical_cols[0]].value_counts().head(10)
    counts.plot(kind="bar")
    plt.title(f"Top Categories by {categorical_cols[0]}")
    plt.xlabel(categorical_cols[0])
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "04_category_counts.png")
    plt.close()

# Chart 5: Outlier check using boxplot
if numeric_cols:
    plt.figure(figsize=(9, 5))
    sns.boxplot(data=clean_df[numeric_cols])
    plt.title("Numeric Columns: Outlier Overview")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "05_outlier_overview.png")
    plt.close()

print("\nEDA COMPLETE")
print("Charts and cleaned data saved in:", OUTPUT_DIR)



