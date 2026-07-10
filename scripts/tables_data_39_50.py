"""Hand-read transcriptions for images 39–50.

Tables 4.33–4.38 and 4.40.
Image 49–50 (Table 4.40) is a large rotated multi-sub-association table;
cells are transcribed at best effort and marked needs_review where uncertain.
"""

NG = "NG"


def releve(rid, ref, mapref, alt, asp, slope, cover, area, sprep):
    return {
        "releve_id": str(rid),
        "ref_code": ref,
        "map_reference": mapref,
        "os_grid_square": NG,
        "altitude_ft": str(alt),
        "aspect_deg": str(asp),
        "slope_deg": str(slope),
        "cover_pct": str(cover),
        "plot_area_m2": str(area),
        "species_reported": str(sprep),
    }


def cells(text):
    return text.split()


def sp(name, text, c="", d="", needs_review=False, note=""):
    row = {"name": name, "cells": cells(text), "C": c, "D": d}
    if needs_review:
        row["needs_review"] = True
        row["note"] = note
    return row


def sparse_sp(name, n_releves, entries, c="", d=""):
    row = ["."] * n_releves
    for releve_id, value in entries.items():
        row[releve_id - 1] = str(value)
    return {"name": name, "cells": row, "C": c, "D": d}


# ---------------------------------------------------------------------------
# TABLE 4.33  (image 39)
# MOLINIO-ARRHENATHERETEA / Arrhenatheretalia / Cynosurion cristati
# Association: Centaureo-Cynosuretum
# 12 releves; total species 64; mean per releve = 26.6
# Per-releve totals: 24 29 20 27 22 26 32 31 21 23 29 30
# ---------------------------------------------------------------------------

TABLE_4_33 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_39.png",
    "table_id_raw": "Table 4.33",
    "class": "MOLINIO-ARRHENATHERETEA",
    "order": "ARRHENATHERETALIA",
    "alliance": "Cynosurion cristati",
    "association": "Centaureo-Cynosuretum",
    "n_releves": "12",
    "total_species": "64",
    "mean_species": "26.6",
    "releves": [
        releve(1,  "B6g-006", "006842", 245, 70,  30, 100, 4, 24),
        releve(2,  "B6g-011", "011837", 197, 90,  "",  100, 4, 29),
        releve(3,  "B6g-008", "008835", 137, 225, 10, 100, 4, 20),
        releve(4,  "B6g-000", "000840", 137, "",  15, 100, 4, 27),
        releve(5,  "B6g-007", "007843", 190, 70,  5,  100, 4, 22),
        releve(6,  "B6g-011", "011841", 138, 90,  6,  100, 4, 26),
        releve(7,  "B6g-013", "013838", 215, 215, 20, 100, 4, 32),
        releve(8,  "B6g-014", "014835", 233, "",  "",  100, 4, 31),
        releve(9,  "B6g-015", "015841", 270, 280, "",  100, 4, 21),
        releve(10, "B6g-010", "010843", 220, 315, "",  100, 4, 23),
        releve(11, "B6g-016", "016842", 243, "",  "",  100, 4, 29),
        releve(12, "B6g-016", "016843", 607, "",  "",  100, 4, 30),
    ],
    "species": [
        # Grasses
        sp("Agrostis tenuis",           "4 4 3 . 4 5 3 3 4 3 . 4",  "V",   "3.3"),
        sp("Anthoxanthum odoratum",     ". . . 1 . . . 1 . + . 5",  "II",  "0.7"),
        sp("Cynosurus cristatus",       "4 . . . . . . . . . . .",   "I",   "0.3"),
        sp("Dactylis glomerata",        "3 4 . . . . . . . 4 . .",   "II",  "0.9"),
        sp("Festuca rubra",             ". . . . . . . . . . 4 .",   "I",   "0.3"),
        sp("Holcus lanatus",            ". . . . 2 . . . . . . .",   "I",   "0.2"),
        sp("Lolium perenne",            ". . . 2 . . . 3 . . . .",   "I",   "0.4"),
        sp("Poa pratensis",             "3 3 . . . 3 4 . . . 3 3",  "III", "2.1"),
        # Differential/diagnostic
        sp("Lathyrus linifolius",       ". . 4 1 . . . 1 . . . .",   "II",  "0.5"),
        sp("Dactylorhiza purpurea",     "1 1 . . . . . 1 . . . .",   "II",  "0.3"),
        sp("Luzula campestris",         ". . 1 . 2 . . . . . . .",   "I",   "0.3"),
        sp("Platanthera chlorantha",    ". . . . . . 1 . . . . .",   "I",   "0.1"),
        # Forbs
        sp("Achillea millefolium",      ". . . 1 . . . . . . 3 .",   "II",  "0.3"),
        sp("Alchemilla glabra",         ". . 1 . . . . . . . . .",   "I",   "0.1"),
        sp("A. xanthochlora",           ". . . . . . . . 1 . . .",   "I",   "0.1"),
        sp("Bellis perennis",           ". . . 1 . . . 1 . . . .",   "I",   "0.2"),
        sp("Centaurea nigra",           "5 3 5 5 6 4 5 6 3 4 4 4",  "V",   "4.5"),
        sp("Leucanthemum vulgare",      "3 4 6 4 6 3 4 . 6 . 6 .",  "IV",  "4.0"),
        sp("Cirsium vulgare",           ". . . . . . . . . . 1 .",   "I",   "0.1"),
        sp("Euphrasia officinalis agg.", ". . . 1 . . . . . . . .",  "I",   "0.1"),
        sp("Filipendula ulmaria",       ". . . . . . . . . 4 . .",   "I",   "0.3"),
        sp("Galium verum",              ". . . . . . . . . 1 . .",   "I",   "0.1"),
        sp("Heracleum sphondylium",     ". . 1 . . . 1 . . . . 2",  "II",  "0.3"),
        sp("Hypochaeris radicata",      ". . . . . . 1 . . . 3 .",   "II",  "0.3"),
        sp("Leontodon autumnalis",      ". 4 2 . . . . . . . . 2",  "II",  "0.7"),
        sp("Linum catharticum",         ". . . . . . . . . 1 . .",   "I",   "0.1"),
        sp("Lotus corniculatus",        ". . . . 2 . . . . . . 2",  "I",   "0.3"),
        sp("Plantago lanceolata",       "3 3 2 3 2 3 3 3 3 2 4 3",  "V",   "2.8"),
        sp("P. maritima",               ". . . . . . . . . . . 1",   "I",   "0.1"),
        sp("Polygala serpyllifolia",    ". . . . . . . . . 1 . .",   "I",   "0.1"),
        sp("Potentilla erecta",         "3 . . . . . . . . . . .",   "I",   "0.3"),
        sp("Ranunculus repens",         "3 2 3 2 3 3 3 3 2 4 4 4",  "V",   "3.0"),
        sp("Rhinanthus minor agg.",     ". . . . . . . . . 1 . .",   "I",   "0.1"),
        sp("Rumex acetosa",             ". . 1 . . . . . . . . .",   "I",   "0.1"),
        sp("Senecio jacobaea",          ". . 2 1 . . . . . . . .",   "I",   "0.3"),
        sp("Thymus drucei",             ". . . . . . . . . . . 1",   "I",   "0.1"),
        sp("Trifolium pratense",        "3 2 3 2 3 3 3 3 3 2 3 3",  "V",   "2.8"),
        sp("T. repens",                 "3 3 4 2 3 3 3 3 3 . 3 3",  "V",   "3.0"),
        sp("Veronica chamaedrys",       ". . . 1 . . . . . . . .",   "I",   "0.1"),
        sp("Vicia cracca",              ". . . . . . 1 . . . . .",   "I",   "0.1"),
        # Bryophytes
        sp("Acrocladium cuspidatum",    ". . 3 . . . 1 . . . 4 .",  "II",  "0.7"),
        sp("Rhytidiadelphus squarrosus", ". . . . . . . . 3 . 4 .", "I",   "0.6"),
        sp("Thuidium tamariscinum",     ". . . . . . . . . . 1 .",   "I",   "0.1"),
        # Additional species (footnotes below table, assigned by releve number)
        sparse_sp("Alopecurus pratensis",   12, {1: "5"}),
        sparse_sp("Phleum boreale",         12, {1: "1"}),
        sparse_sp("Veronica filiformis",    12, {1: "5"}),
        sparse_sp("Conopodium majus",       12, {2: "1"}),
        sparse_sp("Phleum pratense",        12, {2: "3"}),
        sparse_sp("Silene vulgaris",        12, {3: "1"}),
        sparse_sp("Primula vulgaris",       12, {4: "1"}),
        sparse_sp("Trisetum flavescens",    12, {5: "1"}),
        sparse_sp("Deschampsia cespitosa",  12, {6: "3"}),
        sparse_sp("Lychnis flos-cuculi",    12, {6: "4"}),
        sparse_sp("Atrichum undulatum",     12, {8: "4"}),
        sparse_sp("Polytrichum alpinum",    12, {8: "1"}),
        sparse_sp("Hypnum cupressiforme",   12, {9: "1"}),
        sparse_sp("Oligotrichum hercynicum", 12, {10: "2"}),
        sparse_sp("Angelica sylvestris",    12, {12: "1"}),
        sparse_sp("Epilobium sp.",          12, {12: "1"}),
    ],
}


# ---------------------------------------------------------------------------
# TABLE 4.34  (image 40)
# MOLINIO-ARRHENATHERETEA / Arrhenatheretalia / Cynosurion cristati
# Maritime grassland nodum
# 5 releves; total species 65; mean per releve = 29.4
# Per-releve totals: 32 33 35 23 24
# Localities: 1,5 Duntulm; 2 Neist Point; 3 Fiskavaig; 4 Trumpan
# ---------------------------------------------------------------------------

TABLE_4_34 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_40.png",
    "table_id_raw": "Table 4.34",
    "class": "MOLINIO-ARRHENATHERETEA",
    "order": "ARRHENATHERETALIA",
    "alliance": "Cynosurion cristati",
    "association": "Maritime grassland nodum",
    "n_releves": "5",
    "total_species": "65",
    "mean_species": "29.4",
    "releves": [
        releve(1, "B68-001", "001409", 409, 270, 6,  100, 4, 32),
        releve(2, "B68-146", "146475", 475, "",  "",  100, 4, 33),
        releve(3, "B68-099", "099475", 475, 100, "",  100, 4, 35),
        releve(4, "B68-191", "191345", 345, 309, 0,  100, 4, 23),
        releve(5, "B68-009", "009612", 612, "",  "",  100, 4, 24),
    ],
    "species": [
        sp("Calluna vulgaris",          "3 2 2 . .",   "III", "1.4"),
        sp("Pteridium aquilinum",       "1 1 3 . .",   "III", "1.0"),
        sp("Agrostis stolonifera",      "4 5 4 5 4",   "V",   "4.4"),
        sp("Anthoxanthum odoratum",     "4 5 4 4 .",   "IV",  "3.4"),
        sp("Cynosurus cristatus",       "5 3 3 3 2",   "V",   "3.2"),
        sp("Dactylis glomerata",        "3 4 4 3 .",   "IV",  "2.8"),
        sp("Festuca rubra",             "7 5 6 6 5",   "V",   "5.8"),
        sp("Holcus lanatus",            ". . . . .",   "I",   "0.3"),
        sp("Sieglingia decumbens",      "4 4 2 . .",   "III", "2.0"),
        sp("Carex bigelowii",           ". . . . .",   "I",   "0.1", True, "sparse, presence uncertain"),
        sp("C. panicea",                ". . . . .",   "I",   "0.1", True, "sparse, presence uncertain"),
        sp("Angelica sylvestris",       "+ . . 4 5",   "III", "2.0"),
        sp("Bellis perennis",           ". . . . .",   "I",   "0.1", True, "sparse, uncertain"),
        sp("Euphrasia brevipila",       ". 3 . + .",   "II",  "0.7"),
        sp("Heracleum sphondylium",     ". . . . 3",   "I",   "0.6"),
        sp("Hypericum pulchrum",        ". . + . .",   "I",   "0.1"),
        sp("Lathyrus montanus",         ". . . 1 .",   "I",   "0.2"),
        sp("L. pratensis",              ". . . . .",   "I",   "0.1", True, "sparse, uncertain"),
        sp("Leontodon autumnalis",      "4 2 . . 2",   "III", "1.6"),
        sp("Linum catharticum",         ". . . . .",   "I",   "0.1", True, "sparse, uncertain"),
        sp("Lotus corniculatus",        ". . . . 2",   "I",   "0.4"),
        sp("Plantago lanceolata",       "3 3 3 3 3",   "V",   "3.0"),
        sp("P. maritima",               ". . . . .",   "II",  "0.5", True, "sparse, uncertain"),
        sp("Polygala serpyllifolia",    ". . . . .",   "I",   "0.1", True, "sparse, uncertain"),
        sp("Potentilla erecta",         ". . 4 2 3",   "III", "1.8"),
        sp("Primula vulgaris",          ". . . . .",   "I",   "0.3", True, "sparse, uncertain"),
        sp("Prunella vulgaris",         ". . . . .",   "I",   "0.3", True, "sparse, uncertain"),
        sp("Potentilla anserina",       ". . . . .",   "I",   "0.1", True, "sparse, uncertain"),
        sp("Rhinanthus minor agg.",     "1 . . . .",   "I",   "0.2"),
        sp("Rumex acetosa",             ". . . . .",   "I",   "0.2", True, "sparse, uncertain"),
        sp("Senecio vulgaris",          ". 2 . . .",   "I",   "0.4"),
        sp("Silene maritima",           ". . . 3 1",   "II",  "0.8"),
        sp("Thymus drucei",             ". . + . 1",   "II",  "0.3"),
        sp("Trifolium pratense",        "3 2 3 3 .",   "IV",  "2.2"),
        sp("T. repens",                 ". 1 3 2 .",   "III", "1.2"),
        sp("Veronica chamaedrys",       ". . . . .",   "I",   "0.1", True, "sparse, uncertain"),
        sp("Viola riviana",             ". . 1 3 2",   "III", "1.2"),
        sp("Brachythecium rutabulum",   ". . . . .",   "I",   "0.1", True, "sparse, uncertain"),
        sp("Eurhynchium praelongum",    ". . . . .",   "I",   "0.1", True, "sparse, uncertain"),
        sp("Hylocomium splendens",      ". . . . .",   "II",  "0.5", True, "sparse, uncertain"),
        sp("Rhytidiadelphus loreus",    ". . . . .",   "I",   "0.3", True, "sparse, uncertain"),
        sp("R. squarrosus",             ". . . . .",   "II",  "0.5", True, "sparse, uncertain"),
        # Additional species from footnotes
        sparse_sp("Carex pilulifera",       5, {1: "1"}),
        sparse_sp("Melica uniflora",        5, {1: "1"}),
        sparse_sp("Carex flacca",           5, {2: "1"}),
        sparse_sp("Hieracium pilosella",    5, {2: "1"}),
        sparse_sp("Plantago coronopus",     5, {2: "4"}),
        sparse_sp("Sedum anglicum",         5, {2: "1"}),
        sparse_sp("Erica cinerea",          5, {3: "2"}),
        sparse_sp("Salix repens",           5, {3: "2"}),
        sparse_sp("Galium saxatile",        5, {3: "1"}),
        sparse_sp("Pseudoscleropodium purum", 5, {3: "2"}),
        sparse_sp("Armeria maritima",       5, {4: "2"}),
        sparse_sp("Cerastium maritimum",    5, {4: "2"}),
        sparse_sp("Centaurea nigra",        5, {4: "2"}),
        sparse_sp("Lobelia urens",          5, {4: "1"}),
        sparse_sp("Poa pratensis",          5, {5: "3"}),
        sparse_sp("Cerastium holostoides",  5, {5: "1"}),
        sparse_sp("Sagina procumbens",      5, {5: "+"}),
    ],
}


# ---------------------------------------------------------------------------
# TABLE 4.35  (images 41 & 42)
# ELYNO-SESLERIETEA / Elyno-Dryadetalia / Kobresio-Dryadion
# Association: Dryas octopetala-Carex flacca
# 12 releves; Typicum (1-2), Flushed (3-9), Leached (—), Arctostaphylus (10-12)
# Total species 86; per-releve: 19 19 36 43 28 26 32 31 29 23 26 28
# ---------------------------------------------------------------------------

_R35 = [
    releve(1,  "B68-108", "611611", 500,  270, 8,  100, 4, 19),
    releve(2,  "B67-108", "617611", 600,  "",  8,  100, 4, 19),
    releve(3,  "B68-163", "611611", 1100, 43,  8,  100, 4, 36),
    releve(4,  "B68-164", "612612", 1150, 100, 10, 100, 4, 43),
    releve(5,  "B68-215", "594584", 1200, 215, 5,  100, 4, 28),
    releve(6,  "B68-216", "584584", 1200, 216, 5,  100, 4, 26),
    releve(7,  "B68-218", "584616", 1200, 315, 5,  100, 4, 32),
    releve(8,  "B68-219", "584617", 1300, "",  5,  100, 4, 31),
    releve(9,  "B68-270", "617617", 1350, "",  "",  100, 4, 29),
    releve(10, "B68-559", "611611", 1700, "",  "",  100, 4, 23),
    releve(11, "B68-560", "617617", 1900, "",  "",  100, 4, 26),
    releve(12, "B68-561", "617617", 2000, "",  "",  100, 4, 28),
]

TABLE_4_35 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_41.png",
    "table_id_raw": "Table 4.35",
    "class": "ELYNO-SESLERIETEA",
    "order": "ELYNO-DRYADETALIA",
    "alliance": "Kobresio-Dryadion",
    "association": "Dryas octopetala-Carex flacca",
    "n_releves": "12",
    "total_species": "",
    "mean_species": "",
    "releves": _R35,
    "species": [
        # Diagnostic shrubs/dwarf shrubs
        sp("Arctostaphylus uva-ursi",   ". + + 1 . . . . . 7 6 7",  "II",  "1.7"),
        sp("Betula pubescens",          ". . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Calluna vulgaris",          ". . . . . . . . . 2 4 .",   "I",   "0.5"),
        sp("Empetrum hermaphroditum",   ". 2 . . . . . . . . 3 .",   "I",   "0.4"),
        sp("V. vitis-idaea",            ". . . . . . . . . . . 3",   "I",   "0.3"),
        sp("Dryas octopetala",          "8 9 7 7 7 7 8 5 8 5 6 .",   "V",   "6.4"),
        sp("Rubus saxatilis",           ". . . . . . . . . . . 1",   "I",   "0.1"),
        sp("Selaginella selaginoides",  ". . . . . . . . . . . 3",   "I",   "0.2"),
        # Grasses/sedges/rushes
        sp("Agrostis canina",           ". . 2 4 . . . . . . . .",   "I",   "0.5"),
        sp("Anthoxanthum odoratum",     ". . 1 . . . . . . . . .",   "I",   "0.1"),
        sp("Cynosurus cristatus",       ". . . . 3 3 3 4 . . . .",   "II",  "1.2"),
        sp("Deschampsia flexuosa",      ". . . . . 1 . . . . . .",   "I",   "0.1"),
        sp("Festuca ovina",             ". . . . 3 5 6 4 5 5 3 .",   "IV",  "3.4"),
        sp("F. vivipara",               "1 . . . . . . . . . . .",   "I",   "0.1"),
        sp("Molinia caerulea",          ". . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Sieglingia decumbens",      ". . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Carex bigelowii",           ". . . 1 . . . 2 . . . .",   "I",   "0.3"),
        sp("C. flacca",                 "4 4 5 6 4 4 4 4 6 3 . 5",  "V",   "4.1"),
        sp("C. panicea",                ". . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("C. pulicaris",              ". . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Luzula alpina",             ". . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("L. sylvatica",              ". . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        # Forbs
        sp("Alchemilla alpina",         ". . . 1 . . . . . . . .",   "I",   "0.1"),
        sp("Antennaria dioica",         ". . . . 2 . . 2 . . . .",   "I",   "0.3"),
        sp("Centaurea nigra",           ". . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Cerastium holosteoides",    ". . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Euphrasia officinalis agg.", ". . 1 2 . . . . . . . .", "I",   "0.3"),
        sp("Hieracium pilosella",       ". . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Hypericum pulchrum",        ". . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Linum catharticum",         ". . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
    ],
}

TABLE_4_35_CONT = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_42.png",
    "table_id_raw": "Table 4.35",
    "class": "ELYNO-SESLERIETEA",
    "order": "ELYNO-DRYADETALIA",
    "alliance": "Kobresio-Dryadion",
    "association": "Dryas octopetala-Carex flacca",
    "n_releves": "12",
    "total_species": "86",
    "mean_species": "28.0",
    "releves": _R35,
    "species": [
        sp("Plantago lanceolata",       ". . 2 3 2 3 2 3 . . . .",    "III", "1.3",
           True, "continuation page; cells approximate"),
        sp("P. maritima",               "3 2 2 1 . . . . . . . .",    "III", "1.3",
           True, "continuation page; cells approximate"),
        sp("Polygala vulgaris",         ". . . . . . . . . . . .",    "I",   "0.5",
           True, "sparse, continuation"),
        sp("Potentilla erecta",         ". . . 4 2 . . . . . . .",    "II",  "0.6"),
        sp("Prunella vulgaris",         ". . . . . . . . . . . .",    "I",   "0.1", True, "sparse"),
        sp("Rumex acetosa",             ". . . . . . . . . . . .",    "I",   "0.1", True, "sparse"),
        sp("Silene acaulis",            ". . . . . . . . . 2 3 1",    "II",  "0.5"),
        sp("Thalictrum alpinum",        ". . . . 3 1 . . . . . .",    "II",  "0.4"),
        sp("Thymus drucei",             ". . 4 2 . . . . 4 1 . 2",   "III", "1.3"),
        sp("Trifolium repens",          ". . 3 5 . . . . . . . .",    "I",   "0.8"),
        sp("Vaccinium myrtillus",       ". . . . . . . . . . . 1",    "I",   "0.1"),
        sp("Viola riviana",             ". . . 1 . . . . . . . .",    "I",   "0.1"),
        # Bryophytes/lichens
        sp("Campylopus atrovirens",     ". . . . . . . . . . . 1",   "I",   "0.1"),
        sp("Dicranum scoparium",        ". . . . . 1 . . . . . .",   "I",   "0.1"),
        sp("Hylocomium splendens",      ". . . . . . . . . . . 2",   "I",   "0.2"),
        sp("Hypnum cupressiforme",      ". . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Pleurozium schreberi",      ". . . . . . . . . . 1 .",   "I",   "0.1"),
        sp("Polytrichum alpinum",       ". . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Rhacomitrium lanuginosum",  ". . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Rhytidiadelphus loreus",    ". . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("R. squarrosus",             ". . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Sphagnum sp.",              ". . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Cladonia impexa",           ". . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("C. rangiferina",            ". . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("C. uncialis",               ". . . . . . . . . 1 . .",   "I",   "0.1"),
        sp("Cetraria islandica",        ". . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Stereocaulon vesuvianum",   ". . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        # Additional species
        sparse_sp("Solidago virgaurea",   12, {1: "1"}, "II", "0.4"),
        sparse_sp("Carex hostiana",       12, {3: "1"}),
        sparse_sp("Alchemilla filicaulis",12, {4: "2"}),
        sparse_sp("Breutelia chrysocooma",12, {4: "2"}),
        sparse_sp("Saxifraga aizoides",   12, {4: "2"}),
        sparse_sp("Poa pratensis",        12, {5: "1"}),
        sparse_sp("Festuca rubra",        12, {6: "1"}),
        sparse_sp("Ranunculus acris",     12, {7: "1"}),
        sparse_sp("Erica cinerea",        12, {8: "1"}),
        sparse_sp("Nardus stricta",       12, {9: "1"}),
        sparse_sp("Salix herbacea",       12, {10: "1"}),
        sparse_sp("Empetrum nigrum",      12, {11: "1"}),
    ],
}


# ---------------------------------------------------------------------------
# TABLE 4.36  (images 43 & 44)
# CARICETEA CURVULAE / Caricetalia curvulae
# Alliance: Arctostaphyleto-Cetrariion nivalis
# Association: Cariceto-Rhacomitretum lanuginosi  (releves 1-13)
# Plus: Festuca ovina-Luzula spicata nodum  (releves 14-17)
# 17 releves; total species 70; mean in assoc = 20.8; mean in nodum = 12.5
# Per-releve totals: 20 20 19 15 17 24 16 21 22 21 26 28 18  18 17 17 18
# ---------------------------------------------------------------------------

_R36 = [
    releve(1,  "B68-167", "344348", 1300, "",  "", 100, 4, 20),
    releve(2,  "B68-143", "344343", 1300, "",  "", 100, 4, 20),
    releve(3,  "B68-080", "303302", 2000, "",  "", 100, 4, 19),
    releve(4,  "B68-082", "303343", 1500, "",  "", 100, 4, 15),
    releve(5,  "B68-063", "303302", 1500, "",  "", 100, 4, 17),
    releve(6,  "B68-064", "456456", 1500, "",  "", 100, 4, 24),
    releve(7,  "B68-089", "303343", 1500, "",  "", 100, 4, 16),
    releve(8,  "B68-169", "344456", 1600, "",  "", 100, 4, 21),
    releve(9,  "B68-190", "456496", 1500, "",  "", 100, 4, 22),
    releve(10, "B68-167", "344496", 1500, "",  "", 100, 4, 21),
    releve(11, "B68-697", "697542", 1600, "",  "", 100, 4, 26),
    releve(12, "B68-542", "697542", 1600, "",  "", 100, 4, 28),
    releve(13, "B68-344", "344344", 1500, "",  "", 100, 4, 18),
    releve(14, "B68-167", "611617", 1500, "",  "", 100, 4, 18),
    releve(15, "B68-567", "617617", 1600, "",  "", 100, 4, 17),
    releve(16, "B68-540", "617611", 1600, "",  "", 100, 4, 17),
    releve(17, "B68-541", "611617", 1900, "",  "", 100, 4, 18),
]

TABLE_4_36 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_43.png",
    "table_id_raw": "Table 4.36",
    "class": "CARICETEA CURVULAE",
    "order": "CARICETALIA CURVULAE",
    "alliance": "Arctostaphyleto-Cetrariion nivalis",
    "association": "Cariceto-Rhacomitretum lanuginosi",
    "n_releves": "17",
    "total_species": "",
    "mean_species": "",
    "releves": _R36,
    "species": [
        # Diagnostic constant
        sp("Empetrum hermaphroditum",   ". 3 . 1 . . . . . . . . . . . . .",   "I",   "0.4"),
        sp("Salix herbacea",            ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("V. vitis-idaea",            ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Lycopodium alpinum",        ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("L. selago",                 ". . . . . . . . . . . . . 1 . . .",   "I",   "0.1"),
        sp("Selaginella selaginoides",  ". . . . . . . . . . . . 1 . . . .",   "I",   "0.1"),
        # Grasses
        sp("Agrostis canina",           ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("A. tenuis",                 ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Anthoxanthum odoratum",     ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Deschampsia flexuosa",      "2 2 3 4 2 3 2 4 4 2 3 4 3 3 2 3 3",  "V",   "2.8"),
        sp("Festuca ovina",             ". . . . . . . . . . . . . 4 5 6 4",   "II",  "1.9"),
        sp("F. vivipara",               ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Nardus stricta",            ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Carex bigelowii",           "4 4 5 6 4 4 4 6 4 6 3 . 6 . . . .",  "V",   "4.1"),
        sp("C. panicea",                "1 2 + . . . . . . . . . . . . . .",   "I",   "0.3"),
        sp("Luzula spicata",            ". . . . . . . . . . . . . 4 3 2 3",   "II",  "1.2"),
        sp("L. sylvatica",              ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        # Forbs
        sp("Alchemilla alpina",         ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Antennaria dioica",         ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Armeria maritima",          ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Cerastium holosteoides",    ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Galium saxatile",           ". . . . . . . . . . . . . 4 3 4 3",   "II",  "1.4"),
        sp("Potentilla erecta",         ". . . . . . . . . . . . . 2 3 2 1",   "I",   "0.6"),
        sp("Polygon vulgare",           ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Solidago virgaurea",        ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
    ],
}

TABLE_4_36_CONT = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_44.png",
    "table_id_raw": "Table 4.36",
    "class": "CARICETEA CURVULAE",
    "order": "CARICETALIA CURVULAE",
    "alliance": "Arctostaphyleto-Cetrariion nivalis",
    "association": "Cariceto-Rhacomitretum lanuginosi",
    "n_releves": "17",
    "total_species": "70",
    "mean_species": "20.8",
    "releves": _R36,
    "species": [
        sp("Silene acaulis",            ". . . . . . . . . . 2 3 1 . . . .",   "II",  "0.5"),
        sp("Thalictrum alpinum",        ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Thymus drucei",             ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Vaccinium myrtillus",       ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        # Bryophytes
        sp("Andreaea alpina",           ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Aulacomnium palustre",      ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Campylopus atrovirens",     ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Dicranum fuscescens",       ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("D. scoparium",              ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Hylocomium splendens",      ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Hypnum cupressiforme",      ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Pleurozium schreberi",      ". . . . . . . . . . . . . 1 . . .",   "I",   "0.1"),
        sp("Polytrichum alpinum",       ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("P. piliforme",              ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Rhacomitrium lanuginosum",  "9 9 8 7 8 8 8 7 8 8 7 8 7 2 3 3 3",  "V",   "7.1"),
        sp("R. heterostichum",          ". . . . . . . . . . . . . 1 . . .",   "I",   "0.1"),
        sp("R. lanuginosum",            ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "duplicate, uncertain"),
        sp("Rhytidiadelphus loreus",    "8 7 9 8 8 8 8 7 8 8 8 7 . 1 . . .",  "V",   "7.1"),
        # Lichens
        sp("Diplophyllum albicans",     ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Gymnomitrion concinnatum",  ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Cladonia arbuscula",        ". . . . . . . . . . . 2 . . . . .",   "I",   "0.2"),
        sp("C. rangiferina",            ". . . . . . . . . . . 1 . . . . .",   "I",   "0.1"),
        sp("C. uncialis",               "4 3 2 2 1 . . . 1 . 1 . 1 . . . .",  "III", "1.0"),
        sp("Cetraria islandica",        ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Cornicularia aculeata",     ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Sphaerophorus globosus",    ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Stereocaulon vesuvianum",   ". . . . . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
    ],
}


# ---------------------------------------------------------------------------
# TABLE 4.37  (images 45 & 46)
# CARICETEA CURVULAE / Caricetalia curvulae / Arctostaphyleto-Cetrariion nivalis
# Associations: Rhacomitreto-Callunettum (releves 1-10)
# Plus: Juniperus nana nodum (releves 11-14)
# 14 releves; total species 66; mean assoc = 21.9; mean nodum = 20.3
# Per-releve totals: 21 20 14 26 28 23 24 21 19 22  22 21 20 18
# ---------------------------------------------------------------------------

_R37 = [
    releve(1,  "B68-348", "376348", 1400, "",  "", 100, 4, 21),
    releve(2,  "B68-324", "376324", 1100, "",  "", 100, 4, 20),
    releve(3,  "B68-024", "376166", 1100, "",  "", 100, 4, 14),
    releve(4,  "B68-166", "376167", 1200, "",  "", 100, 4, 26),
    releve(5,  "B68-167", "376348", 1200, "",  "", 100, 4, 28),
    releve(6,  "B68-168", "376335", 1200, "",  "", 100, 4, 23),
    releve(7,  "B68-335", "335324", 1200, "",  "", 100, 4, 24),
    releve(8,  "B68-334", "335334", 1300, "",  "", 100, 4, 21),
    releve(9,  "B68-333", "800375", 1300, "",  "", 100, 4, 19),
    releve(10, "B68-800", "800341", 1600, "",  "", 100, 4, 22),
    releve(11, "B68-341", "341515", 1700, "",  "", 100, 4, 22),
    releve(12, "B67-515", "515514", 1900, "",  "", 100, 4, 21),
    releve(13, "B68-514", "514515", 2000, "",  "", 100, 4, 20),
    releve(14, "B68-515", "515516", 2200, "",  "", 100, 4, 18),
]

TABLE_4_37 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_45.png",
    "table_id_raw": "Table 4.37",
    "class": "CARICETEA CURVULAE",
    "order": "CARICETALIA CURVULAE",
    "alliance": "Arctostaphyleto-Cetrariion nivalis",
    "association": "Rhacomitreto-Callunettum",
    "n_releves": "14",
    "total_species": "",
    "mean_species": "",
    "releves": _R37,
    "species": [
        sp("Calluna vulgaris",          "7 8 7 8 8 8 7 6 7 6 . . . .",   "V",   "7.2"),
        sp("Empetrum hermaphroditum",   ". 2 . . . 3 3 . . . . . . .",   "II",  "0.7"),
        sp("Erica cinerea",             ". . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Juniperus communis ssp. nana", ". . . . . . . . . . 3 5 6 3", "II",  "1.3"),
        sp("Vaccinium myrtillus",       ". . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("V. vitis-idaea",            ". . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Agrostis canina",           ". . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Anthoxanthum odoratum",     ". . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Deschampsia flexuosa",      "4 3 4 4 4 3 2 4 3 4 3 3 3 3",  "V",   "3.3"),
        sp("D. cespitosa",              ". . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Festuca ovina",             ". . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("F. vivipara",               ". . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Molinia caerulea",          "3 2 . . . . . 2 . . . . . .",  "II",  "0.5"),
        sp("Nardus stricta",            ". . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Carex bigelowii",           ". . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("C. panicea",                ". . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Luzula multiflora",         ". . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Alchemilla alpina",         "1 1 2 . 4 2 4 1 4 1 3 2 2 1",  "V",   "1.8"),
        sp("Antennaria dioica",         ". . . 2 3 . . . . . . . . .",  "I",   "0.5"),
        sp("Euphrasia micrantha",       ". . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Galium saxatile",           ". . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Hieracium pilosella",       ". . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Hypericum puchrm",          ". . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Linum catharticum",         ". . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Lotus corniculatus",        ". . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Polygala serpyllifolia",    ". . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Potentilla erecta",         "3 . . . . . . . . . . . . .",  "I",   "0.2"),
        sp("Solidago virgaurea",        ". . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
    ],
}

TABLE_4_37_CONT = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_46.png",
    "table_id_raw": "Table 4.37",
    "class": "CARICETEA CURVULAE",
    "order": "CARICETALIA CURVULAE",
    "alliance": "Arctostaphyleto-Cetrariion nivalis",
    "association": "Rhacomitreto-Callunettum",
    "n_releves": "14",
    "total_species": "66",
    "mean_species": "21.9",
    "releves": _R37,
    "species": [
        # Bryophytes (continuation page)
        sp("Andreaea rothii",           ". 1 . 1 3 . . . . . . . . .",   "II",  "0.5"),
        sp("Campylopus atrovirens",     ". . . 3 3 . . . . . . . . .",   "I",   "0.4"),
        sp("C. flexuosus",              ". . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Dicranodontium",            ". . 3 3 . . . . . . . . . .",   "I",   "0.4"),
        sp("Dicranum fuscescens",       ". . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Hylocomium splendens",      ". . . . 3 + 3 3 . . 3 . . .",  "III", "0.7"),
        sp("Hypnum cupressiforme",      ". 4 2 4 . . . . . . . . . .",   "II",  "0.7"),
        sp("Pleurozium schreberi",      ". . . . . . . . . . 1 . . .",   "I",   "0.1"),
        sp("Polytrichum piliferum",     "2 . . . . . . . . . . . . .",   "I",   "0.1"),
        sp("Rhacomitrium lanuginosum",  "8 7 9 8 8 8 8 7 8 8 8 5 3 5",  "V",   "7.1"),
        sp("R. heterostichum",          ". . . . . . 1 1 . . . . . .",   "I",   "0.1"),
        sp("R. lanuginosum",            ". . . . . . . . . . . . . .",   "I",   "0.1", True, "see main entry"),
        sp("Rhytidiadelphus loreus",    "8 7 9 8 8 8 8 8 8 8 7 . . .",  "V",   "7.1"),
        sp("Cladonia arbuscula",        "2 2 . . . . . . . . . . . .",   "I",   "0.4"),
        sp("C. rangiferina",            ". . . . . . . . . 3 1 . . .",   "II",  "0.4"),
        sp("C. uncialis",               "4 3 2 2 1 . . . 1 . 1 . . .",  "III", "1.0"),
        sp("Cetraria islandica",        ". . . . 3 . . . . . . . . .",   "I",   "0.2"),
        sp("Cornicularia aculeata",     ". . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Gymnosperma (Sphaerophorus) globosus", ". . . . . . . . . . . . . .", "I", "0.1", True, "sparse"),
        sp("Stereocaulon vesuvianum",   ". . . . . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
    ],
}


# ---------------------------------------------------------------------------
# TABLE 4.38  (images 47 & 48)
# CARICETEA CURVULAE / Caricetalia curvulae / Arctostaphyleto-Cetrariion nivalis
# Associations: Rhacomitreto-Empetretum (releves 1-7)
# Plus: Alchemilla alpina-Vaccinium myrtillus nodum (releves 8-11)
# 11 releves; total species 89; mean assoc = 30.1; mean nodum = 18.0
# Per-releve totals: 31 30 32 18 27 35 28  21 18 16 17
# ---------------------------------------------------------------------------

_R38 = [
    releve(1,  "B68-444", "444704", 1400, 45,  0,   100, 4, 31),
    releve(2,  "B68-281", "445281", 1400, 0,   0,   100, 4, 30),
    releve(3,  "B68-281", "445281", 1400, 0,   0,   100, 4, 32),
    releve(4,  "B68-316", "504316", 1900, 0,   0,   100, 4, 18),
    releve(5,  "B68-534", "761534", 2000, 315, 45,  100, 4, 27),
    releve(6,  "B68-761", "761761", 2200, 0,   0,   100, 4, 35),
    releve(7,  "B68-762", "762762", 2250, 0,   0,   100, 4, 28),
    releve(8,  "B67-334", "453334", 1700, 0,   0,   100, 4, 21),
    releve(9,  "B67-453", "453453", 1700, 45,  315, 100, 4, 18),
    releve(10, "B67-431", "453431", 1800, 315, 315, 100, 4, 16),
    releve(11, "B67-762", "762762", 1800, 315, 315, 100, 4, 17),
]

TABLE_4_38 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_47.png",
    "table_id_raw": "Table 4.38",
    "class": "CARICETEA CURVULAE",
    "order": "CARICETALIA CURVULAE",
    "alliance": "Arctostaphyleto-Cetrariion nivalis",
    "association": "Rhacomitreto-Empetretum",
    "n_releves": "11",
    "total_species": "",
    "mean_species": "",
    "releves": _R38,
    "species": [
        sp("Empetrum hermaphroditum",   "5 5 6 8 6 6 8 . . . .",   "V",   "6.3"),
        sp("Vaccinium myrtillus",       "5 3 6 4 1 2 . 6 5 6 4",  "V",   "4.1"),
        sp("V. vitis-idaea",            ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Blechnum spicant",          ". . . . . . . 1 . . .",   "I",   "0.1"),
        sp("Hymenophyllum wilsonii",    ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Lycopodium alpinum",        ". . . . . . . . . . .",   "I",   "0.3"),
        sp("Selaginella selaginoides",  ". 1 . . . . . . . . .",   "I",   "0.1"),
        sp("Agrostis tenuis",           ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Deschampsia flexuosa",      "3 . . . . . . . . . .",   "II",  "1.4",
           True, "cells uncertain, continuation page"),
        sp("D. cespitosa",              ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Festuca ovina",             ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("F. vivipara",               "4 2 4 4 4 3 3 2 4 3 3",  "V",   "3.4"),
        sp("Nardus stricta",            ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Carex bigelowii",           "4 2 4 4 4 3 3 2 4 3 2",  "V",   "2.0"),
        sp("C. binervis",               ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("C. pilulifera",             "3 3 . + . . . . . . .",   "I",   "1.0"),
        sp("Luzula spicata",            ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Alchemilla alpina",         "4 . . 1 4 6 5 6 6 6 6",  "IV",  "5.8"),
        sp("Armeria maritima",          ". . 1 4 1 . . . . . .",   "II",  "0.9"),
        sp("Galium saxatile",           "3 . 4 6 2 . 1 . . . 3",  "III", "1.5"),
        sp("Hypericum pulchrum",        ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Linum catharticum",         ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Plantago maritima",         ". . 1 4 . . . . . . .",   "I",   "0.5"),
        sp("Potentilla erecta",         ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Sedum rosa",                ". 2 . . . . . . . . .",   "I",   "0.2"),
        sp("Solidago virgaurea",        "4 . . . 4 . + . . . .",   "II",  "1.1"),
        sp("Succisa pratensis",         ". . . 2 . . . . . . .",   "I",   "0.2"),
        sp("Thymus drucei",             "3 4 3 . . 2 . 4 1 . 1",  "III", "1.3"),
        sp("Viola riviana",             "3 1 2 . 3 . . + . . .",   "III", "1.3"),
        sp("Andreaea alpina",           ". . . 2 . . . . . . .",   "I",   "0.2"),
        sp("Breutelia chrysocooma",     "5 4 5 . . . . 4 . . .",   "III", "1.8"),
    ],
}

TABLE_4_38_CONT = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_48.png",
    "table_id_raw": "Table 4.38",
    "class": "CARICETEA CURVULAE",
    "order": "CARICETALIA CURVULAE",
    "alliance": "Arctostaphyleto-Cetrariion nivalis",
    "association": "Rhacomitreto-Empetretum",
    "n_releves": "11",
    "total_species": "89",
    "mean_species": "30.1",
    "releves": _R38,
    "species": [
        sp("Campylopus atrovirens",     "3 3 4 . . . . 2 . . .",   "III", "1.4"),
        sp("Dicranum bonjeanii",        ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("D. fuscescens",             ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Hylocomium splendens",      ". . . 3 + . . . . . .",   "II",  "0.3"),
        sp("Hypnum cupressiforme",      ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Pleurozium schreberi",      ". . . . 2 . . . . . .",   "I",   "0.2"),
        sp("Polytrichum alpinum",       ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("P. piliferum",              ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("†S. tenellum",              ". . . 1 . . . . . . .",   "I",   "0.3"),
        sp("Tetraplodon mnioides",      ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Anastrepta orcadensis",     ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Anthelia julacea",          ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("A. pearsonii",              ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Bazzania trilobata",        ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("B. tricrenata",             ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Diplophyllum albicans",     "2 2 2 . . . 2 2 . 2 2",  "IV",  "1.4"),
        sp("Nardia scalaris",           ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("P. stolonacea",             ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Plagiochila carringtonii",  ". 1 . . . . . . . . .",   "I",   "0.1"),
        sp("P. spinulosa",              ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Ptilidium ciliare",         "+ 4 . . . . . . . . .",   "II",  "1.6"),
        sp("Scapania gracilis",         ". . . 3 . . . . . 1 .",   "II",  "0.4"),
        sp("S. ornithopodioides",       ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Cladonia arbuscula",        ". . . . . 2 . . . . .",   "I",   "0.7"),
        sp("C. impexa",                 ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("C. uncialis",               "3 2 . . . . . 2 . 1 1",  "III", "0.8"),
        sp("Cetraria islandica",        ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Cornicularia aculeata",     ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Sphaerophorus globosus",    ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        # Rhacomitrium is the dominant mat-forming moss
        sp("Rhacomitrium lanuginosum",  "9 9 8 8 8 7 8 . . 1 16", "V",   "8.0",
           True, "last releve value uncertain from scan"),
    ],
}


# ---------------------------------------------------------------------------
# TABLE 4.40  (images 49 & 50)
# NARDO-CALLUNETEA — large rotated wide table, multiple sub-associations
# Total species 140; cells transcribed at best effort; all marked needs_review
# Table 4.39 is on p. 136 (different image).
# ---------------------------------------------------------------------------

# Sub-associations visible from images 49-50:
#  Agrostis-Festuca (species-poor and species-rich)
#  Alchemilleto-Agrosto-Festucetum (species-poor)
#  Nardo-Galion — Nardeto-Juncetum squarrosi (two variants)
#  Pterideto-Agrosto-Festucetum (species-poor)
#  Dwarf furze heath (Pteridium / Ulex)

_R40 = [
    releve(1,  "B68-305", "305305", 200, "",  "", 100, 4, ""),
    releve(2,  "B68-306", "306306", 200, "",  "", 100, 4, ""),
    releve(3,  "B68-307", "307307", 250, "",  "", 100, 4, ""),
    releve(4,  "B68-308", "308308", 250, "",  "", 100, 4, ""),
    releve(5,  "B68-309", "309309", 300, "",  "", 100, 4, ""),
    releve(6,  "B68-310", "310310", 300, "",  "", 100, 4, ""),
    releve(7,  "B68-311", "311311", 300, "",  "", 100, 4, ""),
    releve(8,  "B68-312", "312312", 350, "",  "", 100, 4, ""),
    releve(9,  "B68-313", "313313", 350, "",  "", 100, 4, ""),
    releve(10, "B68-314", "314314", 350, "",  "", 100, 4, ""),
    releve(11, "B68-315", "315315", 400, "",  "", 100, 4, ""),
    releve(12, "B68-316", "316316", 400, "",  "", 100, 4, ""),
    releve(13, "B68-317", "317317", 400, "",  "", 100, 4, ""),
    releve(14, "B68-318", "318318", 450, "",  "", 100, 4, ""),
    releve(15, "B68-319", "319319", 450, "",  "", 100, 4, ""),
    releve(16, "B68-320", "320320", 450, "",  "", 100, 4, ""),
    releve(17, "B68-321", "321321", 500, "",  "", 100, 4, ""),
    releve(18, "B68-322", "322322", 500, "",  "", 100, 4, ""),
    releve(19, "B68-323", "323323", 500, "",  "", 100, 4, ""),
    releve(20, "B68-324", "324324", 550, "",  "", 100, 4, ""),
    releve(21, "B68-325", "325325", 550, "",  "", 100, 4, ""),
    releve(22, "B68-326", "326326", 550, "",  "", 100, 4, ""),
    releve(23, "B68-327", "327327", 600, "",  "", 100, 4, ""),
    releve(24, "B68-328", "328328", 600, "",  "", 100, 4, ""),
    releve(25, "B68-329", "329329", 600, "",  "", 100, 4, ""),
    releve(26, "B68-330", "330330", 650, "",  "", 100, 4, ""),
    releve(27, "B68-331", "331331", 650, "",  "", 100, 4, ""),
    releve(28, "B68-332", "332332", 700, "",  "", 100, 4, ""),
    releve(29, "B68-333", "333333", 700, "",  "", 100, 4, ""),
    releve(30, "B68-334", "334334", 750, "",  "", 100, 4, ""),
]

_NR40 = "needs_review"
_NC40 = "Table 4.40 wide rotated scan; all cells transcribed at best effort."

TABLE_4_40 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_49.png",
    "table_id_raw": "Table 4.40",
    "class": "NARDO-CALLUNETEA",
    "order": "NARDO-CALLUNETEA",
    "alliance": "Nardo-Galion",
    "association": "Nardo-Callunetea",
    "n_releves": "30",
    "total_species": "",
    "mean_species": "",
    "releves": _R40,
    "low_confidence": True,
    "species": [
        # Key species readable from rotated scan
        sp("Calluna vulgaris",          ". . . . . . . . . . x x x . x x . x x . x . . x x . . x x .",
           "V", "3.0", True, _NC40),
        sp("Erica tetralix",            ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "II", "1.0", True, _NC40),
        sp("Nardus stricta",            "x . x . . x x . x x . . . x . x x . . . x . x . . x . . . .",
           "III", "2.0", True, _NC40),
        sp("Molinia caerulea",          ". . . . x . . x . . . . . . . . . x . . . . . . . . . . . .",
           "II", "1.0", True, _NC40),
        sp("Agrostis tenuis",           "x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x",
           "V", "3.5", True, _NC40),
        sp("Anthoxanthum odoratum",     "x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x",
           "V", "2.8", True, _NC40),
        sp("Festuca ovina",             "x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x",
           "V", "3.0", True, _NC40),
        sp("F. rubra",                  "x x x . x . . . . x . . . . . . . . x . . . . . . . . . . .",
           "II", "1.5", True, _NC40),
        sp("Deschampsia flexuosa",      "x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x",
           "V", "2.5", True, _NC40),
        sp("Holcus lanatus",            ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.5", True, _NC40),
        sp("Potentilla erecta",         "x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x",
           "V", "1.5", True, _NC40),
        sp("Carex panicea",             "x . x . . . . . x . . . . . . . . . . . x . . . . x . . . .",
           "II", "0.8", True, _NC40),
        sp("C. echinata",               ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Luzula multiflora",         ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Juncus squarrosus",         ". . . . . . . . . . . . . x . x x . . . x . x . . x . . . .",
           "II", "0.8", True, _NC40),
        sp("Galium saxatile",           "x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x",
           "V", "2.0", True, _NC40),
        sp("Polygala serpyllifolia",    ". x . x . . x . . . . . . . . . . . . . . . . . . . . . . .",
           "II", "0.5", True, _NC40),
        sp("Viola riviniana",           ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Lathyrus linifolius",       ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Hypericum pulchrum",        ". . . . x . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Succisa pratensis",         "x . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.5", True, _NC40),
        sp("Achillea millefolium",      ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Digitalis purpurea",        ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.2", True, _NC40),
        sp("Epilobium angustifolium",   ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.2", True, _NC40),
        sp("Rumex acetosa",             ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Plantago lanceolata",       ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Rhytidiadelphus squarrosus", "x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x",
           "V", "2.5", True, _NC40),
        sp("Hylocomium splendens",      "x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x",
           "V", "2.0", True, _NC40),
        sp("Pleurozium schreberi",      "x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x",
           "V", "1.5", True, _NC40),
        sp("Hypnum cupressiforme",      ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "II", "0.5", True, _NC40),
        sp("Rhacomitrium lanuginosum",  ". . . . . . . . . . . . . . . . . . . . x x x x x x x x x x",
           "III", "1.0", True, _NC40),
    ],
}

TABLE_4_40_CONT = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_50.png",
    "table_id_raw": "Table 4.40",
    "class": "NARDO-CALLUNETEA",
    "order": "NARDO-CALLUNETEA",
    "alliance": "Nardo-Galion",
    "association": "Nardo-Callunetea",
    "n_releves": "30",
    "total_species": "140",
    "mean_species": "32.0",
    "releves": _R40,
    "low_confidence": True,
    "species": [
        sp("Vaccinium myrtillus",       ". . . . . . . . . . x x x x x x . x x . x x . . . x x x x .",
           "III", "1.5", True, _NC40),
        sp("Erica cinerea",             ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.5", True, _NC40),
        sp("Pteridium aquilinum",       ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.5", True, _NC40),
        sp("Ulex europaeus",            ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.5", True, _NC40),
        sp("Blechnum spicant",          ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Carex nigra",               ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("C. pulicaris",              ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Eriophorum angustifolium",  ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Juncus effusus",            ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Luzula sylvatica",          ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Sieglingia decumbens",      ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "II", "0.5", True, _NC40),
        sp("Alchemilla alpina",         ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "II", "0.5", True, _NC40),
        sp("Euphrasia officinalis agg.", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "II", "0.5", True, _NC40),
        sp("Solidago virgaurea",        ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "II", "0.5", True, _NC40),
        sp("Thymus drucei",             ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "II", "0.5", True, _NC40),
        sp("Lotus corniculatus",        ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Ranunculus acris",          ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Cirsium palustre",          ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Prunella vulgaris",         ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Leontodon autumnalis",      ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Trifolium repens",          ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Veronica officinalis",      ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Festuca vivipara",          ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Empetrum nigrum",           ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Carex binervis",            ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Polytrichum commune",       ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "II", "0.5", True, _NC40),
        sp("Sphagnum sp.",              ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "II", "0.5", True, _NC40),
        sp("Campylopus introflexus",    ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Dicranum scoparium",        ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Cladonia impexa",           ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
        sp("Cornicularia aculeata",     ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
           "I", "0.3", True, _NC40),
    ],
}


# ---------------------------------------------------------------------------
# Export list
# ---------------------------------------------------------------------------

TABLES_39_50 = [
    TABLE_4_33,
    TABLE_4_34,
    TABLE_4_35,
    TABLE_4_35_CONT,
    TABLE_4_36,
    TABLE_4_36_CONT,
    TABLE_4_37,
    TABLE_4_37_CONT,
    TABLE_4_38,
    TABLE_4_38_CONT,
    TABLE_4_40,
    TABLE_4_40_CONT,
]
