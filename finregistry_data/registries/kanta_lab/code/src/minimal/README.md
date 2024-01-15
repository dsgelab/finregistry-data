# Table of Contents
- [Usage](#run)
- [All Steps](#read)
   - [Reading](#read)
   - [For each line from std::cin](#in)
   - [Creates a new file with columns](#new)
- [Extra Files Created](#important)
   -  [Duplicates](#dup)
   -  [Removed Lines](#rem)
- [Expected Columns](#expect)

<a name="run">
 
# Usage

```c
cat finregistry_[file_no].csv.finreg_ID | exec/minimal [res_path] [file_no] [date] [data/thl_sote_fix_name_map.tsv] [data/lab_id_map.tsv] [write_reports]
```

The input arguments need be appended in the correct order

* `res_path`: Path to results directory
* `file`: File number
* `date`: Date of file
* `thl_sote_path`: Path to THL SOTE organisations name map `data/thl_sote_organisations.tsv`
* `thl_abbrv_path`: Path to official abbreviations map `data/thl_lab_id_abbrv_map.tsv`
* `write_reports`: Wheter to write report or not, either "True" or "False"
  
 <a name="important">

# All Steps

<a name="read">

## Reading Files

1. Reads in duplicate lines from all previous files 
```c
std::unordered_map<std::string, int> all_dup_lines; # Counts number of times the duplicate lines appear in the current file
```
2. Reads in the [THL SOTE Organisation](https://thl.fi/fi/web/tiedonhallinta-sosiaali-ja-terveysalalla/ohjeet-ja-soveltaminen/koodistopalvelun-ohjeet/sote-organisaatio-rekisteri) map 
  - Created by mapping each organisations OID to shorter strings which are based on the the city 
  -` Example: 1.2.246.10.1739.4173.10.1 mapped to Helsinki_1301 is HUS
```c
std::unordered_map<std::string, std::string> thl_sote_map;
```
3. Reads in the official [THL Koodistopalvelu regional lab IDs map to abbreviations](https://koodistopalvelu.kanta.fi/codeserver/pages/classification-view-page.xhtml?classificationKey=88&versionKey=120)
  - Example: 
  
  ![image](https://user-images.githubusercontent.com/56593546/235346446-813e5adb-0199-4c15-ac6d-4b6585ff90d0.png)
  
```c
    std::unordered_map<std::string, std::string> thl_abbrv_map;
``` 

<a name="in">

## For each line from std::cin
   
1. Reads line and splits using "\t" - Removes all spaces from each columns data.
2. Turns all NA markers to actual NAs in the data 
    - `Puuttuu`, `""`, `THYJÄ`, `_`, `-1` (except in value column), `NA`, `NULL`
3. Skips rest and writes line to error file if:
    - current hetu root is not `1.2.246.21` (they are manually assigned hetus),
    - or the measurement status is  `K`, `W`, `X`, or `I` (unfinished, wrong, no result, sample in the lab waiting for result). 
4. Creates duplicate row vector and skips the row if already in duplicate line map.
   ```c
      std::vector<std::string> dup_vec = {finregid, lab_date_time, service_provider_oid, lab_id, local_lab_abbrv, lab_value, lab_unit};
   ```
5. Lab IDs and abbreviations come from the two columns
    * `labooratoriotutkimusoid` 
         * THL - lab ID source: 0
         * lab abbreviation from THL abbreviation map in `data/thl_lab_id_abbrv_map.tsv`
    * `paikallinentutkimusnimikeid`
         * Local - lab ID source: 1
         * lab abbreviation from column `paikallinentutkimusnimike`
 ```c
    std::string local_lab_abbrv = remove_chars(line_vec[31], ' ');
    std::string local_lab_id = remove_chars(line_vec[32], ' ');
    std::string thl_lab_id = remove_chars(line_vec[0], ' ');
   ```
7. Gets a readable service provider name from the THL SOTE organisation map.
8. Removes all " characters from the data
9. Checks that the lab value or abnormality and the lab ID are not missing
    - If they are, writes the line to the missing data file and skips the line.
10. Adds the line to the duplicate line map
11. Creates output vector and writes it to a tab separated file
```c
std::vector<std::string> final_line_vec = {finregid, lab_date_time, service_provider_name, lab_id, lab_id_source, lab_abbrv, lab_value, lab_unit, lab_abnormality, measure_stat, ref_value_text, data_system, data_system_ver};
```

Columns directly copied from the data:
```c
std::string finregid = remove_chars(line_vec[4], ' ');
std::string lab_date_time = remove_chars(line_vec[11], ' ');
std::string service_provider_oid = remove_chars(line_vec[28], ' ');
std::string measure_stat = remove_chars(line_vec[34], ' ');
std::string lab_value = remove_chars(line_vec[35], ' ');
std::string lab_unit = remove_chars(line_vec[36], ' ');
std::string lab_abnormality = remove_chars(line_vec[37], ' ');
std::string ref_value_text = remove_chars(line_vec[44], ' ');
std::string data_system = remove_chars(line_vec[18], ' ');
std::string data_system_ver = remove_chars(line_vec[20], ' ');
```
### Writing
1. Writes a row count report about the total number of lines, as well as the number of
      - Usable rows written to the output file
      - The number of duplicate rows encountered in this file
      - The number of rows with missing data
      - The number of rows with bad measurement status
      - The number of rows with not-official hetus.
2. Writes all duplicate rows newly encountered in this file to
   `<res_path>processed/reports/problem_rows/duplines_<file_no>_<date>.tsv}`
<a name="new">
   
## Creates a new file with columns

  1. `FINREGISTRYID` - Pseudoanonimized IDs
  2. `LAB_DATE_TIME` - Date and time of lab measurement
  3. `LAB_SERVICE_PROVIDER` - Service provider string based on OID mapped to city
  4. `LAB_ID` - Regional or local lab ID
  5. `LAB_ID_SOURCE` - Source of lab ID 0: local 1: national
  6. `LAB_ABBREVIATION` - Laboratory abbreviation from data (local) or mapped using the THL map (national)
  7. `LAB_VALUE` - The value of the laboratory measurement
  8. `LAB_UNIT` - The unit from the file
  9. `LAB_ABNORMALITY` - The abnormality of the measurement i.e. high, low, positive, negative. A lot of missingness
  10. `MEASUREMENT_STAUTS`- The measurement status, i.e. C - corrected results or F - final result. See [Koodistopalvelu - AR/LABRA - Tutkimusvastauksien tulkintakoodit 1997](https://koodistopalvelu.kanta.fi/codeserver/pages/publication-view-page.xhtml?distributionKey=2637&versionKey=321&returnLink=fromVersionPublicationList).
  11. `REFERENCE_VALUE_TEXT`- The reference values for the measurement in text form.
  12. `DATA_SYSTEM` - Data system used to store the information.
  13. `DATA_SYSTEM_VERSION` - Version of the data system used.

 
 # Extra Files Created

 <a name="dup">
  
 ## Duplicates
 A duplicate is defined if all of the following data is the same: 
 
 1. Finregistry ID
 2. Date and time
 3. Service provider organization
 3. Laboratory test name ID
 4. Laboratory test name abbreviation
 5. Test result value
 6. Test result unit

Lines occuring in a specific file are written to `<res_path>processed/reports/problem_rows/duplines_<file_no>_<date>.tsv`

<a name="rem">

 ## Removed lines

 Removed lines are directly written to a file located at 
 `<res_dir>/problem_rows/problem_rows_file_<file_no>_<date>.tsv`, if the `write_reports` argument is set to `True`.
 
 Lines are removed if they have:
 * Hetu roots that are not `1.2.246.21` (they are manually assigned hetus).
 * A measurement status of `K`, `W`, `X`, or `I` (unfinished, wrong, no result, sample in the lab waiting for result).
 
 Lines with no information about the lab value and abnormality or
 a missing Lab ID are removed and if the `write_reports` argument is set to True,
 written to a file located at
 `<res_dir>/problem_rows/missing_data_rows_file_<file_no>_<date>.tsv`,


<a name="expect">

# Expected columns
 1. `laboratoriotutkimusoid` - Laboratory test OID
 2. `asiakirjaoid` - Document OID
 3. `merkintaoid` - Note OID
 4. `entryoid` - Entry OID
 5. `potilashenkilotunnus` - Finregistry ID
 6. `palvelutapahtumatunnus` - Service event ID
 7. `tutkimuksennaytelaatu` - Measurement
 8. `tutkimuksentekotapa` - Test method
 9. `potilassyntymaaika_pvm` - Patient birth date
 10. `potilas_sukupuoli` - Patient sex
 11. `labooratoriotutkimusoid` - Laboratory test OID
 12. `tutkimusaika` - Test time
 13. `alkuperainenasiakirjaoid` - Original document OID
 14. `asiakirjaversio` - Document version
 15. `rekisterinpitaja_organisaatio_h` - Registry controller organisation ID
 16. `rekisterinpitaja_h` -  Registry organisation ID
 17. `asiakirjavalistilapk` - Document status
 18. `marittelykokoelmaoid` - Collection OID
 19. `tietojarjestelanimi` - Data system name
 20. `tietojarjestelavalmistaja` - Data system manufacturer
 21. `tietojarjestelaversio` - Data system version
 22. `asiajirjaluontiaika` - Document creation time
 23. `pal_alkuperainenasiakirjaoid` - Original document OID
 24. `pal_asiakirjaversio` - Document version
 25. `pal_ariakirjaoid` - Document OID
 26. `pal_asiakirjaversio` - Document version
 27. `rekisterinpitaja_organisaatio` - Registry controller organisation ID
 28. `rekisterinpitaja` -  Registry organisation ID
 29. `palveluntuottaja_organisaatio` - Service provider organisation ID
 30. `palveluisanta_organisaatio` - Service host organisation ID
 31. `hetu_root` - Finregistry ID root
 32. `paikallinentutkimusnimike` - Local test name
 33. `paikallinentutkimusnimikeid` - Local test name ID
 34. `tutkimuskoodistonjarjestelmaid` - Test code system ID
 35. `tutkimuksenvastauksentila` - Test result status
 36. `tutkimustulosarvo` - Test result value
 37. `tutkimustulosyksikkö` - Test result unit
 38. `tuloksenpoikkeavuus` - Test result abnormality
 39. `tuloksenvalmistumisaika` - Test result time
 40. `viitearvoryhma` - Reference value group
 41. `viitevalialkuarvo` - Reference value lower limit
 42. `viitevalialkuarvoyksikko` - Reference value lower limit unit
 43. `viitevaliloppuarvo` - Reference value upper limit
 44. `viitevaliloppuarvoyksikko` - Reference value upper limit unit
 45. `viitearvoteksti` - Reference value text
 46. `erikoisalalyhenne` - Speciality abbreviation
 
