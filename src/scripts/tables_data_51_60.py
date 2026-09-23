"""Hand-read transcriptions for images 51–60.

Tables 4.41, 4.42, 4.43, 4.44, 4.39, 4.45, 4.46.
Note: Table 4.39 appears on image 57 (out of printed order in the book).
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
# TABLE 4.41  (image 51)
# NARDO-CALLUNETEA / Nardetalia / Nardo-Galion saxatilis
# Association: Nardo-Juncetum squarrosi
# 9 releves; total species 65; mean per releve = 18.8
# Per-releve totals: 14 30 30 22 16 16 21 22 18
# Localities: 1,7 Beinn Edra; 2,3 Sgurr Mor; 3,4,6 The Storr; 5 Healavaig Bhearg; 8 Healavaig Mhor
# ---------------------------------------------------------------------------

TABLE_4_41 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_51.png",
    "table_id_raw": "Table 4.41",
    "class": "NARDO-CALLUNETEA",
    "order": "NARDETALIA",
    "alliance": "Nardo-Galion saxatilis",
    "association": "Nardo-Juncetum squarrosi",
    "n_releves": "9",
    "total_species": "65",
    "mean_species": "18.8",
    "releves": [
        releve(1, "B67-130", "433616", 1750, 270, "",  100, 4, 14),
        releve(2, "B68-105", "103660", 1900, "",  "",  100, 4, 30),
        releve(3, "B68-073", "073358", 1600, "",  "",  100, 4, 30),
        releve(4, "B68-075", "488548", 1600, "",  "",  100, 4, 22),
        releve(5, "B68-177", "023411", 1600, "",  "",  100, 4, 16),
        releve(6, "B68-126", "023411", 1000, "",  "",  100, 4, 16),
        releve(7, "B67-126", "023602", 1000, "",  "",  100, 4, 21),
        releve(8, "B68-165", "445445", 1000, "",  "",  100, 4, 22),
        releve(9, "B68-104", "445690", 1000, 135, 3,   100, 4, 18),
    ],
    "species": [
        sp("Calluna vulgaris",           ". 2 4 . . . 2 2 .",   "III", "1.1"),
        sp("Empetrum nigrum",            ". 1 . . . . . . .",   "I",   "0.7"),
        sp("Vaccinium myrtillus",        ". . 3 . . . . . .",   "I",   "0.8", True, "sparse"),
        sp("Lycopodium alpinum",         ". . . . . . . . .",   "II",  "0.8", True, "sparse"),
        sp("L. selago",                  ". . . 4 . . . . .",   "II",  "0.8"),
        sp("Selaginella selaginoides",   ". 2 2 2 . . . . .",   "II",  "0.4"),
        sp("Agrostis tenuis",            "3 5 3 . 3 . . . .",   "III", "1.6"),
        sp("Anthoxanthum odoratum",      ". . . . . . . . .",   "I",   "0.6", True, "sparse"),
        sp("Deschampsia flexuosa",       ". 3 3 3 . . . 3 .",   "III", "1.1"),
        sp("Festuca ovina",              ". . . . . . . . .",   "I",   "0.6", True, "sparse"),
        sp("Molinia caerulea",           ". . . . . . . . .",   "I",   "0.6", True, "sparse"),
        sp("Nardus stricta",             "8 8 8 7 8 4 3 5 .",   "V",   "5.7"),
        sp("Carex bigelowii",            ". . . . . . . . .",   "II",  "1.0", True, "sparse"),
        sp("C. echinata",               ". . 3 . . . . . .",   "I",   "0.4"),
        sp("C. panicea",                ". 3 . . . . . . .",   "I",   "0.7"),
        sp("C. pilulifera",             ". . . . . 1 . . .",   "I",   "0.4"),
        sp("Eriophorum angustifolium",  ". . . . . 2 . . .",   "I",   "0.4"),
        sp("Juncus kochii",             ". . . . . . . . 2",   "I",   "0.4"),
        sp("J. squarrosus",             ". 5 6 7 7 8 8 8 6",   "V",   "6.6"),
        sp("Galium saxatile",           "3 + 3 4 1 4 3 4 3",   "V",   "0.6"),
        sp("Polygala serpyllifolia",    ". . . . . . . . .",   "I",   "0.6", True, "sparse"),
        sp("Potentilla erecta",         ". 5 . 4 . . . . 2",   "III", "2.0"),
        sp("Thymus drucei",             ". . . . . . . . .",   "I",   "0.6", True, "sparse"),
        sp("Viola palustris",           ". . . . . . . . .",   "I",   "0.6", True, "sparse"),
        sp("V. riviniana",              ". . . . . . . . 1",   "I",   "0.6"),
        sp("Hylocomium splendens",      "2 4 3 4 . . . . .",   "III", "1.6"),
        sp("Polytrichum alpinum",       ". . . . . . . . .",   "I",   "0.6", True, "sparse"),
        sp("Rhacomitrium lanuginosum",  ". 2 . 6 2 8 4 . .",   "IV",  "3.1"),
        sp("Rhytidiadelphus loreus",    ". 4 . 4 . . . . .",   "II",  "1.3"),
        sp("Sphagnum capillaeum",       ". . . . 4 3 3 3 3",   "III", "3.1"),
        sp("S. papillosum",             ". 3 . 3 . 8 4 7 7",   "IV",  "3.6"),
        sp("S. plumulosum",             ". . . . . . . . .",   "I",   "0.6", True, "sparse"),
        sp("Thuidium tamariscinum",     ". . 3 . . . . . .",   "I",   "0.7"),
        sp("Cladonia uncialis",         ". . . . . . . . .",   "II",  "0.6", True, "sparse"),
        # Additional species
        sparse_sp("Festuca ovina",       9, {1: "3"}),
        sparse_sp("Cerastium holosteoides", 9, {2: "+"}),
        sparse_sp("Alchemilla alpina",   9, {2: "+"}),
        sparse_sp("Taraxacum officinale agg.", 9, {2: "1"}),
        sparse_sp("Campanula rotundifolia", 9, {3: "1"}),
        sparse_sp("Gentianella campestris", 9, {4: "1"}),
        sparse_sp("Crepis paludosa",     9, {4: "1"}),
        sparse_sp("Breutelia chrysocooma", 9, {4: "+"}),
        sparse_sp("Cladonia arbuscula",  9, {5: "1"}),
        sparse_sp("Pseudoscleropodium purum", 9, {5: "3"}),
        sparse_sp("Frullania tamarisci", 9, {5: "+"}),
        sparse_sp("Campylopus flexuosus", 9, {6: "+"}),
        sparse_sp("Calypogeia muellerana", 9, {6: "+"}),
        sparse_sp("Lepidozia reptans",   9, {6: "1"}),
        sparse_sp("L. sylvatica",        9, {7: "1"}),
        sparse_sp("Pinguicula vulgaris", 9, {7: "+"}),
        sparse_sp("Equisetum palustre",  9, {8: "1"}),
        sparse_sp("Calamagrostis epigejos", 9, {8: "1"}),
        sparse_sp("Campylopus introflexus", 9, {9: "1"}),
        sparse_sp("Sphagnum recurvum",   9, {9: "2"}),
        sparse_sp("Pinguicula vulgaris", 9, {9: "1"}),
    ],
}


# ---------------------------------------------------------------------------
# TABLE 4.42  (image 52)
# NARDO-CALLUNETEA / Calluno-Ulicetalia / Ericion cinereae
# Association: Callunetum vulgaris
# 8 releves; total species 47; mean per releve = 17.2
# Per-releve totals: 11 11 20 21 19 23 16 17
# Localities: 1 Slat Bheinn; 2 Fiskavaig; 3 Coirenche; 4 Glen Varragill; 5 Loch Sligachan;
#             6 Beinn a' Mhadaidh; 7 Dunvegan Head; 8 Sgurr na Coinnich
# ---------------------------------------------------------------------------

TABLE_4_42 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_52.png",
    "table_id_raw": "Table 4.42",
    "class": "NARDO-CALLUNETEA",
    "order": "CALLUNO-ULICETALIA",
    "alliance": "Ericion cinereae",
    "association": "Callunetum vulgaris",
    "n_releves": "8",
    "total_species": "47",
    "mean_species": "17.2",
    "releves": [
        releve(1, "B67-081", "544185", 80,  135, 20, 100, 4, 11),
        releve(2, "B67-031", "312336", 250, 0,   5,  100, 4, 11),
        releve(3, "B67-868", "446257", 250, 270, 15, 100, 4, 20),
        releve(4, "B68-054", "468341", 250, 270, 10, 100, 4, 21),
        releve(5, "B68-059", "495417", 255, 135, 15, 100, 4, 19),
        releve(6, "B68-468", "399564", 415, 135, 50, 100, 4, 23),
        releve(7, "B68-115", "176318", 500, 45,  20, 100, 4, 16),
        releve(8, "B67-099", "757213", 100, 225, 10, 85,  4, 17),
    ],
    "species": [
        sp("Erica cinerea",             "3 . 2 5 4 6 7 .",   "IV",  "4.1"),
        sp("Calluna vulgaris",          "8 9 8 8 9 8 8 8",   "V",   "8.3"),
        sp("Blechnum spicant",          "3 . . . . . . .",   "I",   "1.4"),
        sp("Agrostis canina",           "2 . . . . 1 . .",   "II",  "0.4"),
        sp("A. tenuis",                 ". . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Deschampsia flexuosa",      "3 1 2 . 3 3 4 2",   "V",   "1.9"),
        sp("Festuca ovina",             ". . . . 2 2 . .",   "II",  "0.8"),
        sp("Molinia caerulea",          ". . . . 4 5 . .",   "II",  "2.0"),
        sp("Carex bigelowii",           ". 3 1 . 3 . . +",   "III", "0.4"),
        sp("C. panicea",               ". . . 1 . 3 . .",   "II",  "0.5"),
        sp("C. pilulifera",            ". . . . . . . .",   "I",   "0.2", True, "sparse"),
        sp("Trichophorum cespitosum",   ". . 1 3 . . 3 .",   "II",  "0.6"),
        sp("Galium saxatile",           "3 . 3 4 1 4 3 4",   "IV",  "2.0"),
        sp("Lotus corniculatus",        ". . 3 3 2 . . .",   "III", "1.0"),
        sp("Polygala serpyllifolia",    ". . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Potentilla erecta",         ". . . 4 4 4 2 .",   "III", "3.0"),
        sp("Succisa pratensis",         ". 2 2 . . . . .",   "II",  "0.8"),
        sp("Viola palustris",           ". . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Breutelia chrysocooma",     ". . . . 4 . . .",   "I",   "0.8"),
        sp("Dicranodontium sp.",        ". . . . . 2 4 .",   "II",  "0.7"),
        sp("*Hypnum cupressiforme",     "5 3 3 4 3 4 3 .",   "V",   "2.9"),
        sp("Pleurozium schreberi",      ". . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Rhacomitrium lanuginosum",  "4 1 1 3 . 4 7 7",   "V",   "3.5"),
        sp("Rhytidiadelphus loreus",    "3 . . . . . 3 .",   "II",  "1.3"),
        sp("Sphagnum capillaeum",       ". . . . . 4 3 3",   "III", "3.6"),
        sp("S. papillosum",            ". . . . . . 4 .",   "I",   "0.8"),
        sp("Thuidium tamariscinum",     ". . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Cladonia arbuscula",        "4 2 . . . . 2 .",   "III", "0.5"),
        sp("C. coccifera",             ". . . . . . 2 .",   "I",   "0.4"),
        sp("C. uncialis",              ". . . . . . . .",   "I",   "0.1", True, "sparse"),
        # Additional species
        sparse_sp("Pteridium aquilinum",  8, {2: "2"}),
        sparse_sp("Thelypteris limbosperma", 8, {2: "2"}),
        sparse_sp("Nardostachys jatamansi", 8, {3: "1"}),
        sparse_sp("Veronica officinalis", 8, {3: "2"}),
        sparse_sp("Dactylorhiza maculata", 8, {3: "+"}),
        sparse_sp("Antennaria dioica",    8, {3: "3"}),
        sparse_sp("Cladonia bellidiflora", 8, {4: "1"}),
        sparse_sp("Lycopodium elevation", 8, {7: "1"}),
        sparse_sp("Pseudoscleropodium purum", 8, {7: "3"}),
        sparse_sp("Robus saxatilis",      8, {8: "1"}),
        sparse_sp("Cladonia pyxidata",    8, {8: "1"}),
        sparse_sp("Vaccinium myrtillus",  8, {8: "1"}),
        sparse_sp("Cladonia crispata",    8, {8: "+"}),
    ],
}


# ---------------------------------------------------------------------------
# TABLE 4.43  (images 53 & 54)
# NARDO-CALLUNETEA / Calluno-Ulicetalia / Ericion cinereae
# Calluna vulgaris-Sieglingia decumbens (releves 1-10)
# Calluna vulgaris-Arctostaphylus uva-ursi nodum (releves 11-14)
# 14 releves; total species 106; mean per releve = 33.5 (assoc) / 34.0 (nodum)
# Per-releve totals: 32 39 43 44 29 29 38 37 22 26  21 22 33 30
# ---------------------------------------------------------------------------

_R43 = [
    releve(1,  "B67-416", "416405", 180, 180, 30, 100, 4, 32),
    releve(2,  "B68-353", "353353", 750, 130, 20, 100, 4, 39),
    releve(3,  "B68-353", "353353", 800, 130, 20, 100, 4, 43),
    releve(4,  "B68-353", "353353", 800, 130, 10, 100, 4, 44),
    releve(5,  "B68-630", "630635", 650, 270, 20, 100, 4, 29),
    releve(6,  "B68-563", "563605", 630, 270, 5,  100, 4, 29),
    releve(7,  "B68-605", "605605", 600, 270, 5,  100, 4, 38),
    releve(8,  "B68-635", "635187", 700, 270, 5,  100, 4, 37),
    releve(9,  "B68-187", "187187", 700, 270, 25, 100, 4, 22),
    releve(10, "B68-187", "187187", 700, 270, 5,  100, 4, 26),
    releve(11, "B68-167", "611617", 1300, "", "",  100, 4, 21),
    releve(12, "B68-568", "617617", 1400, "", "",  100, 4, 22),
    releve(13, "B68-560", "617617", 1400, "", "",  100, 4, 33),
    releve(14, "B68-561", "611617", 1500, "", "",  100, 4, 30),
]

TABLE_4_43 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_53.png",
    "table_id_raw": "Table 4.43",
    "class": "NARDO-CALLUNETEA",
    "order": "CALLUNO-ULICETALIA",
    "alliance": "Ericion cinereae",
    "association": "Calluna vulgaris-Sieglingia decumbens",
    "n_releves": "14",
    "total_species": "",
    "mean_species": "",
    "releves": _R43,
    "species": [
        sp("Arctostaphylus uva-ursi",   ". . . . . . . . . . 5 7 6 4",  "II",  "0.4"),
        sp("Empetrum nigrum",           "2 5 5 4 6 5 7 8 2 . . . . .",  "V",   "4.8"),
        sp("Erica cinerea",             ". . . . . . . . . . . . . .",  "II",  "0.4", True, "sparse"),
        sp("Calluna vulgaris",          "7 8 7 8 8 8 8 7 6 7 . . . .",  "V",   "7.6"),
        sp("Juniperus communis ssp. nana", ". . . . . . . . . . 3 5 6 3", "II", "0.5"),
        sp("Lonicera periclymenum",     ". . . . . . . . . . . . . .",  "I",   "0.1", True, "sparse"),
        sp("*Salix repens",             ". . . . . . . . . . . . . .",  "I",   "0.1", True, "sparse"),
        sp("Blechnum spicant",          ". 4 3 3 . 4 . . . . . . . .",  "III", "1.3"),
        sp("Pteridium aquilinum",       ". . . . . . . . . . . 2 . .",  "I",   "0.1"),
        sp("Agrostis canina",           "4 4 3 4 4 4 4 . 3 3 3 3 3 4",  "V",   "3.2"),
        sp("Anthoxanthum odoratum",     ". . . . . . . . . . . . . .",  "I",   "0.1", True, "sparse"),
        sp("Deschampsia flexuosa",      "2 . 3 3 4 3 2 4 4 2 3 2 3 3",  "V",   "2.8",
           True, "cells approximate image 53"),
        sp("Festuca ovina",             ". . . . . . . . . . . . . .",  "I",   "0.1", True, "sparse"),
        sp("F. rubra",                  ". . . . . . . . . . . . . .",  "I",   "0.1", True, "sparse"),
        sp("F. vivipara",               ". . . . . . . . . . . . . .",  "I",   "0.1", True, "sparse"),
        sp("Holcus lanatus",            ". . . . . . . . . . . . . .",  "I",   "0.1", True, "sparse"),
        sp("Molinia caerulea",          "3 . 4 1 . . . . . . 3 . . .",  "II",  "0.5"),
        sp("Nardus stricta",            ". . . . . . . . . . . . . .",  "I",   "0.1", True, "sparse"),
        sp("Carex bigelowii",           ". . . . . . . . . . . . . .",  "I",   "0.1", True, "sparse"),
        sp("C. panicea",               ". 2 . . 2 . . . . . . . . .",  "II",  "0.4"),
        sp("C. pilulifera",            "3 . . 3 . . . 2 . . . . . .",  "II",  "0.5"),
        sp("Dactylorchis maculata",    "2 2 . . 3 . . 3 . . . . . .",  "II",  "0.5"),
        sp("Luzula campestris",         "2 2 1 2 . . 1 . . . . . . .",  "III", "0.8"),
        sp("Trichophorum cespitosum",   ". . . . . . 4 . . . . . . .",  "I",   "0.5"),
        sp("Achillea millefolium",      ". . . . . . . . . . . . . .",  "I",   "0.2", True, "sparse"),
        sp("Alchemilla xanthochlora",   ". . . 2 . . . . . . . . . .",  "I",   "0.4"),
        sp("Antennaria dioica",         ". . 3 3 2 . 3 . . . . . 2 3",  "III", "1.0"),
        sp("Andyllis vulneraria",       ". . . . . 3 . . . . . . . .",  "I",   "0.4"),
        sp("Bellis perennis",           ". . . . . . . . . . . . . .",  "I",   "0.2", True, "sparse"),
        sp("Carlina vulgaris",          ". . . . . . . . . . . . . .",  "I",   "0.3"),
        sp("Cerastium holosteoides",    ". 2 1 . . . . . . . . . . .",  "II",  "0.3"),
        sp("Euphrasia micrantha",       ". 3 2 2 1 2 3 2 . . . 1 . .",  "IV",  "1.7"),
        sp("Galium saxatile",           "1 . . . 2 . . 2 . . . . 3 .",  "II",  "0.8"),
        sp("Hieracium pilosella",       "1 . . . . . . . . . . . . .",  "I",   "0.3"),
    ],
}

TABLE_4_43_CONT = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_54.png",
    "table_id_raw": "Table 4.43",
    "class": "NARDO-CALLUNETEA",
    "order": "CALLUNO-ULICETALIA",
    "alliance": "Ericion cinereae",
    "association": "Calluna vulgaris-Sieglingia decumbens",
    "n_releves": "14",
    "total_species": "106",
    "mean_species": "33.5",
    "releves": _R43,
    "species": [
        sp("Hypericum pulchrum",        "3 2 3 2 . . . . . . . . . .",  "III", "1.5"),
        sp("Lathyrus montanus",         "3 3 2 . . . . . . . . 2 2 .",  "III", "1.0"),
        sp("Linum catharticum",         ". . . . . . . 1 . . . . . .",  "I",   "0.3"),
        sp("Lotus corniculatus",        ". . 3 3 2 . . . . . . . . .",  "II",  "0.9"),
        sp("Lysimachia nemorum",        ". . . . . . . . . . . . . .",  "I",   "0.1", True, "sparse"),
        sp("Pinguicula vulgaris",       ". . . . . . . . . . . . . .",  "I",   "0.3"),
        sp("Plantago lanceolata",       "1 . . . . . . . . . . . . .",  "I",   "0.3"),
        sp("P. maritima",               ". . . . . . . . . . . . . .",  "I",   "0.3", True, "sparse"),
        sp("Polygala serpyllifolia",    ". . . . . . . 1 . . . . . .",  "I",   "0.3"),
        sp("Potentilla erecta",         "3 . . . . 1 . . . . . . . .",  "I",   "0.3"),
        sp("Primula vulgaris",          ". . . . . . . . . . . . . .",  "I",   "0.6"),
        sp("Prunella vulgaris",         ". 2 1 3 . . . . . . . 2 2 1",  "II",  "0.6"),
        sp("Ranunculus acris",          ". 1 . . . . . . . . . . . .",  "I",   "1.3"),
        sp("Rumex acetosa",             "3 . . . . . . . . . . . . .",  "I",   "0.2"),
        sp("Solidago virgaurea",        ". 1 . . . 4 4 . . . . . . .",  "II",  "1.3"),
        sp("Succisa pratensis",         "3 1 . . . . . . . 2 . . . .",  "II",  "0.8"),
        sp("Taraxacum officinale agg.", ". 2 . . . . . . . . . . . .",  "I",   "0.2"),
        sp("Teucrium scordonia",        ". . 1 . . . . . . . . . . .",  "I",   "0.2"),
        sp("Thymus drucei",             "3 3 1 2 . . 2 5 1 . 4 3 . 3",  "IV",  "2.4"),
        sp("Trifolium repens",          ". . . . . . . . . . . . . .",  "I",   "0.6"),
        sp("Viola riviniana",           "2 . 3 2 . . 2 . 3 2 . . . .",  "III", "1.5"),
        sp("Breutelia chrysocooma",     "3 3 4 3 . . . . . . . . . .",  "III", "1.6"),
        sp("Dicranodontium scoparium",  "4 2 . . . . . . 3 2 . 4 . .",  "III", "2.1"),
        sp("Hylocomium splendens",      ". . 2 . . . 3 3 . . . . . .",  "II",  "1.2"),
        sp("Hylocomium brevirostre",    ". . . . . . . . . . . . . .",  "I",   "0.1", True, "sparse"),
        sp("*Hypnum cupressiforme",     ". 4 2 4 . . . . . . . . . .",  "II",  "1.1"),
        sp("Isothecium myosuroides",    ". . . . . . . . . . . . . .",  "I",   "0.1", True, "sparse"),
        sp("Mnium hornum",              ". 2 . . . . . 1 . . . . . .",  "I",   "0.6"),
        sp("Plagiochilum undulatum",    ". . . . . . . . . . . . . .",  "I",   "0.4"),
        sp("Pleurozium schreberi",      ". . 2 . . 3 . 3 . . . . . .",  "II",  "0.5"),
        sp("Pseudoscleropodium purum",  ". . . . . . . . . . . . . .",  "I",   "0.1", True, "sparse"),
        sp("Rhacomitrium lanuginosum",  "4 . . . . . . . . . . . . .",  "I",   "0.5"),
        sp("R. triquetrum",             ". . . . . . . . . . . . . .",  "I",   "0.3"),
        sp("Rhytidiadelphus loreus",    ". . . . . 3 5 . . . . . . .",  "II",  "0.8"),
        sp("R. squarrosus",             "2 3 5 3 . . . . . . . . . .",  "II",  "2.0"),
        sp("Thuidium tamariscinum",     ". 4 . . . 4 4 4 . . 3 . . .",  "III", "1.7"),
        sp("Frullania fragilifolia",    ". . . . . . . . . . . . . .",  "I",   "0.1", True, "sparse"),
        sp("F. tamarisci",             ". . . . . . . . . . . . . .",  "I",   "0.1", True, "sparse"),
        sp("Scapania gracilis",         ". . . . . . . . . . . . . .",  "I",   "0.1", True, "sparse"),
        sp("Trichocolea tomentella",    ". . . . . . . . . . . . . .",  "I",   "0.1", True, "sparse"),
    ],
}


# ---------------------------------------------------------------------------
# TABLE 4.44  (images 55 & 56)
# NARDO-CALLUNETEA / Calluno-Ulicetalia / Myrtillion Boreale
# Association: Vaccineto-Callunetum hepaticosum
# 6 releves; total species 86; mean per releve = 41.5
# Per-releve totals: 46 43 40 42 40 36
# ---------------------------------------------------------------------------

_R44 = [
    releve(1, "B68-005", "413762", 150,  45, 30, 90,  4, 46),
    releve(2, "B68-006", "414761", 150,  45, 30, 100, 4, 43),
    releve(3, "B68-233", "553215", 450,  45, 45, 100, 4, 40),
    releve(4, "B67-013", "552214", 500,  0,  45, 100, 4, 42),
    releve(5, "B68-120", "494531", 1100, 0,  40, 100, 4, 40),
    releve(6, "B68-121", "494531", 1100, 0,  40, 100, 4, 36),
]

TABLE_4_44 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_55.png",
    "table_id_raw": "Table 4.44",
    "class": "NARDO-CALLUNETEA",
    "order": "CALLUNO-ULICETALIA",
    "alliance": "Myrtillion Boreale",
    "association": "Vaccineto-Callunetum hepaticosum",
    "n_releves": "6",
    "total_species": "",
    "mean_species": "",
    "releves": _R44,
    "species": [
        sp("Erica cinerea",             "2 2 . . 4 3",   "IV",  "1.8"),
        sp("Calluna vulgaris",          "8 8 8 8 8 8",   "V",   "8.0"),
        sp("Lonicera periclymenum",     "1 + . . . .",   "II",  "0.3"),
        sp("Vaccinium myrtillus",       ". 3 4 3 4 4",   "V",   "3.0"),
        sp("Blechnum spicant",          "3 2 4 3 4 4",   "V",   "3.3"),
        sp("Dryopteris filix-mas",      "1 2 . . . 3",   "III", "1.0"),
        sp("Hymenophyllum wilsonii",    "+ 1 3 + . 1",   "V",   "1.2"),
        sp("Thelypteris limbosperma",   ". . . 2 2 .",   "II",  "0.7"),
        sp("Agrostis tenuis",           ". . 3 1 . .",   "II",  "0.7"),
        sp("Deschampsia flexuosa",      "1 3 . . 2 3",   "IV",  "1.5"),
        sp("Festuca vivipara",          ". . 2 2 + .",   "III", "0.8"),
        sp("Molinia caerulea",          ". . 3 4 . .",   "II",  "1.2"),
        sp("Carex binervis",            "1 2 . . 1 2",   "IV",  "1.0"),
        sp("*Dactylorchis maculata",    ". 1 . . 1 .",   "II",  "0.3"),
        sp("Luzula sylvatica",          "2 2 . . . .",   "II",  "0.7"),
        sp("Trichophorum cespitosum",   ". 3 . . 1 1",   "III", "0.8"),
        sp("Euphrasia micrantha",       "+ . 1 . . .",   "II",  "0.3"),
        sp("Galium saxatile",           ". . . 2 3 2",   "III", "1.2"),
        sp("Hypericum pulchrum",        "2 3 3 . . .",   "III", "1.3"),
        sp("Pinguicula vulgaris",       "1 2 . . . .",   "II",  "0.5"),
        sp("Potentilla erecta",         "3 3 4 2 3 3",   "V",   "3.0"),
        sp("Succisa pratensis",         ". 1 2 . 2 .",   "III", "0.8"),
        sp("Viola riviniana",           ". 1 . . . 2",   "II",  "0.5"),
        sp("Breutelia chrysocooma",     "2 4 4 . 4 .",   "IV",  "2.3"),
        sp("Campylopus atrovirens",     "1 1 1 3 1 .",   "V",   "1.2"),
        sp("C. flexuosus",             "1 1 . . . .",   "II",  "0.3"),
        sp("C. setifolius",            ". . 2 . 1 .",   "II",  "0.5"),
        sp("Dicranum scoparium",        "2 . . 3 1 .",   "III", "1.0"),
        sp("D. majus",                 ". . 1 2 . .",   "II",  "0.5"),
    ],
}

TABLE_4_44_CONT = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_56.png",
    "table_id_raw": "Table 4.44",
    "class": "NARDO-CALLUNETEA",
    "order": "CALLUNO-ULICETALIA",
    "alliance": "Myrtillion Boreale",
    "association": "Vaccineto-Callunetum hepaticosum",
    "n_releves": "6",
    "total_species": "86",
    "mean_species": "41.5",
    "releves": _R44,
    "species": [
        sp("Dicranodontium uncinatum",  ". . 2 . . .",   "II",  "0.5"),
        sp("Hookeria lucens",           ". . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Hylocomium splendens",      "4 1 2 3 . .",   "IV",  "1.7"),
        sp("H. umbratum",              ". . . . . .",   "I",   "0.1", True, "sparse"),
        sp("†Hypnum cupressiforme",     "1 . 1 1 . 2",   "III", "0.3"),
        sp("Isothecium myosuroides",    ". 2 . 1 2 3",   "III", "1.3"),
        sp("Mnium hornum",             ". . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Plagiochilum undulatum",    "3 . 1 . 1 .",   "III", "1.2"),
        sp("Plilium crista-castrensis", "2 . . 3 . .",   "II",  "1.0"),
        sp("Pleurozium schreberi",      "3 2 . 2 . .",   "III", "0.5"),
        sp("Rhacomitrium lanuginosum",  "1 2 5 4 7 7",   "V",   "4.3"),
        sp("Rhytidiadelphus loreus",    "3 2 3 1 3 4",   "V",   "2.7"),
        sp("Sphagnum capillaeum",       "2 3 5 5 2 5",   "V",   "3.7"),
        sp("S. quinquefarium",         "2 5 . 5 . 2",   "IV",  "2.3"),
        sp("†S. subsecundum",          "2 . . . . .",   "I",   "0.3"),
        sp("S. tenellum",              ". 4 1 . 2 .",   "III", "1.2"),
        sp("Thuidium tamariscinum",     ". . 3 . 2 .",   "II",  "0.8"),
        sp("Cladonia uncialis",         ". . . . . .",   "II",  "0.6", True, "sparse"),
        sp("Anastrepta orcadensis",     "+ . 2 2 . .",   "III", "1.2"),
        sp("Bazzania tricrenata",       ". 2 . 4 . 3",   "III", "2.2"),
        sp("Calypogeia muellerana",     ". 4 5 3 . .",   "III", "2.2"),
        sp("Cephalozia bicuspidata",    ". . 1 . . .",   "I",   "0.3"),
        sp("Diplophyllum albicans",     "4 5 3 1 2 4",   "V",   "3.3"),
        sp("Frullania tamarisci",       ". . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Lepidozia reptans",         "3 . . + . .",   "II",  "0.7"),
        sp("L. tricodes",              ". . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Mastigophora woodsii",      ". . 4 6 4 3",   "III", "2.3"),
        sp("Mylia taylori",            "3 . 4 4 3 .",   "IV",  "2.3"),
        sp("Pellia epiphylla",         ". . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Plagiochila spinulosa",     "3 . 3 1 4 3",   "IV",  "2.4"),
        sp("Pleurozia purpurea",        ". 2 3 . . .",   "II",  "1.2"),
        sp("Scapania gracilis",         "2 3 . 3 3 3",   "IV",  "2.3"),
        sp("S. ornithopodioides",      ". . . . . .",   "I",   "0.1", True, "sparse"),
        # Additional species
        sparse_sp("Juniperus communis ssp. nana", 6, {1: "+"}),
        sparse_sp("Pteridium aquilinum",  6, {1: "2"}),
        sparse_sp("Sphagnum robustum",    6, {1: "1"}),
        sparse_sp("Riccardia sinuata",    6, {1: "1"}),
        sparse_sp("Sedum rosea",          6, {2: "1"}),
        sparse_sp("Myriophyllum alterniflorum", 6, {2: "3"}),
        sparse_sp("Caltha palustris",     6, {3: "4"}),
        sparse_sp("Herberta adunca",      6, {3: "+"}),
        sparse_sp("Cladonia bellidiflora", 6, {4: "+"}),
        sparse_sp("Hylocomium flagellare", 6, {5: "1"}),
        sparse_sp("Herberta adunca",      6, {5: "3"}),
        sparse_sp("Dryopteris borreri",   6, {6: "1"}),
        sparse_sp("Sphagnum plumulosum",  6, {6: "+"}),
        sparse_sp("Marchantia marginata", 6, {6: "1"}),
    ],
}


# ---------------------------------------------------------------------------
# TABLE 4.39  (image 57)
# NOTE: printed on p. 130, after Tables 4.41–4.44 in scan order.
# SALICETEA HERBACEAE / Deschampsieto-Myrtilletalia / Nardeto-Caricion bigelowii
# Association: Nardus stricta-Vaccinium myrtillus
# 11 releves; Typicum (1-9), Vaccinium-rich (10-11)
# Total species 54; mean per releve = 18.5
# Per-releve totals: 18 18 18 13 15 17 21 17 19 21 24
# ---------------------------------------------------------------------------

TABLE_4_39 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_57.png",
    "table_id_raw": "Table 4.39",
    "class": "SALICETEA HERBACEAE",
    "order": "DESCHAMPSIETO-MYRTILLETALIA",
    "alliance": "Nardeto-Caricion bigelowii",
    "association": "Nardus stricta-Vaccinium myrtillus",
    "n_releves": "11",
    "total_species": "54",
    "mean_species": "18.5",
    "releves": [
        releve(1,  "B68-336", "505811", 1800, 45,  3,   100, 4, 18),
        releve(2,  "B67-001", "501811", 1900, 45,  "",  100, 4, 18),
        releve(3,  "B68-001", "501811", 1900, 45,  "",  100, 4, 18),
        releve(4,  "B68-943", "811811", 1850, 0,   "",  100, 4, 13),
        releve(5,  "B68-244", "219219", 1900, 0,   5,   100, 4, 15),
        releve(6,  "B68-082", "811811", 2000, 0,   "",  100, 4, 17),
        releve(7,  "B68-083", "811811", 2000, 0,   "",  100, 4, 21),
        releve(8,  "B68-069", "548548", 1850, 0,   5,   100, 4, 17),
        releve(9,  "B68-067", "548223", 2250, 315, "",  100, 4, 19),
        releve(10, "B67-066", "223223", 2300, 315, "",  100, 4, 21),
        releve(11, "B68-066", "223223", 2300, 315, "",  100, 4, 24),
    ],
    "species": [
        sp("Calluna vulgaris",          "1 2 + . . . . . . . .",   "III", "0.8"),
        sp("Empetrum hermaphroditum",   ". . . . . . . . . . .",   "III", "0.5", True, "sparse"),
        sp("Vaccinium myrtillus",       ". . . . . 2 3 . . 4 8",  "V",   "3.5"),
        sp("Blechnum spicant",          ". . . 3 . . . . . . .",   "I",   "0.5"),
        sp("Lycopodium alpinum",        "4 2 3 2 3 2 . . 2 . .",   "V",   "2.3"),
        sp("L. selago",                 ". . . . 4 . . . . . .",   "I",   "0.3"),
        sp("Salix herbacea",            ". . . . . . . . . 2 3",   "II",  "1.0"),
        sp("Agrostis tenuis",           "3 . . . . . . . . . .",   "II",  "1.0"),
        sp("Deschampsia flexuosa",      ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Festuca ovina",             ". . . . . . . . . . .",   "I",   "0.5", True, "sparse"),
        sp("F. vivipara",               ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("F. hisupina",              ". . . . . . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Nardus stricta",            "8 9 8 7 9 8 8 6 4 4 4",   "V",   "7.3"),
        sp("Carex bigelowii",           ". 3 . . . . . . . . .",   "II",  "1.0"),
        sp("C. pilulifera",            "3 . . . . . . . . . .",   "I",   "1.4"),
        sp("Luzula alpina",             ". . . . . . . . . . .",   "I",   "0.5", True, "sparse"),
        sp("Alchemilla alpina",         ". . . . . . . . . . .",   "II",  "0.7", True, "sparse"),
        sp("Galium saxatile",           "4 2 4 4 6 4 2 . . . .",   "V",   "3.0"),
        sp("Polygala serpyllifolia",    ". . . . . . . . . . .",   "I",   "0.5", True, "sparse"),
        sp("Potentilla erecta",         "5 1 . 4 . . 4 . . . .",   "V",   "1.5"),
        sp("Thymus drucei",             ". . . . . . . . . . .",   "I",   "0.5", True, "sparse"),
        sp("Myosotis palustris",        ". . . . . . . 2 . . .",   "I",   "0.4"),
        sp("Mnium hornum",             ". . 1 . 2 . . . . . .",   "I",   "0.4"),
        sp("Rhacomitrium lanuginosum",  "5 6 5 7 5 3 5 3 5 4 5",   "V",   "4.4"),
        sp("Rhytidiadelphus loreus",    ". . . . . . 4 3 . . .",   "I",   "3.2"),
        sp("Anastrepta orcadensis",     ". . . . . . . . . 2 3",   "II",  "0.7"),
        sp("Ptilidium ciliare",         ". 1 . . . . . . . . .",   "II",  "0.4"),
        sp("Cetraria islandica",        "2 3 2 3 4 3 2 . . 1 .",   "V",   "2.0"),
        sp("Cladonia arbuscula",        ". . . . . . . . . 2 2",   "II",  "0.3"),
        sp("C. uncialis",              ". . . . . . . . . . .",   "I",   "1.9", True, "sparse"),
        # Additional species
        sparse_sp("Trichophorum cespitosum", 11, {1: "2"}),
        sparse_sp("Sphagnum plumulosum", 11, {2: "2"}),
        sparse_sp("Rhytidiadelphus squarrosus", 11, {3: "2"}),
        sparse_sp("Anthelia julacea",    11, {3: "3"}),
        sparse_sp("Molinia caerulea",    11, {4: "2"}),
        sparse_sp("Carex panicea",       11, {4: "2"}),
        sparse_sp("Vaccinium vitis-idaea", 11, {5: "2"}),
        sparse_sp("Sphagnum tenellum",   11, {5: "2"}),
        sparse_sp("Caltha palustris",    11, {6: "2"}),
        sparse_sp("Juncus trifidus",     11, {6: "2"}),
        sparse_sp("Empetrum hermaphroditum var. micropetalum", 11, {7: "2"}),
        sparse_sp("Bartsia alpina",      11, {7: "1"}),
        sparse_sp("Hylocomium splendens", 11, {8: "1"}),
        sparse_sp("Lophocolea bidentata", 11, {9: "1"}),
        sparse_sp("Mylia taylori",       11, {9: "1"}),
        sparse_sp("Scapania gracilis",   11, {9: "1"}),
        sparse_sp("Empetrum hermaphroditum", 11, {10: "2"}),
        sparse_sp("Deschampsia cespitosa", 11, {11: "3"}),
    ],
}


# ---------------------------------------------------------------------------
# TABLE 4.45  (image 58)
# BETULO-ADENOSTYLETEA / Adenostyletalia
# Alliance: Dryoptero-Calamagrostidion purpurae
# Association: Luzula sylvatica-Vaccinium myrtillus
# 5 releves; total species 75; mean per releve = 30.4
# Per-releve totals: 41 33 34 16 26
# ---------------------------------------------------------------------------

TABLE_4_45 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_58.png",
    "table_id_raw": "Table 4.45",
    "class": "BETULO-ADENOSTYLETEA",
    "order": "ADENOSTYLETALIA",
    "alliance": "Dryoptero-Calamagrostidion purpurae",
    "association": "Luzula sylvatica-Vaccinium myrtillus",
    "n_releves": "5",
    "total_species": "75",
    "mean_species": "30.4",
    "releves": [
        releve(1, "B67-106", "106605", 250,  0,  0,  100, 2, 41),
        releve(2, "B67-094", "094334", 250,  0,  10, 100, 4, 33),
        releve(3, "B68-122", "122551", 1100, 0,  15, 100, 4, 34),
        releve(4, "B67-097", "097057", 1100, 0,  35, 100, 4, 16),
        releve(5, "B68-349", "249349", 1700, 0,  50, 100, 4, 26),
    ],
    "species": [
        sp("Calluna vulgaris",          "4 3 5 . .",   "III", "2.0"),
        sp("Vaccinium myrtillus",       "6 5 5 5 5",   "V",   "5.2"),
        sp("Blechnum spicant",          "3 3 4 . 4",   "V",   "3.3"),
        sp("Dryopteris borreri",        "1 2 . . 3",   "III", "1.6"),
        sp("D. dilatata",              "4 3 . . .",   "II",  "1.4"),
        sp("D. filix-mas",             ". 2 . . .",   "I",   "0.4"),
        sp("Hymenophyllum wilsonii",    "+ 1 3 + .",   "IV",  "1.2"),
        sp("Thelypteris dryopteris",    ". . . 1 .",   "I",   "0.3"),
        sp("T. limbosperma",           "4 6 5 . .",   "III", "3.0"),
        sp("T. phegopteris",           ". . . . .",   "I",   "0.1", True, "sparse"),
        sp("Agrostis canina",           "1 . . 4 .",   "II",  "1.0"),
        sp("Anthoxanthum odoratum",     ". 3 3 3 3",   "IV",  "2.4"),
        sp("Deschampsia flexuosa",      ". 1 2 . .",   "II",  "0.6"),
        sp("Festuca ovina",             ". . . 2 4",   "II",  "1.2"),
        sp("F. vivipara",              ". . 2 2 4",   "III", "1.6"),
        sp("Molinia caerulea",          ". . . . .",   "I",   "0.1", True, "sparse"),
        sp("Endymion non-scriptus",     ". 3 3 . .",   "II",  "1.2"),
        sp("Luzula sylvatica",          "8 3 3 9 7",   "V",   "6.0"),
        sp("Alchemilla alpina",         ". 1 2 . .",   "II",  "0.6"),
        sp("Cardamine flexuosa",        "+ . 2 1 .",   "III", "0.6"),
        sp("Digitalis purpurea",        ". . . . .",   "I",   "0.1", True, "sparse"),
        sp("Galium saxatile",           ". 4 1 . .",   "II",  "1.0"),
        sp("Hypericum pulchrum",        ". 2 1 . .",   "II",  "0.6"),
        sp("Oxalis acetosella",         ". . . 3 .",   "I",   "0.6"),
        sp("Potentilla erecta",         "3 . . 3 2",   "III", "1.6"),
        sp("Viola riviniana",           ". . . . .",   "I",   "0.1", True, "sparse"),
        sp("Breutelia chrysocooma",     "3 3 . . .",   "II",  "1.2"),
        sp("Dicranum scoparium",        ". 3 . . .",   "I",   "0.6"),
        sp("Hylocomium splendens",      "3 . 3 . .",   "II",  "1.2"),
        sp("Isothecium myosuroides",    "3 . . . .",   "I",   "0.6"),
        sp("Mnium hornum",             ". 2 1 . .",   "II",  "0.6"),
        sp("Plagiochilum undulatum",    "2 . . . .",   "I",   "0.4"),
        sp("Polytrichum formosum",      ". . . . .",   "I",   "0.1", True, "sparse"),
        sp("Rhacomitrium lanuginosum",  ". . . 4 7",   "II",  "2.2"),
        sp("Rhytidiadelphus loreus",    "5 . 4 . .",   "II",  "1.8"),
        sp("†S. subsecundum",          ". . 2 . .",   "I",   "0.4"),
        sp("Thuidium delicatulum",      "3 2 . . .",   "II",  "1.0"),
        sp("Diplophyllum albicans",     ". . . . .",   "I",   "0.1", True, "sparse"),
        sp("Scapania gracilis",         ". . . . .",   "I",   "0.1", True, "sparse"),
        # Additional species
        sparse_sp("Dryopteris aemula",    5, {1: "4"}),
        sparse_sp("Ajuga reptans",        5, {1: "2"}),
        sparse_sp("Anemone nemorosa",     5, {1: "3"}),
        sparse_sp("Hypericum androsaemum", 5, {1: "3"}),
        sparse_sp("Sphagnum quinquefarium", 5, {1: "2"}),
        sparse_sp("Luzula multiflora",    5, {2: "3"}),
        sparse_sp("Lotus corniculatus",   5, {2: "1"}),
        sparse_sp("Sedum rosea",          5, {2: "1"}),
        sparse_sp("Atrichum undulatum",   5, {2: "1"}),
        sparse_sp("Frullania tamarisci",  5, {2: "1"}),
        sparse_sp("Vaccinium vitis-idaea", 5, {3: "2"}),
        sparse_sp("Calamagrostis purpurea", 5, {4: "9"}),
        sparse_sp("Selaginella selaginoides", 5, {4: "1"}),
        sparse_sp("Salix herbacea",       5, {4: "+"}),
        sparse_sp("Sphagnum capillaeum",  5, {4: "2"}),
        sparse_sp("Crypotgamma crispa",   5, {4: "4"}),
        sparse_sp("Lophozia ventricosa",  5, {4: "1"}),
        sparse_sp("Saxifraga hypnoides",  5, {4: "5"}),
        sparse_sp("Rhacomitrium fasciculare", 5, {5: "3"}),
        sparse_sp("R. heterostichum",     5, {5: "3"}),
        sparse_sp("Herberta adunca",      5, {5: "+"}),
    ],
}


# ---------------------------------------------------------------------------
# TABLE 4.46  (images 59 & 60)
# BETULO-ADENOSTYLETEA / Adenostyletalia / Mulgedion alpini
# Association: Luzula sylvatica-Silene dioica
# 7 releves; total species 105; mean per releve = 34.0
# Per-releve totals: 27 24 24 35 34 43 31
# ---------------------------------------------------------------------------

_R46 = [
    releve(1, "B68-009", "009410", 100, 315, 0,  80,  4, 27),
    releve(2, "B68-151", "151153", 50,  0,   0,  100, 4, 24),
    releve(3, "B68-153", "153507", 50,  0,   5,  100, 4, 24),
    releve(4, "B68-308", "308797", 75,  0,   10, 100, 4, 35),
    releve(5, "B68-368", "368378", 400, 0,   0,  100, 4, 34),
    releve(6, "B67-396", "396396", 150, 10,  10, 100, 4, 43),
    releve(7, "B68-378", "378378", 350, 60,  60, 100, 4, 31),
]

TABLE_4_46 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_59.png",
    "table_id_raw": "Table 4.46",
    "class": "BETULO-ADENOSTYLETEA",
    "order": "ADENOSTYLETALIA",
    "alliance": "Mulgedion alpini",
    "association": "Luzula sylvatica-Silene dioica",
    "n_releves": "7",
    "total_species": "",
    "mean_species": "",
    "releves": _R46,
    "species": [
        sp("Calluna vulgaris",          "3 . 5 5 3 6 8",   "V",   "5.1"),
        sp("Empetrum nigrum",           "4 . . . . . .",   "II",  "0.9"),
        sp("Erica cinerea",             ". . 6 . . . .",   "II",  "1.3"),
        sp("Juniperus communis ssp. nana", ". . . . 4 . 5", "II", "1.3"),
        sp("Rubus saxatilis",           ". . . 4 3 3 .",   "III", "1.0"),
        sp("Athyrium filix-femina",     ". 6 . 3 . 4 .",   "III", "1.9"),
        sp("Dryopteris borreri",        "4 . . . . . .",   "I",   "0.9"),
        sp("Polypodium vulgare",        ". 4 4 . . . .",   "II",  "1.0"),
        sp("Thelypteris limbosperma",   ". . . 3 3 3 1",   "III", "1.5"),
        sp("T. phegopteris",           ". . . . . . .",   "I",   "0.7", True, "sparse"),
        sp("Agrostis tenuis",           ". . 3 . 3 . 1",   "II",  "0.6"),
        sp("Arrhenatherum elatius",     ". 3 . 3 . . .",   "II",  "0.9"),
        sp("Deschampsia flexuosa",      ". . . . . . .",   "I",   "0.9", True, "sparse"),
        sp("Festuca ovina",             "6 . 4 5 3 3 3",   "V",   "3.4"),
        sp("F. vivipara",              ". . . . . . .",   "II",  "0.5", True, "sparse"),
        sp("Holcus lanatus",            "4 4 . . . . .",   "II",  "1.4"),
        sp("Carex bigelowii",           "2 4 . 1 . . 2",   "III", "0.7"),
        sp("C. pulicaris",             ". . . 2 . . .",   "I",   "0.3"),
        sp("Endymion non-scriptus",     ". 2 3 4 5 6 3",   "V",   "3.3"),
        sp("Luzula sylvatica",          "5 7 5 3 4 6 5",   "V",   "5.9"),
        sp("Orchis mascula",            ". . . . . + .",   "I",   "0.3"),
        sp("Angelica sylvestris",       "3 7 2 . 2 3 3",   "V",   "2.9"),
        sp("Armeria maritima",          ". . . . . . .",   "I",   "0.5", True, "sparse"),
        sp("Centaurea nigra",           ". . . . . . .",   "I",   "0.5", True, "sparse"),
        sp("Cirsium heterophyllum",     ". 3 1 . . 3 .",   "III", "0.6"),
        sp("Digitalis purpurea",        ". . . . . . .",   "I",   "0.3", True, "sparse"),
        sp("Epilobium montanum",        "2 3 . . 3 . .",   "III", "0.9"),
        sp("Filipendula ulmaria",       ". 4 4 . 4 . .",   "III", "2.3"),
        sp("Galium saxatile",           ". . . . . 2 .",   "II",  "0.6"),
    ],
}

TABLE_4_46_CONT = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_60.png",
    "table_id_raw": "Table 4.46",
    "class": "BETULO-ADENOSTYLETEA",
    "order": "ADENOSTYLETALIA",
    "alliance": "Mulgedion alpini",
    "association": "Luzula sylvatica-Silene dioica",
    "n_releves": "7",
    "total_species": "105",
    "mean_species": "34.0",
    "releves": _R46,
    "species": [
        sp("Geum rivale",               ". . . 4 2 . .",   "III", "1.1"),
        sp("Hypericum pulchrum",        "1 . . . . . 3",   "II",  "1.1"),
        sp("Lathyrus montanus",         "3 3 . . 2 . 1",   "III", "1.0"),
        sp("Lotus corniculatus",        ". . . . . . .",   "I",   "0.3", True, "sparse"),
        sp("Plantago lanceolata",       "1 . + . . . .",   "II",  "0.3"),
        sp("Polygala serpyllifolia",    ". . . . . . .",   "I",   "0.3", True, "sparse"),
        sp("Potentilla erecta",         "3 1 . 1 . 3 .",   "III", "1.4"),
        sp("Primula vulgaris",          ". . . . . . .",   "I",   "0.3", True, "sparse"),
        sp("Prunella vulgaris",         ". 3 3 . . . .",   "II",  "0.9"),
        sp("Rumex acetosa",             "3 4 4 3 5 3 .",   "V",   "2.9"),
        sp("Sedum rosea",               "3 4 4 . 3 5 3",   "V",   "2.9"),
        sp("Silene dioica",             "3 4 4 3 5 6 4",   "V",   "4.4"),
        sp("Solidago virgaurea",        ". 2 . . . . .",   "I",   "0.9"),
        sp("Succisa pratensis",         ". . . . . . .",   "I",   "0.3", True, "sparse"),
        sp("Teucrium scordonia",        ". . . 1 2 . .",   "II",  "1.3"),
        sp("Thymus drucei",             ". . 3 . . . .",   "II",  "0.7"),
        sp("Trifolium repens",          ". 4 . . . . .",   "I",   "0.8"),
        sp("Valeriana officinalis",     ". . 5 4 2 + .",   "III", "1.7"),
        sp("Veronica serpyllifolia",    ". . . . . . .",   "I",   "0.3", True, "sparse"),
        sp("Viola riviniana",           "4 3 . 2 3 . .",   "III", "1.0"),
        sp("Breutelia chrysocooma",     "3 3 4 3 . 2 .",   "IV",  "1.1"),
        sp("Dicranodontium sp.",        ". . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Hylocomium brevirostre",    ". 3 . . . . .",   "I",   "0.9"),
        sp("H. splendens",             ". . . . . . .",   "I",   "0.3", True, "sparse"),
        sp("*Hypnum cupressiforme",     ". . . . . 1 .",   "II",  "0.9"),
        sp("Isothecium myosuroides",    ". . . . . 3 .",   "II",  "0.5"),
        sp("Mnium hornum",             ". . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Plagiochilum undulatum",    "2 . . . . . .",   "I",   "0.4"),
        sp("Pleurozium schreberi",      ". . 2 3 . . .",   "II",  "0.5"),
        sp("Pseudoscleropodium purum",  ". 2 . 3 . . .",   "II",  "0.3"),
        sp("Rhacomitrium lanuginosum",  ". . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("R. triquetrus",            ". 4 . . 4 . .",   "II",  "0.8"),
        sp("Rhytidiadelphus loreus",    ". . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Thuidium tamariscinum",     ". 4 . . . 4 .",   "II",  "1.7"),
        sp("Frullania tamarisci",       ". . . . . . .",   "I",   "0.1", True, "sparse"),
        sp("Scapania gracilis",         ". 3 . . 3 . .",   "II",  "0.6"),
        sp("Trichocolea tomentella",    ". . . . . . .",   "I",   "0.1", True, "sparse"),
        # Additional species
        sparse_sp("Carex flacca",         7, {1: "1"}),
        sparse_sp("Heracleum sphondylium", 7, {1: "2"}),
        sparse_sp("Conopodium majus",     7, {1: "2"}),
        sparse_sp("Asplenium adiantum-nigrum", 7, {2: "1"}),
        sparse_sp("Cardamine pratensis",  7, {2: "2"}),
        sparse_sp("Lobaria pulmonaria",   7, {2: "2"}),
        sparse_sp("Dryopteris aemula",    7, {3: "2"}),
        sparse_sp("D. filix-mas",         7, {3: "5"}),
        sparse_sp("Chaerophyllum temulentum", 7, {3: "4"}),
        sparse_sp("Crepis paludosa",      7, {3: "2"}),
        sparse_sp("Lathyrus pratensis",   7, {4: "1"}),
        sparse_sp("Plagiochila asplenoides", 7, {4: "3"}),
        sparse_sp("Sorbus aucuparia",     7, {5: "3"}),
        sparse_sp("Viola sepium",         7, {5: "1"}),
        sparse_sp("Plagiothecium undulatum", 7, {5: "1"}),
        sparse_sp("Trollius europaeus",   7, {5: "1"}),
        sparse_sp("Sanicula europaea",    7, {6: "2"}),
        sparse_sp("Vicia sepium",         7, {6: "1"}),
        sparse_sp("Rhytidiadelphus loreus", 7, {6: "1"}),
        sparse_sp("Diplophyllum albicans", 7, {6: "1"}),
        sparse_sp("Plagiochila spinulosa", 7, {6: "3"}),
        sparse_sp("Lonicera periclymenum", 7, {7: "2"}),
        sparse_sp("Osmunda regalis",      7, {7: "5"}),
    ],
}


# ---------------------------------------------------------------------------
# Export list
# ---------------------------------------------------------------------------

TABLES_51_60 = [
    TABLE_4_41,
    TABLE_4_42,
    TABLE_4_43,
    TABLE_4_43_CONT,
    TABLE_4_44,
    TABLE_4_44_CONT,
    TABLE_4_39,
    TABLE_4_45,
    TABLE_4_46,
    TABLE_4_46_CONT,
]
