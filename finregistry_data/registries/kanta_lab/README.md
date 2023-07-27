# Overview

These are various C++ programs for working with the Kanta lab data files.

# Creating Minal File
Reduces the original files to a single file with columns
#### Creates a new file with columns
  1. `FINREGISTRYID` - Pseudoanonimized IDs
  2. `DATE_TIME` - Date and time of lab measurement
  3. `SERVICE_PROVIDER` - Service provider string based on OID mapped to city
  4. `LAB_ID` - Regional or local lab ID
  5. `LAB_ID_SOURCE` - Source of lab ID 0: local 1: regional
  6. `LAB_ABBREVIATION` - Laboratory abbreviation from data (local) or mapped using the THL map (regional)
  7. `LAB_VALUE` - The value of the laboratory measurement
  8. `LAB_UNIT` - The unit from the file
  9. `LAB_ABNORMALITY` - The abnormality of the measurement i.e. high, low, positive, negative. A lot of missingness
## Usage
```
for file_no in 1:10:
  cat finregistry_[file_no].csv.finreg_ID | exec/minimal [res_path] [file_no] [thl_sote_fix_name_map.tsv] [lab_id_map.tsv]
```

## Current Pipeline

### Reading Files
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

### For each line from std::cin
#### Creates a new file with columns
  0. `FINREGISTRYID` - Pseudoanonimized IDs
  1. `DATE_TIME` - Date and time of lab measurement
  2. `SERVICE_PROVIDER` - Service provider string based on OID mapped to city
  3. `LAB_ID` - Regional or local lab ID
  4. `LAB_ID_SOURCE` - Source of lab ID 0: local 1: regional
  5. `LAB_ABBREVIATION` - Laboratory abbreviation from data (local) or mapped using the THL map (regional)
  6. `LAB_VALUE` - The value of the laboratory measurement
  7. `LAB_UNIT` - The unit from the file
  8. `LAB_ABNORMALITY` - The abnormality of the measurement i.e. high, low, positive, negative. A lot of missingness
#### Steps
1. Reads in line a splits, using ";" - See function `read_correct_lines`
    - Checks if the line has 25 columns
    - If not tries to concatenate with next line to see if it was an early line break
    - If not checks if the next line is well defined 
    - Writes badly defined lines to a file `[res_path]/processed/reports/problem_rows/problem_rows_file_[file_no].csv`
2. Turns all NA markers to actual NAs in the data 
    - `Puuttuu`, `""`, `THYJÄ`, `_`, `-1` (except in value column
3. Columns directly copied from the data:
```c
std::string finregistry_id = final_line_vec[1];
std::string date_time = final_line_vec[11];
std::string lab_value = final_line_vec[19];
std::string lab_unit = final_line_vec[20];
std::string lab_abnormality = final_line_vec[22];
```    
4. Lab IDs, depending on data
  - If we have both the code and name -> local lab ID, source = 0
  - If we have only the code -> regional lab ID, source = 1
5. Getting abbreviations for regional lab ID, using `thl_abbrv_map`
6. Getting THL SOTE organisation string, using ``thl_sote_map`
7. Creating duplicate line string 
```c
std::vector<std::string> dup_vec = {finregistry_id, date_time, service_provider_name, lab_id, lab_abbrv, lab_value, lab_unit};
std::string dup_line = concat_string(dup_vec, std::string("")); 
```
8. Adding only non-duplicate lines to the file
9. Adding line to duplicate line map `all_dup_lines`
10. Adding lines with neither lab value, nor lab abnormality information to a file `[res_path]/processed/reports/problem_rows/missing_data_rows_file_[file_no].csv

## Steps left to do
- Provide all maps
  - Preprocessing of THL SOTE or provide map
  - THL lab ID map easy to access
- Share binary
- File to run ./minimal on all files and then concatenate to one `all_minimal.tsv` file

## Important
- Currently the process takes a lot of space before compression (over 100GB)
  - It is in principal possible to skip all the error file creations if necessary to save some space. However, this still needs to be implemented
