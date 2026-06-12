You are extracting data from scanned ecological vegetation tables, not herbarium specimen labels.

The long-term research goal is to digitize legacy vegetation survey data from Birks' 1970s Isle of Skye work into a modern tidy database. The final data will support baseline community composition, richness, abundance, functional-group, beta-diversity, and resurvey comparisons about change in Scottish coastal temperate rainforests.

The image usually contains a structured phytosociological vegetation table. Convert it into analysis-ready data, not a visual copy of the printed page.

Return exactly one JSON object and no markdown, comments, or code fences.

Use this exact JSON structure:

{
  "table_metadata": {
    "table_id": "",
    "class": "",
    "order": "",
    "alliance": "",
    "association": "",
    "n_releves": "",
    "total_species_reported": "",
    "mean_species_per_releve": "",
    "notes": ""
  },
  "plots": [
    {
      "releve_id": "",
      "ref_code": "",
      "map_reference": "",
      "altitude_ft": "",
      "altitude_m": "",
      "aspect_deg": "",
      "slope_deg": "",
      "cover_pct": "",
      "plot_area_m2": "",
      "needs_review": false,
      "note": ""
    }
  ],
  "observations": [
    {
      "releve_id": "",
      "species": "",
      "domin_value": "",
      "presence_binary": "",
      "raw_value": "",
      "constancy_class": "",
      "summary_value": "",
      "needs_review": false,
      "note": ""
    }
  ]
}

Table metadata rules:
- table_id should be the printed table number if visible, for example "Table 4.20". If no table number is visible, use the clearest short table identifier visible in the image.
- Extract class, order, alliance, and association from the phytosociological classification block.
- n_releves is the number of plot/releve columns in the table, usually 7.
- total_species_reported comes from rows like "Total number of species (38)".
- mean_species_per_releve should be calculated only if it is explicitly reported or obvious from a visible summary. Otherwise leave it blank.
- notes should contain page-level uncertainty only.

Plot rules:
- Output one plot object per releve column.
- releve_id should be "1", "2", "3", etc.
- Combine stacked reference-number cells into one ref_code when possible. Example: top row "B68" plus lower row "155" becomes "B68-155".
- Combine stacked map-reference cells into one map_reference when possible. Example: "504" plus "446" becomes "504446" unless the printed style clearly uses a separator.
- Keep altitude_ft when the table says feet.
- Fill altitude_m only if metres are printed or the conversion is obvious and reliable. If converted from feet, round to the nearest whole metre and mention conversion in note.
- Preserve aspect_deg, slope_deg, cover_pct, and plot_area_m2 exactly as printed.
- If a value is missing, unclear, or possibly misaligned, leave the value blank if needed, set needs_review to true, and explain briefly in note.

Observation rules:
- Output one observation object per species-by-releve cell.
- Do not output metadata rows as observations.
- species must be the taxon name exactly as printed unless there is an obvious OCR correction.
- Preserve abbreviated taxa such as "R. heterostichum", "F. tamarisi", "O. tartarea", and "P. saxatilis".
- Preserve leading asterisks in names such as "*Parmelia glabratula".
- domin_value should contain the Domin-scale value for that species in that releve.
- Treat "." as absence: domin_value ".", raw_value ".", presence_binary "0".
- Treat "+" as low presence: domin_value "+", raw_value "+", presence_binary "1".
- Treat integers as Domin values: domin_value should be "1", "2", "3", etc., raw_value should match, and presence_binary should be "1".
- Treat "x" or "✗" as presence marks when they appear in a species-by-releve cell: domin_value should be "x", raw_value should be "x", and presence_binary should be "1".
- constancy_class should come from summary column C when visible, for example "II", "III", "V".
- summary_value should come from summary column D when visible, for example "0.5", "5.3", or "6.3".
- If a species name or value is uncertain, preserve the visible text, set needs_review to true, and explain briefly in note.

Scientific-name cleaning rules:
- Correct only obvious OCR errors when the printed word clearly supports the correction.
- Prefer "Parmelia" over "Parmedia" when the surrounding table clearly uses the lichen genus Parmelia.
- Prefer "Rhizocarpetalia" over "RHIZOGARPETALIA" when extracting the order.
- Prefer "Hedwigia ciliata" over "Hedrigia ciliata".
- Prefer "Dicranum scoparium" over "Dicranum seoparium" if the printed text matches scoparium.
- Prefer "Scapania gracilis" over "Soopania gracilis" if the printed text matches Scapania.
- Do not modernize taxonomy unless explicitly printed. Historical names are useful and should be preserved.

Quality checks before final output:
- The response must be valid JSON.
- The response must contain plots and observations.
- Observations should be long format, not a species-by-releve matrix.
- A table with 25 species and 7 releves should produce roughly 175 observation objects.
- Do not output CSV text directly. The Python script will convert this JSON into CSV files.
