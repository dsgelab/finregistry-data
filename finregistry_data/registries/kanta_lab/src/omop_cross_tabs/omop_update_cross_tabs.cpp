#include "../header.h"

/**
 * @brief Creates cross tables between Lab and OMOP
 * 
 * @param line The current line of the file in vector form
 * @param col_names The column header names
 * @param col_tables The column tables
 *  
 * @return void
 * 
 * Creates cross tables:
 *  - LAB_ID vs OMOP_ID
 *  - OMOP_ID vs OMOP_ABBREVIATION, LAB_VALUE, OMOP_UNIT, service_provider_name
 *  - LAB_ABBREVIATION vs OMOP_ABBREVIATION
 *  - LAB_UNIT vs OMOP_UNIT
*/
void omop_update_cross_tabs(std::vector<std::string> line,
                            std::vector<std::string> &col_names,
                            std::unordered_map<std::string, std::unordered_map<std::string, unsigned long long>> &col_tables) {

    for(long unsigned int col_idx=0; col_idx < col_names.size(); col_idx++) {
        std::string col_name = col_names[col_idx];
        std::string col;
        // All column elements for better readability
        std::string finregistryid = line[0];
        std::string date_time = line[1];
        std::string service_provider_name = line[2];
        std::string lab_id = line[3];
        std::string lab_id_source = line[4];
        std::string lab_abbreviation = line[5];
        std::string lab_value = line[6];
        std::string lab_unit = line[7];
        std::string lab_abnormality = line[8];
        std::string omop_id = line[9];
        std::string omop_name = line[10];
        std::string omop_unit = line[11];

        switch(col_idx) {
            case 9: // OMOP_ID
                {std::vector<std::string> tab_elems{lab_id, omop_id};
                col = concat_string(tab_elems, "\t");
                break;}
            case 10: // OMOP_NAME
                {std::vector<std::string> tab_elems{omop_id, omop_name, lab_value, omop_unit, service_provider_name};
                col = concat_string(tab_elems, "\t");
                break;}
            case 11: // OMOP_UNIT   
                {std::vector<std::string> tab_elems{lab_unit, omop_unit, omop_id};
                col = concat_string(tab_elems, "\t");
                break;}
            case 0: case 1: case 2: case 3: case 4: case 5: case 6: case 7: case 8:
                break;
        }
        if(col_tables[col_name].count(col) != 1){
            col_tables[col_name][col] = 1;
        } else {
            col_tables[col_name][col]++;
        }
    }
}