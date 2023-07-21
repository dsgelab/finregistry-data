#include "../header.h"

/***
 *  @brief Updates the column tables for each column
 * 
 *  @param line The current line of the file in vector form
 *  @param col_names The column header names
 *  @param col_tables The column tables
 *  
 *  @return void
 * 
 * Expects the columns to be FINREGISTRYID;DATE_TIME;service_provider_name;LAB_ID;LAB_ABBREVIATION;LAB_VALUE;LAB_UNIT;LAB_ABNORMALITY;OMOP_ID;OMOP_NAME;OMOP_ABBREVIATION;OMOP_UNIT
 * Skips column tables for columns DATE_TIME, LAB_VALUE, and OMOP_NAME
*/
void update_col_tabs(std::vector<std::string> line,
                       std::vector<std::string> &col_names,
                       std::unordered_map<std::string, std::unordered_map<std::string, unsigned long long>> &col_tables) {

    for(long unsigned int col_idx=0; col_idx < col_names.size(); col_idx++) {
        std::string col_name = col_names[col_idx];
        std::string col;

        switch(col_idx) {
            case 1: case 5: case 9:
                break;
            default:
                col = line[col_idx];
        }
        if(col_tables[col_name].count(col) != 1){
            col_tables[col_name][col] = 1;
        } else {
            col_tables[col_name][col]++;
        }
    }
}