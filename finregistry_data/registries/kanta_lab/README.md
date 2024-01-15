# Table of Contents

- [Using the Final Data](#final_cols)
  - [Columns](#final_cols)
  - [Important Notes](#final_notes)
    - [Service Providers](#provider)
    - [Lab IDs and abbreviations](#ids)
    - [Units](#units)
  - [How to Best Use the Data](#best_use)
  - [Known Bugs](#bugs)
- [This Repo](#repo)
  - [Usage](#repo)
  - [Processing Pipeline](#pipe)

# Using the Final Data

The current processed version of the kanta lab  v2 - 2023-12-12 has the following 11 columns

<a name="final_cols">

## Columns

| #   | Column Name | Easy Description | General Notes | Technical Notes |
| --- | --- | --- | --- | --- |
| 1   | `FINREGISTRYID` | Pseudoanonimized IDs |     |     |
| 2   | `LAB_DATE_TIME` | Date and time of lab measurement |     |     |
| 3   | `LAB_SERVICE_PROVIDER` | Service provider | This is NOT the lab performing the test but the service provider that ordered the test see Section [Important Notes](#final_notes) for more details. | The original data contains uses OIDs  ([OID-yksilöintitunnukset](https://thl.fi/aiheet/tiedonhallinta-sosiaali-ja-terveysalalla/ohjeet-ja-soveltaminen/koodistopalvelun-ohjeet/oid-yksilointitunnukset)). These were mapped to a readable string based on the city where the service provider is registered i.e. *HUS is mapped to Helsinki_1301*. The map is at [upload/data/thl\_sote\_map_named.tsv](https://github.com/detroiki/kanta_lab/blob/main/upload/data/thl_sote_map_named.tsv) and based on [THL - SOTE-organisaatiorekisteri 2008](https://koodistopalvelu.kanta.fi/codeserver/pages/classification-view-page.xhtml?classificationKey=421&versionKey=501). |
| 4   | `LAB_ID` | National (THL) or local lab ID of the measurement |     |     |
| 5   | `LAB_ID_SOURCE` | Source of the lab ID | 0: local and 1: national (THL) |     |
| 6   | `LAB_ABBREVIATION` | Laboratory abbreviation of the measurement from the data (local) or mapped using the THL map (national) |     | The map for the national (THL) IDs is at  [upload/data/thl\_lab\_id\_abbrv\_map.tsv](https://github.com/detroiki/kanta_lab/blob/main/upload/data/thl_lab_id_abbrv_map.tsv),  and was downloaded from [Kuntaliitto - Laboratoriotutkimusnimikkeistö](https://koodistopalvelu.kanta.fi/codeserver/pages/classification-view-page.xhtml?classificationKey=88&versionKey=120) |
| 7   | `LAB_VALUE` | The value of the laboratory measurement |     |     |
| 8   | `LAB_UNIT` | The unit of the labroatroy measurement from the data |     |     |
| 9   | `OMOP_ID` | OMOP concept ID of the lab measurement | For more details about the lab measurements see Sections \[Mapping to OMOP\](#omop)[](#) | Mapped using the lab ID and the lab abbreviation (not the unit) at [upload/data/omop\_concept\_map.tsv](https://github.com/detroiki/kanta_lab/blob/main/upload/data/omop_concept_map.tsv) |
| 10  | `OMOP_NAME` | Name of the OMOP concept |     |     |
| 11  | `LAB_ABNORMALITY` | Abnormality of the lab measurement | Describes whether the test is result is normal or abnormal i.e. too high or low low based on the laboratories reference values. This is **not** a quality control variable but to state it simply and inaccurately denotes whether the patient is healthy or not. See [AR/LABRA - Poikkeustilanneviestit](https://91.202.112.142/codeserver/pages/publication-view-page.xhtml?distributionKey=10329&versionKey=324&returnLink=fromVersionPublicationList) for the abbreviations meanings. | The column contains a lot of missingness. |
| 12  | `MEASUREMENT_STATUS` | The measurement status | The final data contains only `C` \- corrected results or `F` \- final result | See [Koodistopalvelu - AR/LABRA - Tutkimusvastauksien tulkintakoodit 1997](https://koodistopalvelu.kanta.fi/codeserver/pages/publication-view-page.xhtml?distributionKey=2637&versionKey=321&returnLink=fromVersionPublicationList) |
| 13  | `REFERENCE_VALUE_TEXT` | The reference values for the measurement in text form | This can be used to define the lab abnormality with better coverage using regex expressions (-to be implemented for the whole data). |     |

<a name="final_notes">

## Important notes

<a name="provider">
  
### Service Providers:

We **do not have any information on the actual lab performing the tests**, instead we can only know which service provider has ordered the tests. However, there are not too many labs and service providers in Finland so this column could likely still be used for some quality control purposes.

<a name="ids">

### Lab IDs and abbreviations

Some labs use the national lab IDs. However, **each lab can use their own unique lab ID and abbreviation** to describe the lab measurement. Additionally, different lab tests can sometimes be considered equivalent, i.e. plasma and serum based measurements.

- For this reason **it is recommended to use the OMOP IDs to find all measurements**, unless you have expert opinions on which lab IDs and abbreviations to use.
- **At this time we do not know all local lab IDs**, some of the lab IDs learned from the data have been added to the mapping based on their lab abbreviations. See Section \[\](). Overall this increases the OMOP mapping to about 93% of the data.

<a name="units">

### Units:

The units in the final data are from the data and **do not necessarily map to the assigned OMOP concepts**. Each lab measurement typically has 1-2 most common units. The rest of the data might be either very rarely used units or typos.

**Special units** have been added for some inconsistencies in the data.

- **The unit `binary`** denotes test results that contain not lab value and but only 0: normal and 1: abnormal. These are either binary tests, such as covid tests or measurements where the lab value is missing and we only know whether the result was normal or abnormal.
- **The unit `ordered`** denotes tests that are titles where multiple tests are ordered together, i.e. 2475 b-pvk+tkd - Short blood count panel - Blood.

<a name="best_use">

### How to Best Use the Data
For the reasons behind each step see the previous section.

***Use Case: Single measurement of interest***

1.  Find the OMOP concept ID for the measurement
    - see [athena.ohdsi.org](https://athena.ohdsi.org/search-terms/start), ask Kira (kira.detrois at helsinki.fi) for the summary statistics or simply use the data
2.  Filter the data based on the OMOP ID
3.  Filter the data for the top (1-2) most commonly used units
    - Either remove the rest of the data or fix obvious typos
4.  Have fun! :smiley:

<a name="bugs">

### Known Bugs

- The label ordered is actually currently not in use. This has been fixed for future versions.

<a name="repo">


# This Repo

This repo contains various C++ programs (and one python file) for processing the original Kanta lab files.

## Usage

The whole pipeline can be easily run by simply uploading the directory `upload` to your environment a **replacing the paths for the results directory (`res_dir`)** and the **original data directory (`data_dir`)** in the
Makefile. **Additionally, you will need to activate a python environment with packages: csv, re, sys, time, and collections, for the unit fixing step.**

Then run

```
make run_all
```

This will run all the steps in the pipeline and create all the necessary folders and files.

The pipeline can also be run step by step. See the Makefile for the exact commands and steps.

<a name="pipe">

## Pipeline
- [Creating Minimal File](#minimal)
- [Mapping OMOP](#omop)
- [Unit Fixing](#unit)
- [Final Fixing](#final)

  
<a name="minimal">
  
### Creating Minimal File

Reduces the original files by selecting only the most relevant columns and performs small quality control measurements.

See the minimal README located at [code/src/minimal](https://github.com/dsgelab/finregistry-data/tree/main/finregistry_data/registries/kanta_lab/code/src/minimal) for a detailed description of all steps performed.

<a name="omop"/>

### Mapping OMOP

Maps the OMOP concepts, using both the lab ID and abbreviation map. We can map about 60% of the local lab IDs and 78.6% of the data this way. 

The lab ID and abbreviations are mapped to the correct source table, if possible and otherwise hierarchical to the best matching source table. The four tables are LABfi the nation wide table, LABfi_HUS the HUS table, LABfi_TMP the Tampere table, and LABfi_TKU the Turku table. The hierarchy for local lab IDs from non-major hospitals is HUS, TMP, TKU.

<a name="unit">

## Unit Fixing

This is implemented in pyhton, using regex. Fixes include:

- Turning empty units to NAs
- Fixing and unifying all `10e5`, `10^9` etc. to one form `e5`, `e9` etc.
- Fixing and unifying all forms of `(y|μ)ks(ikkö)` to `u`
- Fixing and unifying all forms of `kopio(t), sol(y|μ|u), kpl, pisteet` to `count`.
- Fixing and unifying all `n(ä)kö(ke)k(enttä)`to `field`
- Fixing and unifying all `gulost` and `gstool` to `g`, since the fact that it is `g stool`is clear from the measurement.
- Fixing and unfiying all `(til)osuus` to `osuus`. 
- Fixing and unifying all `tiiteri` to `titer`.
- Fixing and unifying all `mosm/kg` to `mosm_kgh2o`.
- Fixing and unifying all `inrarvo` to `inr`.
- Fixing and unifying all `ml/min/(173m2)` to `ml/min/173m2`.
- Fixing all missing or wrong `/`, this can include i.e. `7`.
- Fixing typos, such as `mot` instead of `mol` and `mmmol` instead of `mmol`.
- Changing `umol` to `μmol` and `ug/l` to `μg/l`.
- Making `+` and `pos` to `A` and `-` and `neg(at)` to `N`.
- Making `o/oo` to `promille`.
- Making `/d`, and `/vrk` to `/24h`.
- Removing information such as the degree and ph, i.e. `mg/l/37c` simply becomes `mg/l`. These are typically already unified in the concepts and only irregularly denoted in the unit.
- Removing information `/100leuk`and `/24h` for the same reason as above.
- Making power changes for `ku/l`to `u/ml`, `pg/ml` to `ng/l`, `μg/l` to `ng/ml`, `μg/ml` to `mg/l`.

For all regex commands see: [code/src/unit_fixing.py](https://github.com/dsgelab/finregistry-data/tree/main/finregistry_data/registries/kanta_lab/code/src/unit_fixing.py)

<a name="final">

## Final Fixing

1. **Fixes abnormality abbreviations** to be consistent with the standard definition see [AR/LABRA - Poikkeustilanneviestit](https://91.202.112.142/codeserver/pages/publication-view-page.xhtml?distributionKey=10329&versionKey=324&returnLink=fromVersionPublicationList). This means replacing
    * < with L, > with H, POS with A and NEG with N. 
    * If the abbreviation is not one of these, it is replaced with NA.
2. **Converting e6/l to e9/l** by dividing them by 1000 and changing the unit. To increase unity within the same measurements. Note that this is actually not implemented yet. (TODO).
3. **Fixes some of the units**
    * Removes units that are numbers 
    * Adds units for **INR**, and **pH** where they are almost always missing
        * Adds unit ph to a list of lab IDs, and abbreviation combos that are pH based on their OMOP mapping. The list is at `/data/xxxx`(TODO, for now ask Kira if you end up needing it.).
        * Adds unit to 4520 p-tt-inr, 4520 p-inr, 955 p-inr.
4. **Changes unit to `ordered` and removes the lab value for titles.** Titles are a set of lab measurements ordered together, here they often contain random information, probably from the children entries. Only information that is potentially reasonable is the abnormality. However, I wouldn't necessarily trust it. At the very least the information that this test has ben ordered can be preserved. The list of lab ID and abbreviation combos for titles is at `/data/xxxx`(TODO, for now ask Kira if you end up needing it). - Note there currently is a bug in this. Instead of removing any data it adds pH to the units. (TODO, for now ask Kira if you end up needing it.)
5. **Removes data from years <2014 and >2022**
6. **Unifies all percentages and fractions to be in percentage.** Meaning, all entries with unit `osuus` (fraction) are multiplied by 100 and the unit is changed to `%`. For sometimes the percentage unit makes less sense logically. However, overall the data is preserved and for measurements where both fraction and percentage are used the data is unified this way.
7. **Removes illegal values**
    * Values that are not numbers - TODO is this actually a bug, i.e. do we have left or right censored values that are being removed in this way?
    * Negative values, except for the measurements with abbreviations: -h-ind, -ab-hb-met, xxxbe*, xxxvekaas*
8. **Removes measurements with measurement status D and P.** D stands for deleted information and P for a preliminary result. The entrie with missing information are kept. We have found that this increases the coverage across different areas of Finland. Indicating that the actual status is missing from specific providers.
9.**Moves all lab abnormality info to the lab value with unit `binary`**, in cases where this is the onl information we have. So `0` means normal and `1` abnormal.
 ## Learning New OMOP Concepts

Adds OMOP IDs to lab IDs that are unknown but occur at least 1000 times with lab abbreviations that can be mapped to the OMOP ID. The list of new omop concepts can be found here: [upload/data/new_omop_mappings.tsv](https://github.com/dsgelab/finregistry-data/tree/main/finregistry_data/registries/kanta_lab/upload/data/new_omop_mappings.tsv).
