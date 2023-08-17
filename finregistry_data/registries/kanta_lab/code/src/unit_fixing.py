import pandas as pd
import re
from collections import defaultdict
import sys

unit_tbl = defaultdict(int)
unit_fix_tbl = defaultdict(int)

res_dir = sys.argv[1]


count = 0
with open(res_dir + "processed/data/kanta_lab_minimal_omop.csv", 'r', encoding="utf-8") as fin:
    with open(res_dir + "processed/data/kanta_lab_minimal_fixed_units.csv", 'w', encoding="utf-8") as fout_min:
        with open(res_dir + "processed/reports/counts/unit_fixes.csv", 'w', encoding="utf-8") as fout_fix:

            first_line = 1
            for line in fin:
                count = count + 1 
                line_arr = line.strip().split(";")
                if not first_line:
                    if(len(line_arr) > 7):
                        lab_unit = line_arr[7]
                        line_arr[5] = re.sub(r'"(.*)"', r'\1', line_arr[5]) # Remove "" around some of the abbreviations
                        if(lab_unit != "NA"): 
                            lab_unit = lab_unit.lower().strip()  
                            lab_unit = re.sub(r'^$', 'NA', lab_unit)

                            # es
                            lab_unit = re.sub(r'^\d+(?=e\d+)', '', lab_unit)
                            lab_unit = re.sub(r'^\b\d+(?=e\d+)', '', lab_unit)
                            lab_unit = re.sub(r"(x)?(10)?e(?=\d)", "e", lab_unit)
                            lab_unit = re.sub(r"(x)?10(\^|\*)", "e", lab_unit)
                            lab_unit = re.sub(r"e(0)?(?=[0-9]+.?l)", "e", lab_unit)
                            lab_unit = re.sub(r"^\^(?=[0-9]+.?l)", "e", lab_unit)


                            ## micros
                            lab_unit = re.sub(r"(y|µ)ks(ikkö)?", "u", lab_unit)
                            lab_unit = re.sub(r"y", "µ", lab_unit) # Most ys do not mean anything
                            lab_unit = re.sub(r"lµ", "ly", lab_unit) # Except for lymph stuff

                            # mµ/l
                            lab_unit = re.sub(r"m([a-z]?)µ", "mµ", lab_unit) # i.e. mlµ and miµ
                            lab_unit = re.sub(r"^mµ.?l$", "mµ/l", lab_unit)
                            
                            # µ/l - Enzyme activity
                            lab_unit = re.sub(r"^µ.?l$", "µ/l", lab_unit)
                            lab_unit = re.sub(r"^u.?l$", "u/l", lab_unit)

                            # µmol/l
                            lab_unit = re.sub(r"umol", "µmol", lab_unit)
                            lab_unit = re.sub(r"^µmol.?l$", "µmol/l", lab_unit)

                            # µg/l
                            lab_unit = re.sub(r"^(µ|u)g.?l$", "µg/l", lab_unit)

                            # mmol
                            lab_unit = re.sub(r"^(m)?mmo(l)?/", "mmol/", lab_unit)
                            # mol
                            lab_unit = re.sub(r"mo(t|l|i)?(l)?", "mol", lab_unit)

                            # mmol/l and mmol/mol
                            lab_unit = re.sub(r"^mmol.?(l|i|mol).?$", "mmol/l", lab_unit)

                            # mm/h
                            lab_unit = re.sub(r"^(m)?m(h)?/h$", "mm/h", lab_unit)                    
                            lab_unit = re.sub(r"^mh.?h$", "mm/h", lab_unit)

                            # mgl
                            lab_unit = re.sub(r"^.?mg.?l$", "mg/l", lab_unit)

                            # GFR
                            lab_unit = re.sub(r"^ml/min.*$", "ml/min/173m2", lab_unit)
                            lab_unit = re.sub(r"^ml/.*/17.*$", "ml/min/173m2", lab_unit)
                            lab_unit = re.sub(r"^ml.?min.?173m2$", "ml/min/173m2", lab_unit)

                            # INR
                            lab_unit = re.sub(r"^inrarvo$", "inr", lab_unit)

                            #mosm/kg20 - miliosmoles per kilogram of water
                            lab_unit = re.sub(r"^mosm/kg.*$", "mosm/kgh2o", lab_unit)

                            # Osuus
                            lab_unit = re.sub(r"^tilo(s)?$", "osuus", lab_unit)
                            lab_unit = re.sub(r"^(til)osuu(s)$", "osuus", lab_unit)

                            # Counts
                            lab_unit = re.sub(r"kopio(t)?(a)?", "kpl",lab_unit)
                            lab_unit = re.sub(r"klp", "kpl", lab_unit)
                            lab_unit = re.sub(r"sol(y|µ|u)", "kpl", lab_unit)
                            lab_unit = re.sub(r"pisteet", "kpl",lab_unit)
                            # Viewfield
                            lab_unit = re.sub(r"n(ä)?kö(ke)?k(enttä)?", "nk", lab_unit)
                            lab_unit = re.sub(r"s(y|µ)n(fält|f)?$", "nk",lab_unit)
                            # Counts per viewfield
                            lab_unit = re.sub(r"^(kpla)/nk", "kpl/nk", lab_unit)
                            lab_unit = re.sub(r"^kpl.?nk$", "kpl/nk",lab_unit)

                            # Tiiteri
                            lab_unit = re.sub(r"^.*ti(i)?t(t)?er(i)?.*$", "titre",lab_unit)

                            

                            #Imuno assay
                            lab_unit = re.sub(r"^elia(u|µ)", "eliau",lab_unit)
                            lab_unit = re.sub(r"^a(u|µ)/ml$", "au/ml",lab_unit)

                            # f-calpro
                            lab_unit = re.sub(r"gulos(t.*)$", "gstool",lab_unit)
                            lab_unit = re.sub(r"(u|µ)g/g stool", "µg/gstool",lab_unit)

                            # Promille
                            lab_unit = re.sub(r"^promil(l)?$", "promille",lab_unit)
                            lab_unit = re.sub(r"^o/oo$", "promille",lab_unit)

                            # Pos/Neg
                            lab_unit = re.sub(r"^\+$", "A",lab_unit)
                            lab_unit = re.sub(r"^\-$", "N",lab_unit)
                            lab_unit = re.sub(r"^negat$", "N",lab_unit)
                            lab_unit = re.sub(r"^neg$", "N",lab_unit)
                            lab_unit = re.sub(r"^pos$", "A",lab_unit)

                            # Random
                            lab_unit = re.sub(r"^p.?g$", "pg", lab_unit)
                            lab_unit = re.sub(r"^f.?l$", "fl", lab_unit)
                            lab_unit = re.sub(r"q", "g", lab_unit)
                            lab_unit = re.sub(r"\/\/", "/",lab_unit)
                            lab_unit = re.sub(r"(c)?aste(c)?", "aste",lab_unit)
                            lab_unit = re.sub(r"sek", "s",lab_unit)
                            lab_unit = re.sub(r"ve/", "responseequivalent/",lab_unit)
                            lab_unit = re.sub(r"aru", "au",lab_unit)
                            lab_unit = re.sub(r"liter", "l",lab_unit)
                            lab_unit = re.sub(r"iu", "u", lab_unit)

                            # Days
                            lab_unit = re.sub(r"/d$", "/24h",lab_unit)
                            lab_unit = re.sub(r"/vrk$", "/24h",lab_unit)
 
                            # Translations
                            lab_unit = re.sub(r"nk$", "field",lab_unit)
                            lab_unit = re.sub(r"kpl", "count",lab_unit)
                            lab_unit = re.sub(r"lausunto", "lomake", lab_unit)
                            lab_unit = re.sub(r"lomake", "form", lab_unit)
                            lab_unit = re.sub(r"^indeksi$", "index",lab_unit)
                            lab_unit = re.sub(r"arvio", "estimate",lab_unit)
                            lab_unit = re.sub(r"suhde", "ratio",lab_unit)
                            lab_unit = re.sub(r"krt", "times",lab_unit)

                            # Removing redundant and inconsistant information
                            lab_unit = re.sub(r"/100le(uk)$", "",lab_unit)
                            lab_unit = re.sub(r"/24h$", "",lab_unit)
                            lab_unit = re.sub(r"/l/(37c|ph7|ph74)?", "/l", lab_unit)


                            # Power changes
                            lab_unit = re.sub(r"^ku/l$", "u/ml", lab_unit)
                            lab_unit = re.sub(r"^pg/ml$", "ng/l", lab_unit)
                            lab_unit = re.sub(r"^µg/l$", "ng/ml", lab_unit)
                            lab_unit = re.sub(r"^(µ|u)g/ml$", "mg/l", lab_unit)

                            fout_fix.write(line_arr[5] + ";" + line_arr[7] + ";" + lab_unit + "\n")
                            
                        line_arr[7] = lab_unit.strip()

                else:
                    first_line = 0
                fout_min.write(";".join(line_arr) + "\n")