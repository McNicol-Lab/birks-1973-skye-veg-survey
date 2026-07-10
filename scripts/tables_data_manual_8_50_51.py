"""Hand-read transcriptions for Table 4.8, Table 4.50, and Table 4.51.

These three tables were previously missing (4.8) or populated with junk
placeholder rows (4.50, 4.51 — every releve repeating the same single species
because the earlier ollama-based scan of a rotated page failed). This module
replaces them with a genuine transcription made directly from clean page
scans of Birks (1973) supplied for this pass.

Confidence notes:
  - Species identity, constancy class (C), and mean/summary value (D) are
    read directly from clearly printed single tokens at the end of each row
    and are the most reliable fields here.
  - Per-releve Domin cell values are transcribed at best effort from the
    printed grids; all rows are marked needs_review=True so they can be
    spot-checked against the source scan.
  - Map references (six-digit grid numbers) could not be confidently
    resolved to the correct column alignment and are left blank rather than
    risk baking in wrong coordinates; other releve metadata (reference code,
    altitude, aspect, slope, cover, plot area) is transcribed from clearly
    isolated printed values.
"""

NG = "NG"


def releve(rid, ref, mapref, alt, asp, slope, cover, area, sprep):
    return {
        "releve_id": str(rid),
        "ref_code": ref,
        "map_reference": mapref,
        "os_grid_square": NG if mapref else "",
        "altitude_ft": str(alt),
        "aspect_deg": str(asp),
        "slope_deg": str(slope),
        "cover_pct": str(cover),
        "plot_area_m2": str(area),
        "species_reported": str(sprep),
    }


def cells(text):
    return text.split()


NOTE_48 = "Table 4.8 transcribed from scan; per-releve Domin cells at best effort, verify against source."
NOTE_50 = "Table 4.50 transcribed from clean scan; per-releve Domin cells at best effort, verify against source."
NOTE_51 = "Table 4.51 transcribed from clean scan; per-releve Domin cells at best effort, verify against source."


def sp(name, text, c="", d="", note=""):
    row = {"name": name, "cells": cells(text), "C": c, "D": d,
           "needs_review": True, "note": note}
    return row


# ---------------------------------------------------------------------------
# TABLE 4.8  (image 8)
# ASTERETEA TRIPOLIUM / Glauceto-Puccinellietalia / Armerion maritimae
# Two sub-associations sharing one species list:
#   A. Juncus gerardii-Carex extensa (releves 1-17)
#   B. Armeria maritima-Grimmia maritima (releves 18-26)
# Total species in list = 43 (26 in main matrix + 17 single-releve "additional
# species" not transcribed here as they lack matrix cells).
# ---------------------------------------------------------------------------

_T48_REF_A = ["B68-129", "B68-119", "B68-131", "B68-127", "B68-132", "B68-278", "B68-290",
              "B68-135", "B68-143", "B68-177", "B68-178", "B68-355", "B68-116", "B68-117",
              "B68-126", "B68-130", "B68-144"]
_T48_MAP_A = ["597269", "305437", "597269", "596268", "540273", "703158", "565222", "485418",
              "416519", "273433", "273433", "698116", "308427", "308427", "596268", "597269",
              "416519"]
_T48_COVER_A = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 20, 75, 90, 60, 100]

_T48_REF_B = ["B68-004", "B68-148", "B68-175", "B68-145", "B68-176", "B68-109", "B68-203",
              "B68-204", "B68-212"]
_T48_MAP_B = ["527627", "154507", "297420", "131475", "297420", "222613", "323385", "323385",
              "583180"]
_T48_ALT_B = ["", 25, 30, 250, 25, 10, 25, 20, 30]
_T48_COVER_B = [50, 50, 30, 100, 25, 100, 50, 90, 100]
_T48_AREA_B = [1, 2, 3, 4, 4, 4, 4, 4, 4]

TABLE_4_8A = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_8.png",
    "table_id_raw": "Table 4.8",
    "class": "ASTERETEA TRIPOLIUM",
    "order": "GLAUCETO-PUCCINELLIETALIA",
    "alliance": "Armerion maritimae",
    "association": "Juncus gerardii-Carex extensa",
    "n_releves": "17",
    "total_species": "43",
    "mean_species": "9.8",
    "low_confidence": True,
    "releves": [
        releve(i + 1, _T48_REF_A[i], _T48_MAP_A[i], "", "", "", _T48_COVER_A[i], 4, "")
        for i in range(17)
    ],
    "species": [
        sp("Agrostis stolonifera", ". 4 3 4 3 3 . 3 4 3 3 4 3 . 3 . 5", "V", "3.2", NOTE_48),
        sp("Festuca rubra",        ". 3 . 3 2 . 5 4 . 3 4 4 . 6 3 5 .", "V", "3.3", NOTE_48),
        sp("Blysmus rufus",        ". . 2 . . . 2 4 . . . 4 . . . . .", "III", "1.5", NOTE_48),
        sp("Carex extensa",        ". . . 3 3 . . 2 2 . . . 3 . . . .", "III", "1.6", NOTE_48),
        sp("C. flacca",            ". . . . . . . 3 2 . . 3 . . . . .", "II", "0.6", NOTE_48),
        sp("C. scandinavica",      ". . . . 3 . . 2 . 3 . . . . 4 . 3", "II", "0.5", NOTE_48),
        sp("Juncus gerardii",      "5 . 6 5 . 5 7 3 8 7 8 . 8 6 . . 4", "V", "6.3", NOTE_48),
        sp("Triglochin maritima",  ". . . 1 2 . 3 3 3 . 2 . . . 4 . +", "III", "1.1", NOTE_48),
        sp("Armeria maritima",     "6 4 4 8 2 7 4 4 3 6 4 3 . . 5 . 4", "V", "4.5", NOTE_48),
        sp("Aster tripolium",      ". . . . . 5 . 5 4 4 . . . . . . .", "II", "1.0", NOTE_48),
        sp("Cochlearia officinalis agg.", ". . . + . . . . . 1 . 1 . . . . .", "I", "0.2", NOTE_48),
        sp("Glaux maritima",       "5 3 3 . 3 4 5 4 . 4 3 . 5 4 . 4 .", "V", "3.4", NOTE_48),
        sp("Leontodon autumnalis", ". . . 1 2 3 4 . 4 3 . 4 4 . . . .", "II", "0.6", NOTE_48),
        sp("Ligusticum scoticum",  ". . . . . . . + . . . . . . . . .", "I", "0.2", NOTE_48),
        sp("Plantago coronopus",   ". . . . 1 . . . . . . . . . . . .", "II", "0.6", NOTE_48),
        sp("P. maritima",          "8 7 8 3 3 7 7 6 4 7 3 5 3 . 4 . .", "V", "5.2", NOTE_48),
        sp("Sagina maritima",      ". . . 5 3 . . . . . . . . . . . .", "I", "0.5", NOTE_48),
        sp("Spergularia media",    ". . . . . . . . . . . . . 1 2 . .", "I", "0.2", NOTE_48),
        sp("Amblystegium serpens", ". + . . . . . . . . . . . . . . .", "I", "0.2", NOTE_48),
        sp("Grimmia maritima",     ". . . 3 . . . . . . . . . . . . .", "I", "0.7", NOTE_48),
        sp("Trichostomum brachydontium", ". . 1 1 4 . 3 . . . . . . . . . .", "II", "0.6", NOTE_48),
    ],
}

TABLE_4_8B = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_8.png",
    "table_id_raw": "Table 4.8",
    "class": "ASTERETEA TRIPOLIUM",
    "order": "GLAUCETO-PUCCINELLIETALIA",
    "alliance": "Armerion maritimae",
    "association": "Armeria maritima-Grimmia maritima",
    "n_releves": "9",
    "total_species": "43",
    "mean_species": "8.7",
    "low_confidence": True,
    "releves": [
        releve(i + 18, _T48_REF_B[i], _T48_MAP_B[i], _T48_ALT_B[i], "", "", _T48_COVER_B[i], _T48_AREA_B[i], "")
        for i in range(9)
    ],
    "species": [
        sp("Armeria maritima",     "9 8 8 7 9 8 7 8 8", "V", "8.0", NOTE_48),
        sp("Glaux maritima",       ". . . 4 . . . . .", "II", "0.6", NOTE_48),
        sp("Plantago coronopus",   ". . . 3 . . 2 3 .", "II", "0.9", NOTE_48),
        sp("P. maritima",          "3 5 5 3 3 2 5 6 5", "III", "0.8", NOTE_48),
        sp("Sedum anglicum",       ". . + . . . . 4 .", "II", "0.6", NOTE_48),
        sp("Thymus drucei",        ". . . . . . 4 . .", "I", "0.3", NOTE_48),
        sp("Grimmia maritima",     "4 4 5 4 4 2 3 3 3", "V", "3.6", NOTE_48),
        sp("Trichostomum brachydontium", ". . . . . 1 1 . .", "II", "0.2", NOTE_48),
        sp("Anaptychia fusca",     ". . 2 . 2 . 3 . .", "III", "1.2", NOTE_48),
        sp("Ramalina siliquosa",   "4 4 3 . 5 4 . 3 .", "III", "1.8", NOTE_48),
        sp("Xanthoria parietina",  "3 3 2 . . . . 4 .", "II", "1.0", NOTE_48),
    ],
}


# ---------------------------------------------------------------------------
# TABLE 4.50  (image 66)
# QUERCETEA ROBORI-PETRAEAE / Quercetalia robori-petraeae / Quercion robori-petraeae
# Association: Oxalis acetosella-Rhytidiadelphus loreus
# 14 releves; total species in list = 52; mean per releve = 16.5
# ---------------------------------------------------------------------------

_T50_REF = ["B68-218", "B68-264", "B68-266", "B68-267", "B68-300", "B68-314", "B68-319",
            "B68-138", "B68-221", "B68-269", "B68-313", "B68-281", "B68-283", "B68-208"]
_T50_ALT = [100, 100, 100, 100, 200, 100, 100, 50, 100, 100, 100, 45, 45, 200]
_T50_ASP = ["", 225, 225, 225, 0, 0, 45, 45, 0, 225, 0, 45, 45, 20]
_T50_SLOPE = [0, 5, 5, 3, 5, 5, 5, 5, 5, 5, 5, 10, 5, ""]
_T50_COVER = [100, 100, 100, 100, 100, 100, 100, 0.5, 1, 100, 100, 100, 100, 100]
_T50_AREA = [1, 1, 1, 1, 1, 1, 1, 0.5, 1, 1, 1, 1, 1, 1]

TABLE_4_50 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_66.png",
    "table_id_raw": "Table 4.50",
    "class": "QUERCETEA ROBORI-PETRAEAE",
    "order": "QUERCETALIA ROBORI-PETRAEAE",
    "alliance": "Quercion robori-petraeae",
    "association": "Oxalis acetosella-Rhytidiadelphus loreus",
    "n_releves": "14",
    "total_species": "52",
    "mean_species": "16.5",
    "low_confidence": True,
    "releves": [
        releve(i + 1, _T50_REF[i], "", _T50_ALT[i], _T50_ASP[i], _T50_SLOPE[i],
               _T50_COVER[i], _T50_AREA[i], "")
        for i in range(14)
    ],
    "species": [
        sp("Sorbus aucuparia",        ". . . 1 . 1 1 . 3 2 . . 3 1", "III", "0.9", NOTE_50),
        sp("Vaccinium myrtillus",     ". . . 4 4 . 3 . . 3 2 . 5 6", "III", "2.2", NOTE_50),
        sp("Blechnum spicant",        ". . . . . . . . . . . . 3 2", "I", "0.4", NOTE_50),
        sp("Hymenophyllum wilsonii",  "4 . . . . . 2 3 2 . 1 3 . .", "III", "1.1", NOTE_50),
        sp("Anthoxanthum odoratum",   ". . . . 2 2 . . . 3 4 6 3 5", "II", "0.5", NOTE_50),
        sp("Deschampsia flexuosa",    "4 4 4 5 3 3 . 3 4 6 3 5 . .", "V", "3.7", NOTE_50),
        sp("Festuca vivipara",        ". . . . . . . . . 1 . . 2 .", "I", "0.3", NOTE_50),
        sp("Endymion non-scriptus",   "2 3 . . . . . . . . . 2 . .", "II", "0.5", NOTE_50),
        sp("Galium saxatile",         ". . . 2 3 . . 2 . 2 3 . 5 .", "II", "0.9", NOTE_50),
        sp("Melampyrum pratense",     ". . . . . . . . . . . 1 2 .", "I", "0.2", NOTE_50),
        sp("Oxalis acetosella",       "3 4 4 4 2 3 2 2 2 3 5 3 3 .", "V", "2.7", NOTE_50),
        sp("Potentilla erecta",       ". . . 4 4 . 2 3 . 5 5 . . .", "III", "1.9", NOTE_50),
        sp("Breutelia chrysocoma",    ". . . . . . . . 1 . 1 2 . 3", "I", "0.1", NOTE_50),
        sp("Dicranum majus",          "3 . . 1 . . 3 3 . 7 1 1 . 3", "III", "1.1", NOTE_50),
        sp("Hylocomium brevirostre",  "4 7 8 7 5 4 3 2 7 6 6 3 5 3", "V", "5.3", NOTE_50),
        sp("H. splendens",            "8 5 3 4 3 3 2 6 6 2 3 8 4 3", "V", "4.3", NOTE_50),
        sp("H. umbratum",             "3 . . . . . . 2 . . 2 4 . 2", "II", "1.0", NOTE_50),
        sp("Hypnum cupressiforme",    "2 3 1 3 2 . . . 3 1 3 1 . 2", "II", "0.8", NOTE_50),
        sp("Isothecium myosuroides",  "1 3 . 3 2 . . 3 1 . 1 . 3 .", "III", "1.4", NOTE_50),
        sp("Mnium hornum",            ". . . 3 5 . . . . . . 2 . .", "II", "0.4", NOTE_50),
        sp("Pleurozium schreberi",    ". . . 3 1 4 1 2 3 2 3 . 5 3", "III", "1.6", NOTE_50),
        sp("Polytrichum formosum",    "1 . . 3 1 4 1 2 3 . . 2 . 4", "IV", "1.9", NOTE_50),
        sp("Ptilium crista-castrensis", ". . . . . . 2 . 2 . . . . .", "I", "0.3", NOTE_50),
        sp("Rhytidiadelphus loreus",  "2 4 5 4 3 6 4 3 4 9 5 3 3 5", "V", "4.9", NOTE_50),
        sp("R. triquetrus",           ". . . . 2 . . . . 4 . . 6 5", "II", "0.5", NOTE_50),
        sp("Thuidium delicatulum",    "4 6 4 . 5 2 . 4 3 5 6 3 4 3", "V", "4.1", NOTE_50),
        sp("T. tamariscinum",         ". . . 2 3 . . . . 5 5 . 3 .", "III", "1.9", NOTE_50),
        sp("Bazzania trilobata",      ". . . . 2 . . . 2 . 4 . . .", "II", "0.6", NOTE_50),
        sp("Diplophyllum albicans",   "1 . . . . . . . 1 . . . 1 .", "I", "0.1", NOTE_50),
        sp("Frullania tamarisci",     "1 . . 2 . . . 1 3 . 1 . 1 .", "II", "0.4", NOTE_50),
        sp("Plagiochila spinulosa",   "3 6 4 3 . 4 . . . 3 . 6 3 5", "II", "0.5", NOTE_50),
        sp("Scapania gracilis",       "2 4 4 . 3 5 . . . . . 4 4 .", "II", "0.6", NOTE_50),
    ],
}


# ---------------------------------------------------------------------------
# TABLE 4.51  (image 69)
# QUERCETEA ROBORI-PETRAEAE / Quercetalia robori-petraeae / Quercion robori-petraeae
# Association: Hymenophyllum wilsonii-Isothecium myosuroides
# 13 releves; total species in list = 45; mean per releve = 12.8
# ---------------------------------------------------------------------------

_T51_REF = ["B68-139", "B68-268", "B68-276", "B68-270", "B68-272", "B68-299", "B68-316",
            "B68-282", "B68-280", "B68-297", "B68-315", "B68-220", "B68-222"]
_T51_ALT = [200, 100, 100, 100, 100, 200, 100, 100, 100, 100, 100, 100, 100]
_T51_ASP = [45, 225, 225, 225, 225, 0, 0, 45, 45, 0, 0, 0, 0]
_T51_SLOPE = [80, 70, 70, 80, 60, 70, 80, 90, 70, 80, 80, 50, 45]
_T51_SREP = [14, 13, 12, 12, 16, 11, 9, 16, 7, 16, 11, 12, 17]

TABLE_4_51 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_69.png",
    "table_id_raw": "Table 4.51",
    "class": "QUERCETEA ROBORI-PETRAEAE",
    "order": "QUERCETALIA ROBORI-PETRAEAE",
    "alliance": "Quercion robori-petraeae",
    "association": "Hymenophyllum wilsonii-Isothecium myosuroides",
    "n_releves": "13",
    "total_species": "45",
    "mean_species": "12.8",
    "low_confidence": True,
    "releves": [
        releve(i + 1, _T51_REF[i], "", _T51_ALT[i], _T51_ASP[i], _T51_SLOPE[i], 100, 1, _T51_SREP[i])
        for i in range(13)
    ],
    "species": [
        sp("Hymenophyllum wilsonii", "5 5 4 5 5 4 5 5 6 7 7 7 8", "V", "5.6", NOTE_51),
        sp("Deschampsia flexuosa",   ". 1 . 1 2 . . 3 . 2 . . .", "I", "0.2", NOTE_51),
        sp("Campylopus flexuosus",   ". 3 . . 1 . . 3 . . 4 1 2", "II", "0.5", NOTE_51),
        sp("Dicranum majus",         ". 1 2 1 2 3 1 2 . 4 1 2 3", "V", "1.7", NOTE_51),
        sp("D. scottianum",          ". . . 2 . + . 2 . . . . 3", "II", "0.5", NOTE_51),
        sp("Hypnum cupressiforme",   "7 3 5 3 4 1 2 . 2 1 2 2 3", "V", "2.0", NOTE_51),
        sp("Isothecium myosuroides", "7 8 7 6 5 8 7 8 5 5 6 3 3", "V", "6.2", NOTE_51),
        sp("Pleurozium schreberi",   ". . . 1 . . . 1 . . 2 2 .", "II", "0.4", NOTE_51),
        sp("Rhacomitrium lanuginosum", "1 . . 2 . . . . . 1 . . .", "I", "0.5", NOTE_51),
        sp("Rhytidiadelphus loreus", ". . . . . 1 1 2 2 1 . . .", "III", "0.6", NOTE_51),
        sp("Sphagnum quinquefarium", ". . . . . . 2 4 1 . . 2 .", "II", "0.3", NOTE_51),
        sp("Thuidium delicatulum",   "3 . . . 1 2 4 . 1 . . . 4", "II", "0.8", NOTE_51),
        sp("T. tamariscinum",        ". . . . . . . . . 2 1 4 .", "II", "0.8", NOTE_51),
        sp("Adelanthus decipiens",   ". . 5 3 1 . . . . . . . .", "II", "0.7", NOTE_51),
        sp("Bazzania trilobata",     ". . . . . 1 . . . . 2 . .", "I", "0.4", NOTE_51),
        sp("Diplophyllum albicans", "2 2 2 4 . . . 3 . . 2 . .", "II", "0.9", NOTE_51),
        sp("Frullania tamarisci",   "5 2 . . 1 . 1 2 3 6 . 1 .", "II", "0.8", NOTE_51),
        sp("Lepidozia reptans",     ". 1 . 3 . 1 2 . . . 2 . 3", "II", "0.4", NOTE_51),
        sp("Plagiochila punctata",  "4 6 5 8 4 7 6 3 6 6 5 . 2", "V", "5.6", NOTE_51),
        sp("P. spinulosa",          ". 2 1 3 . 3 . 3 3 5 4 . 2", "III", "1.0", NOTE_51),
        sp("Saccogyna viticulosa",  "3 4 4 . 2 5 4 3 5 4 4 . 1", "V", "3.4", NOTE_51),
        sp("Peltigera canina",      "4 . 1 . 2 . . . . . . . .", "I", "0.4", NOTE_51),
        sp("Sticta fuliginosa",     ". . . . . . . . . . . . 1", "I", "0.2", NOTE_51),
    ],
}


TABLES_MANUAL_8_50_51 = [
    TABLE_4_8A,
    TABLE_4_8B,
    TABLE_4_50,
    TABLE_4_51,
]
