# Birks 1973 Vegetation Surveys – Chapter 4 Data Extraction

**Project**: Digitization, extraction, cleaning, and preliminary analysis of vegetation survey tables from H.J.B. Birks’ 1973 PhD thesis (Chapter 4), Isle of Skye, Scotland.

**Repository maintainers**: Gavin McNicol (PI)  
**Contributors**: [Student 1 Name], [Student 2 Name] (UIC CS)  
**Timeline**: June 1 – July 10, 2025

---

## Project Goal

Extract, clean, and harmonize vegetation survey data from Birks (1973) Chapter 4 tables to produce tidy, analysis-ready CSV files and perform preliminary clustering of survey sites. This dataset will support paleoecological research on Holocene vegetation patterns on Skye.

## Data Source

Scanned tables from H.J.B. Birks’ 1973 PhD thesis (Chapter 4).  
**Digitized images**: Available in the shared Google Drive folder:  
https://drive.google.com/drive/folders/18Zxvjh24F09ZtroSKzTkWnSDtKWyZoEm?usp=sharing

## Workflow

1. **Data Extraction** – Convert table images into structured data (CSV or Excel).
2. **Quality Control** – Identify and resolve anomalies (footnotes, symbols, merged cells, etc.).
3. **Data Cleaning** – Standardize species names, site codes, abundance values, and metadata.
4. **Harmonization & Merging** – Combine tables into consistent, tidy data frames.
5. **Export** – Produce clean `.csv` files (e.g., `survey_sites.csv`, `species_composition.csv`, `environmental_variables.csv`).
6. **Preliminary Analysis** – Clustering (e.g., hierarchical, k-means, NMDS) of vegetation survey sites.

## Repository Structure (suggested)

birks-1973-skye-veg/
├── data_raw/              # Original extracted tables (do not edit)
├── data_clean/            # Final tidy CSVs (main output)
├── scripts/
│   ├── 01_extraction/
│   ├── 02_qc/
│   ├── 03_cleaning/
│   ├── 04_harmonization/
│   ├── 05_analysis/
│   └── utils/
├── docs/                  # Notes, data dictionary, codebook
├── outputs/               # Figures, clustering results
├── README.md
└── requirements.txt or environment.yml


## Collaboration Guidelines

- **Do not push directly to `main`** (protected branch).
- **Workflow**:
  1. Fork this repository.
  2. Create a feature branch (`git checkout -b yourname-task-01`).
  3. Work on your scripts and commit regularly.
  4. Open a **Pull Request** to `main` when ready for review.
- Gavin will review PRs, merge changes, and maintain the canonical version.
- You can always clone the main repo to see the latest integrated code.

# Deliverables by July 10

Clean, well-documented .csv files in data_clean/
Reproducible R/Python scripts
Short report/notebook with preliminary clustering results and data dictionary
