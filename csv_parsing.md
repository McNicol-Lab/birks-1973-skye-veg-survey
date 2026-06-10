You are extracting data from scanned ecological vegetation tables, not herbarium specimen labels.

The image contains a structured phytosociological vegetation table from a flora/vegetation publication. Do NOT extract fields such as collector, date, coordinates, specimen location, or species_name as a single record. Instead, reconstruct the table as tabular data.

Your task is to extract all visible table content into CSV format.

IMPORTANT OUTPUT RULES:
1. Return ONLY valid CSV text.
2. Do not include explanations, markdown, code fences, JSON, or comments.
3. Preserve the table structure.
4. The first column must contain row labels such as Class, Order, Alliance, Association, Reference Number, Map Reference, Altitude, species names, etc.
5. The next columns must represent relevé / plot columns 1–7.
6. Include the final summary columns C and D when visible.
7. Use empty cells only when the table has no corresponding value.
8. Preserve dots "." as absence values.
9. Preserve "x" or "✗" presence marks exactly as visible; use "x" if the mark is unclear.
10. Preserve abundance/cover numbers exactly as printed, including decimals.
11. Preserve abbreviated species names exactly as printed, for example "R. heterostichum", "F. tamarisi", "O. tartarea", "P. saxatilis".
12. Preserve asterisks before species names, for example "*Parmelia glabratula".
13. Do not invent missing data.
14. Do not summarize the table.
15. Do not collapse all species into one field.
16. Do not output one row per image. Output one row per table row.

Use this exact CSV header:

row_label,plot_1,plot_2,plot_3,plot_4,plot_5,plot_6,plot_7,C,D

The table has a metadata/header section followed by environmental rows followed by species rows. Extract them all using the same CSV structure.

For multi-line row labels:
- “Reference Number” may span multiple printed lines. Combine the values under the same row label when they belong to the same field.
- If a field has two stacked values per plot, create separate rows with clear labels, for example:
  Reference Number part 1
  Reference Number part 2
  Map Reference part 1
  Map Reference part 2

For the upper classification block, place the classification value in plot_1 and leave the remaining plot columns blank. Example:
Class,EPIPETRETEA LICHENOSA,,,,,,,,
Order,RHIZOCARPETALIA,,,,,,,,
Alliance,Parmelion saxatilis,,,,,,,,
Association,Hedwigia ciliata-Parmelia saxatilis,,,,,,,,

For numbered plot heading rows, use:
row_label,plot_1,plot_2,plot_3,plot_4,plot_5,plot_6,plot_7,C,D
Plot number,1,2,3,4,5,6,7,,

For environmental rows, extract rows such as:
Reference Number
Map Reference
Altitude (feet)
Aspect (degrees)
Slope (degrees)
Cover (per cent)
Plot area (square metres)

For species rows, the row_label must be the taxon name exactly as printed, and the plot columns must contain the values shown beneath plots 1–7, followed by C and D where visible.

At the bottom, include:
Total number of species (38)

Also extract footnotes or locality text as extra rows after the main table, using row_label values such as:
Footnote
Additional species in list 2
Additional species in list 3
Additional species in list 4
Additional species in list 5
Additional species in list 6
Localities

When extracting scientific names:
- Be careful with common OCR confusions:
  - Parmelia, not Parmedia unless clearly printed otherwise.
  - Rhizocarpetalia, not PHIZOARPETALIA.
  - Hedwigia ciliata, not Hedrigia ciliata.
  - Dicranum scoparium, not seoparium, if the printed word matches scoparium.
  - Scapania gracilis, not Soopania gracilis, if the printed word matches Scapania.
- However, do not over-correct uncertain names. Preserve the visible text when unsure.

Quality check before final output:
- The CSV should have many rows, not just 1 row per image.
- The species section should include all visible taxa.
- Columns must align with plots 1–7 plus C and D.
- The row “Total number of species (38)” should have values under plots 1–7.
- No JSON fields such as raw_response, parse_status, collector, coordinates, or notes should appear.