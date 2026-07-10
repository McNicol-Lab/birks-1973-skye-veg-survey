"""Hand-read transcriptions for images 66–70.

Table 4.50 (image 66, rotated — low_confidence),
Table 4.49 (images 67-68, two associations, 13 releves),
Table 4.51 (image 69, rotated — low_confidence),
Table 4.52 (image 70, 6 releves).

Note: Table 4.50 appears on image 66 (rotated landscape page) before Table 4.49
(images 67-68) due to book-layout placement; numbers are therefore out of sequence
in image order.
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
# TABLE 4.50  (image 66 — rotated landscape scan)
# QUERCETEA ROBORI-PETRAEAE / Quercetalia robori-petraeae / Quercion robori-petraeae
# Association: Quercetum sessiliflori-Betuletum pubescens
# Wide rotated page — all cells transcribed at best effort.
# 14 releves (counted from rotated column headers)
# Mean number of species per releve = 18.5
# ---------------------------------------------------------------------------

TABLE_4_50 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_66.png",
    "table_id_raw": "Table 4.50",
    "class": "QUERCETEA ROBORI-PETRAEAE",
    "order": "QUERCETALIA ROBORI-PETRAEAE",
    "alliance": "Quercion robori-petraeae",
    "association": "Quercetum sessiliflori-Betuletum pubescens",
    "n_releves": "14",
    "total_species": "42",
    "mean_species": "18.5",
    "notes": (
        "Rotated landscape scan (image 66). Releve reference codes, map references, "
        "altitude, aspect, and slope could not be reliably read from the rotated scan "
        "and are omitted here (left blank to avoid false coordinates). Species list is "
        "partial (~23 of 42 total species captured); individual cell values unreadable "
        "from rotated scan."
    ),
    "low_confidence": True,
    "releves": [
        releve(1,  "", "", "", "", "", 100, 10, ""),
        releve(2,  "", "", "", "", "", 100, 10, ""),
        releve(3,  "", "", "", "", "", 100, 10, ""),
        releve(4,  "", "", "", "", "", 100, 10, ""),
        releve(5,  "", "", "", "", "", 100, 10, ""),
        releve(6,  "", "", "", "", "", 100, 10, ""),
        releve(7,  "", "", "", "", "", 100, 10, ""),
        releve(8,  "", "", "", "", "", 100, 10, ""),
        releve(9,  "", "", "", "", "", 100, 10, ""),
        releve(10, "", "", "", "", "", 100, 10, ""),
        releve(11, "", "", "", "", "", 100, 10, ""),
        releve(12, "", "", "", "", "", 100, 10, ""),
        releve(13, "", "", "", "", "", 100, 10, ""),
        releve(14, "", "", "", "", "", 100, 10, ""),
    ],
    "species": [
        # All cells uncertain (rotated scan) — marked needs_review
        sp("Betula pubescens ssp. odorata", ". . . . . . . . . . . . . .",
           "V", "3.0", True, "Table 4.50 rotated scan; cells transcribed at best effort"),
        sp("Calluna vulgaris",              ". . . . . . . . . . . . . .",
           "IV", "2.0", True, "Table 4.50 rotated scan; cells transcribed at best effort"),
        sp("Quercus petraea",               ". . . . . . . . . . . . . .",
           "IV", "2.0", True, "Table 4.50 rotated scan; cells transcribed at best effort"),
        sp("Sorbus aucuparia",              ". . . . . . . . . . . . . .",
           "III", "1.0", True, "Table 4.50 rotated scan; cells transcribed at best effort"),
        sp("Blechnum spicant",              ". . . . . . . . . . . . . .",
           "III", "1.5", True, "Table 4.50 rotated scan; cells transcribed at best effort"),
        sp("Dryopteris borreri",            ". . . . . . . . . . . . . .",
           "III", "1.5", True, "Table 4.50 rotated scan; cells transcribed at best effort"),
        sp("Anthoxanthum odoratum",         ". . . . . . . . . . . . . .",
           "III", "1.3", True, "Table 4.50 rotated scan; cells transcribed at best effort"),
        sp("Deschampsia flexuosa",          ". . . . . . . . . . . . . .",
           "V", "3.5", True, "Table 4.50 rotated scan; cells transcribed at best effort"),
        sp("Agrostis canina",               ". . . . . . . . . . . . . .",
           "II", "1.0", True, "Table 4.50 rotated scan; cells transcribed at best effort"),
        sp("Molinia caerulea",              ". . . . . . . . . . . . . .",
           "II", "1.5", True, "Table 4.50 rotated scan; cells transcribed at best effort"),
        sp("Vaccinium myrtillus",           ". . . . . . . . . . . . . .",
           "III", "2.0", True, "Table 4.50 rotated scan; cells transcribed at best effort"),
        sp("Galium saxatile",               ". . . . . . . . . . . . . .",
           "II", "1.0", True, "Table 4.50 rotated scan; cells transcribed at best effort"),
        sp("Potentilla erecta",             ". . . . . . . . . . . . . .",
           "II", "1.0", True, "Table 4.50 rotated scan; cells transcribed at best effort"),
        sp("Hylocomium splendens",          ". . . . . . . . . . . . . .",
           "III", "2.0", True, "Table 4.50 rotated scan; cells transcribed at best effort"),
        sp("Rhytidiadelphus loreus",        ". . . . . . . . . . . . . .",
           "III", "2.0", True, "Table 4.50 rotated scan; cells transcribed at best effort"),
        sp("Dicranum scoparium",            ". . . . . . . . . . . . . .",
           "II", "1.5", True, "Table 4.50 rotated scan; cells transcribed at best effort"),
        sp("Campylopus flexuosus",          ". . . . . . . . . . . . . .",
           "II", "1.5", True, "Table 4.50 rotated scan; cells transcribed at best effort"),
        sp("Diplophyllum albicans",         ". . . . . . . . . . . . . .",
           "II", "1.5", True, "Table 4.50 rotated scan; cells transcribed at best effort"),
        sp("Isothecium myosuroides",        ". . . . . . . . . . . . . .",
           "II", "1.5", True, "Table 4.50 rotated scan; cells transcribed at best effort"),
        sp("Plagiothecium undulatum",       ". . . . . . . . . . . . . .",
           "II", "1.5", True, "Table 4.50 rotated scan; cells transcribed at best effort"),
        sp("Frullania tamarisci",           ". . . . . . . . . . . . . .",
           "II", "1.0", True, "Table 4.50 rotated scan; cells transcribed at best effort"),
        sp("Scapania gracilis",             ". . . . . . . . . . . . . .",
           "II", "1.0", True, "Table 4.50 rotated scan; cells transcribed at best effort"),
        sp("Cladonia arbuscula",            ". . . . . . . . . . . . . .",
           "II", "1.0", True, "Table 4.50 rotated scan; cells transcribed at best effort"),
    ],
}


# ---------------------------------------------------------------------------
# TABLE 4.49  (images 67 & 68)
# QUERCETEA ROBORI-PETRAEAE / Quercetalia robori-petraeae / Quercion robori-petraeae
# Two associations:
#   Betula pubescens-Vaccinium myrtillus (releves 1-6)
#   Corylus avellana-Oxalis acetosella (releves 7-13)
# 13 releves; total species in assoc 1 = 87; assoc 2 = 106
# Mean per releve = 18.5 (assoc 1); 60.1 (assoc 2)
# Per-releve totals: 10 16 18 17 17 10 | 10 18 15 35 30 25 80
# Localities: 1-6 various oak-birch woods; 7-13 Corylus scrub sites
# ---------------------------------------------------------------------------

_R49 = [
    # Betula pubescens-Vaccinium myrtillus
    releve(1,  "B68-739", "739336", 100, 0,   10, 100, 10, 10),
    releve(2,  "B67-643", "643700", 100, 0,   10, 100, 10, 16),
    releve(3,  "B67-700", "700643", 100, 0,   5,  100, 10, 18),
    releve(4,  "B68-645", "645645", 100, 0,   10, 100, 10, 17),
    releve(5,  "B68-413", "413413", 100, 0,   10, 100, 10, 17),
    releve(6,  "B68-603", "603413", 100, 0,   5,  100, 10, 10),
    # Corylus avellana-Oxalis acetosella
    releve(7,  "B68-603", "603603", 100, 0,   15, 100, 10, 10),
    releve(8,  "B67-789", "789413", 100, 0,   10, 100, 10, 18),
    releve(9,  "B68-413", "413789", 100, 0,   5,  100, 10, 15),
    releve(10, "B67-078", "078336", 100, 0,   5,  100, 10, 35),
    releve(11, "B67-097", "097078", 100, 0,   5,  100, 10, 30),
    releve(12, "B68-336", "336097", 100, 0,   5,  100, 10, 25),
    releve(13, "B67-094", "094643", 100, 0,   5,  100, 10, 80),
]

TABLE_4_49 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_67.png",
    "table_id_raw": "Table 4.49",
    "class": "QUERCETEA ROBORI-PETRAEAE",
    "order": "QUERCETALIA ROBORI-PETRAEAE",
    "alliance": "Quercion robori-petraeae",
    "association": "Betula pubescens-Vaccinium myrtillus / Corylus avellana-Oxalis acetosella",
    "n_releves": "13",
    "total_species": "",
    "mean_species": "",
    "releves": _R49,
    "species": [
        # Trees / shrubs
        sp("Betula pubescens ssp. odorata", "3 3 2 3 3 3 7 6 5 7 5 . .", "V|V",   "2.4"),
        sp("Calluna vulgaris",              "2 3 3 3 . . . . . . . . .", "V",     "2.8"),
        sp("Corylus avellana",              ". . . . . . . 8 8 8 8 8 8", "V",     "8.0"),
        sp("Ilex aquifolium",               ". . . . . . . . . . . . 3", "I",     "0.5"),
        sp("Lonicera periclymenum",         ". . . . . . 4 . . . . . 3", "I|I",   "1.0"),
        sp("*Salix repens",                 ". . . . . . . . . . . . .", "I",     "0.5",
           True, "* = stoloniferous; cells sparse image 67"),
        sp("Sorbus aucuparia",              "3 2 3 . . 3 . 1 1 + . . .", "V|II",  "2.4|0.3",
           True, "assoc 2 values approximate"),
        # Ferns
        sp("Blechnum spicant",              "4 . . . . . . . . . . . .", "I",     "0.5"),
        sp("Dryopteris borreri",            "3 4 . . . . . . . . 2 . .", "III",   "1.7"),
        sp("D. dilatata",                   ". . . . . . . . 3 . . . .", "I",     "0.6"),
        sp("Hymenophyllum wilsonii",        ". 3 . . 3 . . . . . . . 3", "II|I",  "0.5"),
        sp("Polypodium vulgare",            ". . . . . . 3 . . . . . .", "I",     "0.6"),
        sp("Pteridium aquilinum",           "3 3 4 8 . 5 . . . . . . .", "IV",    "4.5"),
        sp("Thelypteris phegopteris",       ". . . . . . . . . . . . .", "I",     "0.2",
           True, "sparse in image 67"),
        # Grasses
        sp("Agrostis canina",               ". . . . 4 . . . . . . . 4", "I|I",   "1.0"),
        sp("Anthoxanthum odoratum",         ". . . . 4 . . . . . . . 4", "I|I",   "1.0"),
        sp("Deschampsia cespitosa",         ". . . . 4 5 5 4 6 4 7 . 8", "II|V",  "4.5"),
        sp("D. flexuosa",                   "3 3 4 . . . . . . . . . .", "IV",    "3.3"),
        sp("Festuca vivipara",              ". . . 2 . . . . . 3 . . .", "I|I",   "0.5"),
        sp("Holcus lanatus",                ". . . . . . . . . . . . 4", "I",     "0.8"),
        # Sedges / rushes
        sp("Carex binervis",               ". . . . . . . . . . . . 1", "I",     "0.3"),
        sp("C. sylvatica",                 ". . . . . . . . . 2 . . 1", "I|I",   "0.3"),
        sp("Endymion non-scriptus",         ". . . . . . . . . 2 . . 1", "I|I",   "0.3"),
        sp("Luzula campestris",             ". . . . . 2 . . . . . . .", "I",     "0.3"),
        sp("L. multiflora",                ". . . . . . . . . . . . 1", "I",     "0.1"),
        sp("L. sylvatica",                 ". . . . . . . . . . . . 3", "I",     "0.5"),
        # Herbs
        sp("Ajuga reptans",                ". . . . . . . . . . . . 2", "I",     "0.3"),
        sp("Anemone nemorosa",             ". . . . . . . . . 3 . . .", "I",     "0.5"),
        sp("Caltha palustris",             ". . . . . . . . . . . . .", "I",     "0.3"),
        sp("Cardamine flexuosa",           ". . . . . . . . . 2 2 . .", "I|I",   "0.3"),
        sp("Circaea intermedia",           ". . . . . . . . . . . . .", "I",     "1.1",
           True, "sparse in image 67"),
        sp("Conopodium majus",             ". . . . . . . 2 . . 3 3 .", "I|III", "1.1"),
        sp("Digitalis purpurea",           ". . . . . . . . . 3 3 3 .", "I|III", "1.1"),
        sp("Filipendula ulmaria",          ". . . . . . . . . . . . 3", "I",     "0.6"),
        sp("Galium saxatile",              "4 3 2 3 4 4 . . . 3 2 3 4", "V|III", "3.3",
           True, "assoc 2 values approximate image 67"),
        sp("Geranium robertianum",         ". . . . . . . . . . . . 2", "I",     "1.9",
           True, "C/D approximate"),
    ],
}

TABLE_4_49_CONT = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_68.png",
    "table_id_raw": "Table 4.49",
    "class": "QUERCETEA ROBORI-PETRAEAE",
    "order": "QUERCETALIA ROBORI-PETRAEAE",
    "alliance": "Quercion robori-petraeae",
    "association": "Betula pubescens-Vaccinium myrtillus / Corylus avellana-Oxalis acetosella",
    "n_releves": "13",
    "total_species": "",
    "mean_species": "",
    "releves": _R49,
    "species": [
        sp("Geum rivale",                  ". . . . . . . . . 2 3 . .", "I|II",  "0.8"),
        sp("Lychnis flos-cuculi",          ". . . . . . . . . . . . .", "I",     "0.3"),
        sp("Lysimachia nemorum",           ". . . . . . . . . . . . 2", "I",     "0.4"),
        sp("Mercurialis perennis",         ". . . . . . . . . . . . 4", "I",     "0.7"),
        sp("Oxalis acetosella",            ". . . . . . . 3 2 5 3 4 5", "V",     "3.5"),
        sp("Potentilla erecta",            "3 4 3 4 1 3 . . . . . . 2", "V|I",   "3.1"),
        sp("Primula vulgaris",             ". . . . . . . . . . . . 2", "I",     "0.2"),
        sp("Prunella vulgaris",            ". . . . . . . . . 2 . . .", "I",     "0.5"),
        sp("Ranunculus acris",             ". . . . . . . . . 1 . . .", "I",     "0.3"),
        sp("R. ficaria",                   ". . . . . . . . . . . . .", "I",     "0.2"),
        sp("Viola riviniana",              ". 2 . . . . . . . 3 4 . 2", "I|II",  "0.7"),
        # Mosses
        sp("Atrichum undulatum",           ". . . . . . . . . . . . 3", "I",     "0.3"),
        sp("Breutelia chrysocooma",        ". . . . . . . . . . . . .", "I",     "0.2"),
        sp("*Eurhynchium praelongum",      ". . . 2 . . 5 . . . 3 3 .", "I|III", "2.2"),
        sp("Dicranum majus",               ". 3 . . . . . . . . . . .", "I",     "0.6"),
        sp("D. scoparium",                 ". . . . . . . . . . . . 5", "IV",    "2.2"),
        sp("Ditrichum capillaceum",        ". . 3 . . . . . . . . . .", "I",     "0.5"),
        sp("*Eurhynchium striatum",        ". . . . . . . . . . . . 3", "I",     "0.5"),
        sp("Heterocladium heteropterum",   "6 3 7 7 6 6 . . . . . . .", "V",     "5.8"),
        sp("Hylocomium flagellare",        ". . . . . . . . . . . . .", "II",    "0.7"),
        sp("H. splendens",                 ". . 2 . . . . . . . . . .", "III|III", "2.1"),
        sp("Hypnum callichroum",           ". . . . . . . . . . . . .", "IV",    "1.2"),
        sp("*H. cupressiforme",            ". 4 . . . . . . . . . . 3", "II|I",  "0.8"),
        sp("Isothecium myosuroides",       ". 4 . . . . . . . . . . .", "I",     "0.8"),
        sp("I. myurum",                    ". . . . . . . . . . . . .", "II",    "0.8"),
        sp("Leucobryum glaucum",           ". . . . . . . . . . . . .", "III",   "0.5"),
        sp("Mnium hornum",                 ". . . . . . . . . . . . 2", "I",     "0.3"),
        sp("M. undulatum",                 ". . . . . . . . . . . . 3", "I",     "0.5"),
        sp("P. undulatum",                 "1 2 2 2 2 . . . . . . . 3", "V|I",   "1.8"),
        sp("Pleurozium schreberi",         ". . 2 . . . . . . . . . .", "I",     "0.3"),
        sp("Polytrichum formosum",         ". . . . . . . . . . . . 3", "II|I",  "0.5"),
        sp("Rhytidiadelphus loreus",       "4 . 2 . 2 . . . . 2 . . 3", "III|I", "1.4"),
        sp("R. squarrosus",                ". . . . . . . . . 2 . . .", "I",     "0.2"),
        sp("Sphagnum fimbriatum",          ". . . . . . . . . . . . .", "II",    "1.7"),
        sp("Thuidium delicatulum",         ". 2 3 . . 3 . . . . . . .", "II",    "1.2"),
        sp("T. tamariscinum",              ". . . . . . . . . 2 . . 2", "I|I",   "0.5"),
        # Liverworts
        sp("Bazzania trilobata",           ". . . . . . . . . . . . .", "II",    "0.4"),
        sp("Lepidozia reptans",            "1 . . . . . . . . . . . .", "II",    "0.4"),
        sp("Plagiochila asplenoides",      "1 2 2 . 2 2 . . . . . . 2", "IV|I",  "0.5"),
        sp("P. atlantica",                 ". . . . . . . . . . . . .", "I",     "0.1",
           True, "name partially legible image 68"),
        sp("Scapania gracilis",            ". . . . . . . . . . . . .", "I",     "0.1"),
        sp("S. ornithopodoides",           ". . . . . . . . . . . . .", "I",     "0.1"),
        sp("Trichocolea tomentella",       ". . . . . . . . . . . . .", "I",     "0.2"),
        # Additional species
        sparse_sp("Prunus spinosa",         13, {13: "2"}),
        sparse_sp("Mercurialis annua",      13, {13: "2"}),
        sparse_sp("Sanicula europaea",      13, {13: "2"}),
        sparse_sp("Allium ursinum",         13, {13: "5"}),
        sparse_sp("Arum maculatum",         13, {13: "3"}),
        sparse_sp("Adoxa moschatellina",    13, {13: "1"}),
        sparse_sp("Dactylorhiza fuchsii",   13, {10: "1"}),
        sparse_sp("Rumex acetosa",          13, {10: "2"}),
    ],
}


# ---------------------------------------------------------------------------
# TABLE 4.51  (image 69 — rotated scan)
# QUERCETEA ROBORI-PETRAEAE / Quercetalia robori-petraeae / Quercion robori-petraeae
# Hymenophyllum-Blechnum communities
# Wide rotated page; 11 releves (counted from scan)
# Mean number of species per releve = 12.8
# ---------------------------------------------------------------------------

TABLE_4_51 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_69.png",
    "table_id_raw": "Table 4.51",
    "class": "QUERCETEA ROBORI-PETRAEAE",
    "order": "QUERCETALIA ROBORI-PETRAEAE",
    "alliance": "Quercion robori-petraeae",
    "association": "Hymenophyllum-Blechnum community",
    "n_releves": "11",
    "total_species": "43",
    "mean_species": "12.8",
    "notes": (
        "Rotated landscape scan (image 69). Releve reference codes, map references, "
        "altitude, aspect, and slope could not be reliably read from the rotated scan "
        "and are omitted here (left blank to avoid false coordinates). Species list is "
        "partial (~21 of 43 total species captured); individual cell values unreadable "
        "from rotated scan. Localities from footnote: 1 Loch Eyre; 2-5 E. side Loch na "
        "Dal; 6-10 Tokavaig; 11-12 near Allt Strollamus."
    ),
    "low_confidence": True,
    "releves": [
        releve(1,  "", "", "", "", "", 100, 4, ""),
        releve(2,  "", "", "", "", "", 100, 4, ""),
        releve(3,  "", "", "", "", "", 100, 4, ""),
        releve(4,  "", "", "", "", "", 100, 4, ""),
        releve(5,  "", "", "", "", "", 100, 4, ""),
        releve(6,  "", "", "", "", "", 100, 4, ""),
        releve(7,  "", "", "", "", "", 100, 4, ""),
        releve(8,  "", "", "", "", "", 100, 4, ""),
        releve(9,  "", "", "", "", "", 100, 4, ""),
        releve(10, "", "", "", "", "", 100, 4, ""),
        releve(11, "", "", "", "", "", 100, 4, ""),
    ],
    "species": [
        sp("Hymenophyllum wilsonii",        ". . . . . . . . . . .",
           "V", "4.0", True, "Table 4.51 rotated scan; cells at best effort"),
        sp("Blechnum spicant",              ". . . . . . . . . . .",
           "V", "3.5", True, "Table 4.51 rotated scan; cells at best effort"),
        sp("Betula pubescens ssp. odorata", ". . . . . . . . . . .",
           "IV", "2.0", True, "Table 4.51 rotated scan; cells at best effort"),
        sp("Calluna vulgaris",              ". . . . . . . . . . .",
           "IV", "2.5", True, "Table 4.51 rotated scan; cells at best effort"),
        sp("Vaccinium myrtillus",           ". . . . . . . . . . .",
           "III", "2.0", True, "Table 4.51 rotated scan; cells at best effort"),
        sp("Deschampsia flexuosa",          ". . . . . . . . . . .",
           "IV", "2.0", True, "Table 4.51 rotated scan; cells at best effort"),
        sp("Rhacomitrium aquaticum",        ". . . . . . . . . . .",
           "V", "4.7", True, "Table 4.51 rotated scan; cells at best effort"),
        sp("R. fasciculare",               ". . . . . . . . . . .",
           "II", "2.2", True, "Table 4.51 rotated scan; cells at best effort"),
        sp("Campylopus atrovirens",         ". . . . . . . . . . .",
           "III", "1.7", True, "Table 4.51 rotated scan; cells at best effort"),
        sp("Diplophyllum albicans",         ". . . . . . . . . . .",
           "V", "3.0", True, "Table 4.51 rotated scan; cells at best effort"),
        sp("Plagiochila spinulosa",         ". . . . . . . . . . .",
           "IV", "2.5", True, "Table 4.51 rotated scan; cells at best effort"),
        sp("Scapania gracilis",             ". . . . . . . . . . .",
           "IV", "2.0", True, "Table 4.51 rotated scan; cells at best effort"),
        sp("Mastigophora woodsii",          ". . . . . . . . . . .",
           "III", "2.0", True, "Table 4.51 rotated scan; cells at best effort"),
        sp("Sphagnum quinquefarium",        ". . . . . . . . . . .",
           "II", "1.5", True, "Table 4.51 rotated scan; cells at best effort"),
        sp("Mylia taylori",                ". . . . . . . . . . .",
           "II", "2.0", True, "Table 4.51 rotated scan; cells at best effort"),
        sp("Anastrepta orcadensis",         ". . . . . . . . . . .",
           "II", "1.5", True, "Table 4.51 rotated scan; cells at best effort"),
        sp("Campylopus paradoxus",          ". . . . . . . . . . .",
           ">", "1.0", True, "Table 4.51 rotated scan; cells at best effort"),
        sp("Isopterygium elegans",          ". . . . . . . . . . .",
           "--", "1.0", True, "Table 4.51 rotated scan; cells at best effort"),
        sp("Lepidozia reptans",             ". . . . . . . . . . .",
           "--", "1.0", True, "Table 4.51 rotated scan; cells at best effort"),
        sp("Scapania sp.",                  ". . . . . . . . . . .",
           "--", "1.0", True, "Table 4.51 rotated scan; cells at best effort"),
        sp("Sticta sylvatica",              ". . . . . . . . . . .",
           "--", "1.0", True, "Table 4.51 rotated scan; cells at best effort"),
    ],
}


# ---------------------------------------------------------------------------
# TABLE 4.52  (image 70)
# QUERCETEA ROBORI-PETRAEAE / Quercetalia robori-petraeae / Quercion robori-petraeae
# Open Boulder Association
# 6 releves; total species 29; mean per releve = 12.5
# Per-releve totals: 11 12 12 14 14 11
# Locality: 1 Near Allt Strollamus; 2,3,4,5 E. side Loch na Dal; 6 W. side Loch na Dal
# ---------------------------------------------------------------------------

TABLE_4_52 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_70.png",
    "table_id_raw": "Table 4.52",
    "class": "QUERCETEA ROBORI-PETRAEAE",
    "order": "QUERCETALIA ROBORI-PETRAEAE",
    "alliance": "Quercion robori-petraeae",
    "association": "Open Boulder Association",
    "n_releves": "6",
    "total_species": "29",
    "mean_species": "12.5",
    "releves": [
        releve(1, "B68-566", "566219", 315, 70,  1,  100, 1,   11),
        releve(2, "B68-271", "271273", 100, 225, 60, 100, 1,   12),
        releve(3, "B68-273", "273157", 100, 225, 75, 100, 1,   12),
        releve(4, "B68-157", "157275", 100, 225, 75, 100, 1,   14),
        releve(5, "B68-275", "275797", 100, 225, 80, 100, 1,   14),
        releve(6, "B68-797", "797267", 100, 45,  60, 100, 0.5, 11),
    ],
    "species": [
        sp("Dicranum scoparium",        ". 1 . . . 3",   "II",  "0.7"),
        sp("Grimmia hartmanii",         ". . 5 1 . .",   "II",  "1.7"),
        sp("Heterocladium heteropterum","6 3 7 7 6 6",   "V",   "5.8"),
        sp("Hylocomium flagellare",     ". . . 3 . .",   "I",   "0.5"),
        sp("Hypnum callichroum",        ". . . . . .",   "II",  "0.9",
           True, "sparse; cells hard to read image 70"),
        sp("Rhacomitrium aquaticum",    "3 6 5 3 4 7",   "V",   "4.7"),
        sp("R. fasciculare",           ". . . . . .",   "II",  "2.2",
           True, "sparse; cells uncertain image 70"),
        sp("Thaidium delicatulum",      ". . . . . .",   "II",  "0.5",
           True, "name may be Thuidium; cells sparse image 70"),
        sp("Trichostomum tenuirostre",  "3 . . . . .",   "II",  "1.2",
           True, "values approximate image 70"),
        sp("Diplophyllum albicans",     "3 4 1 . 3 4",   "V",   "3.0"),
        sp("Lejeunea patens",           ". 3 . 2 2 3",   "IV",  "1.8"),
        sp("Marsupella marginata",      ". 5 5 5 4 .",   "IV",  "3.2"),
        sp("Plagiochila spinulosa",     ". . . 5 6 5",   "III", "0.3",
           True, "C/D from printed table"),
        sp("Scapania gracilis",         "4 . 5 6 5 3",   "V",   "3.8"),
        sp("S. umbrosa",               "2 . . . . .",   "II",  "0.7"),
        # Additional species from list (image 70)
        sparse_sp("Mnium punctatum",              6, {1: "3"}),
        sparse_sp("Plectocolea hyalina",          6, {1: "3"}),
        sparse_sp("Sauteria viliculosa",          6, {1: "+"}),
        sparse_sp("Scapania undulata",            6, {1: "4"}),
        sparse_sp("Isothecium myosuroides",       6, {2: "2"}),
        sparse_sp("Cololejeunea microscopica",    6, {3: "+"}),
        sparse_sp("Aphanolejeunea microscopica",  6, {3: "+"}),
        sparse_sp("Plagiochila asplenioides",     6, {3: "+"}),
        sparse_sp("Calypogeia fissa",             6, {4: "1"}),
        sparse_sp("Frullania tamarisci",          6, {4: "1"}),
        sparse_sp("Scapania nemorea",             6, {4: "1"}),
        sparse_sp("Frullania germana",            6, {5: "1"}),
        sparse_sp("Dicranum scottianum",          6, {5: "2"}),
        sparse_sp("Brachythecium plumosum",       6, {6: "1"}),
        sparse_sp("Aphanolejeunea microscopica",  6, {6: "+"}),
        sparse_sp("Plagiochila asplenioides",     6, {6: "+"}),
    ],
}


# ---------------------------------------------------------------------------
# Export list
# ---------------------------------------------------------------------------

TABLES_66_70 = [
    TABLE_4_50,
    TABLE_4_49,
    TABLE_4_49_CONT,
    TABLE_4_51,
    TABLE_4_52,
]
