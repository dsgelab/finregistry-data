import re
from collections import defaultdict
import sys
import time

import csv

start = time.time()
print("Starting unit fixing")

unit_tbl = defaultdict(int)
unit_fix_tbl = defaultdict(int)

res_dir = sys.argv[1]
kanta_lab_file = sys.argv[2]
date = sys.argv[3]

count = 0
with open(kanta_lab_file, 'r', encoding="utf-8") as fin:
    with open(res_dir + "processed/data/kanta_lab_" + date + "_fixed_units.csv", 'w', encoding="utf-8") as fout_min:
        with open(res_dir + "processed/reports/counts/" + date + "_unit_fixes.csv", 'w', encoding="utf-8") as fout_fix:
            reader = csv.reader(fin, quotechar='"', doublequote=False, escapechar='\\', delimiter="\t")            
            first_line = 1
            for line_arr in reader:
                count = count + 1 
                if(count % 10000000 == 0): 
                    end = time.time()
                    print("Lines read = " + str(count) + " Time took = " + str(round((end-start)/60)) + " [min]")
                if not first_line:
                    if(len(line_arr) > 7):
                        lab_unit = line_arr[7]
                        if(lab_unit != "NA"): 
                            lab_unit = lab_unit.lower().strip()  
                            # Remove lonely nonsense signs
                            lab_unit = re.sub(r"(^\*+$|^$)", "NA", lab_unit)

                            # es
                            lab_unit = re.sub(r'(^(\b)?\d+(?=e\d+))', "", lab_unit)

                            lab_unit = re.sub(r"(à?x?(10)?e0?(?=\d)|x?10(\^|\*)|^\^(?=[0-9]+.?l))", "e", lab_unit)
            
                            ## micros
                            lab_unit = re.sub(r"(y|µ)ks(ikkö)?", "u", lab_unit)
                            lab_unit = re.sub(r"y", "µ", lab_unit) # Most ys do not mean anything
                            lab_unit = re.sub(r"lµ", "ly", lab_unit) # Except for lymph stuff
                            lab_unit = re.sub(r"tehtµ", "tehty", lab_unit) # Except for lymph stuff

                            lab_unit = re.sub(r"ug", "µg", lab_unit) # ther is no unit grams

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
                            lab_unit = re.sub(r"(mo(t|l|i)?(l)?)(?=$)|nol", "mol", lab_unit)

                            # mmol/l and mmol/mol
                            lab_unit = re.sub(r"^mmol.?(l|i).?$", "mmol/l", lab_unit)
                            lab_unit = re.sub(r"krea", "", lab_unit)
                            lab_unit = re.sub(r"^mmol.?mol.?$", "mmol/mol", lab_unit)


                            # mm/h
                            lab_unit = re.sub(r"(^(m)?m(h)?/h$|^mh.?h$)", "mm/h", lab_unit)                    

                            # mgl
                            lab_unit = re.sub(r"^.?mg.?l$", "mg/l", lab_unit)

                            # GFR
                            lab_unit = re.sub(r"^ml/min.*", "ml/min/1.73m2", lab_unit)

                            # INR
                            lab_unit = re.sub(r"^inrarvo$", "inr", lab_unit)

                            # FEU
                            lab_unit = re.sub(r"^mg/lfeu$", "mg/l", lab_unit)


                            #mosm/kg20 - miliosmoles per kilogram of water
                            lab_unit = re.sub(r"^mo(l)?sm/kg.*$", "mosm/kgh2o", lab_unit)
                            
                            # Osuus
                            lab_unit = re.sub(r"(^tilo(s)?$|^(til)osuu(s)$)", "osuus", lab_unit)

                            # Counts
                            lab_unit = re.sub(r"(kopio(t)?(a)?|klp|sol(y|µ|u)|sol(y|µ|u)a|pisteet)", "kpl",lab_unit)

                            # Viewfield
                            lab_unit = re.sub(r"(n(ä)?kö(ke)?k(enttä|entt)?|s(y|µ)n(fält|f)?$)", "nk", lab_unit)

                            # Counts per viewfield
                            lab_unit = re.sub(r"(^(kpla)/nk|^kpl.?nk$|/nk$)", "kpl/nk", lab_unit)

                            # Tiiteri
                            lab_unit = re.sub(r"^.*ti(i)?t(t)?er(i)?.*$", "titre",lab_unit)

                            #Imuno assay
                            lab_unit = re.sub(r"^elia(u|µ)", "eliau",lab_unit)
                            lab_unit = re.sub(r"^eliau/m$", "eliau/ml",lab_unit)

                            lab_unit = re.sub(r"^a(u|µ)/ml$", "au/ml",lab_unit)

                            # f-calpro
                            lab_unit = re.sub(r"(gulos(t.*)$|gulo)", "gstool",lab_unit)
                            lab_unit = re.sub(r"((u|µ)g/g(\s+)?stool|(u|µ)g/g(f)?)", "µg/g",lab_unit)


                            # Promille
                            lab_unit = re.sub(r"(^promil(l)?$|^o/oo$)", "promille",lab_unit)

                            # Pos/Neg
                            lab_unit = re.sub(r"(^\-$|^negat$|^neg$)", "N",lab_unit)
                            lab_unit = re.sub(r"(^pos$|^\+$)", "A",lab_unit)

                            # Random
                            lab_unit = re.sub(r"^p.?g$", "pg", lab_unit)
                            lab_unit = re.sub(r"^f.?l$", "fl", lab_unit)
                            lab_unit = re.sub(r"\/\/", "/",lab_unit)
                            lab_unit = re.sub(r"(c)?aste(c)?", "aste",lab_unit)
                            lab_unit = re.sub(r"sek", "s",lab_unit)
                            lab_unit = re.sub(r"ve/", "responseequivalent/",lab_unit)
                            lab_unit = re.sub(r"^ve$", "responseequivalent",lab_unit)
                            lab_unit = re.sub(r"aru", "au",lab_unit)
                            lab_unit = re.sub(r"liter", "l",lab_unit)

                            # Days
                            lab_unit = re.sub(r"(/d$|/vrk$)", "/24h",lab_unit)

                            # Translations
                            lab_unit = re.sub(r"nk$", "field",lab_unit)
                            lab_unit = re.sub(r"kpl", "u",lab_unit) # kpl and counts often interchangeably used with u = unit

                            lab_unit = re.sub(r"(lausunto|lomake)", "form", lab_unit)
                            lab_unit = re.sub(r"indeksi", "index",lab_unit)
                            lab_unit = re.sub(r"arvio", "estimate",lab_unit)
                            lab_unit = re.sub(r"suhde", "ratio",lab_unit)
                            lab_unit = re.sub(r"krt", "times",lab_unit)

                            # Removing redundant and inconsistant information
                            lab_unit = re.sub(r"/100le(uk)$", "/100leuk",lab_unit)
                            lab_unit = re.sub(r"/l(/|)?(4|37c|ph7|ph74)+", "/l", lab_unit)
                            lab_unit = re.sub(r"nmol(bce)?/mmol", "nmol/mmol", lab_unit)


                            # Power changes
                            lab_unit = re.sub(r"^ku/l$", "u/ml", lab_unit)
                            lab_unit = re.sub(r"^pg/ml$", "ng/l", lab_unit)
                            lab_unit = re.sub(r"^(µ|u)g/ml$", "mg/l", lab_unit)

                            # All completley empty fields are NA
                            lab_unit = re.sub(r'(^\s+$|^$)', 'NA', lab_unit)

                            # Recording all unit changes
                            if lab_unit != line_arr[7].strip():
                                lab_abbrv = line_arr[5].strip()
                                orig_lab_unit = line_arr[7].strip()
                                fout_fix.write(lab_abbrv + "\t" + orig_lab_unit + "\t" + lab_unit + "\n")
                            
                        line_arr[7] = lab_unit.strip()

                else:
                    first_line = 0
                fout_min.write("\t".join(line_arr) + "\n")
