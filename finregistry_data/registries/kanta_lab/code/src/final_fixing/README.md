# Usage

```c
	cat file.tsv | exec/final_fixing <res_dir> <date> <ph_list_file_path> <title_list_file_path>
```

The input arguments need be appended in the correct order

* `res_dir`: Path to results directory
* `date`: Date of file
* `ph_list_file_path`: Path to the labs denoting pH tests
* `title_list_file_path`: Path to the labs denoting titles.

# Steps

1. **Fixes abnormality abbreviations** to be consistent with the standard definition see [AR/LABRA - Poikkeustilanneviestit](https://91.202.112.142/codeserver/pages/publication-view-page.xhtml?distributionKey=10329&versionKey=324&returnLink=fromVersionPublicationList). This means replacing
    * < with L, > with H, POS with A and NEG with N. 
    * If the abbreviation is not one of these, it is replaced with NA.
2. **Converting e6/l to e9/l** by dividing them by 1000 and changing the unit. To increase unity within the same measurements. Note that this is actually not implemented yet. (TODO).
3. **Fixes some of the units**
    * Removes units that are numbers 
    * Adds units for **INR**, and **pH** where they are almost always missing
        * Adds unit ph to a list of lab IDs, and abbreviation combos that are pH based on their OMOP mapping. The list is at `/data/xxxx`(TODO).
        * Adds unit to 4520 p-tt-inr, 4520 p-inr, 955 p-inr.
4. **Changes unit to `ordered` and removes the lab value for titles.** Titles are a set of lab measurements ordered together, here they often contain random information, probably from the children entries. Only information that is potentially reasonable is the abnormality. However, I wouldn't necessarily trust it. At the very least the information that this test has ben ordered can be preserved.The list of lab ID and abbreviation combos for titles is at `/data/xxxx`(TODO). - Note there currently is a bug in this. Instead of removing any data it adds pH to the units. (TODO)
5. **Removes data from years <2014 and >2022**
6. **Unifies all percentages and fractions to be in percentage.** Meaning, all entries with unit `osuus` (fraction) are multiplied by 100 and the unit is changed to `%`. For sometimes the percentage unit makes less sense logically. However, overall the data is preserved and for measurements where both fraction and percentage are used the data is unified this way.
7. **Removes illegal values**
    * Values that are not numbers - TODO is this actually a bug, i.e. do we have left or right censored values that are being removed in this way?
    * Negative values, except for the measurements with abbreviations: -h-ind, -ab-hb-met, xxxbe*, xxxvekaas*
8. **Removes measurements with measurement status D and P.** D stands for deleted information and P for a preliminary result. The entrie with missing information are kept. We have found that this increases the coverage across different areas of Finland. Indicating that the actual status is missing from specific providers.
9.**Moves all lab abnormality info to the lab value with unit `binary`**, in cases where this is the onl information we have. So `0` means normal and `1` abnormal.
