#include "../header.h"

/**
 * @brief Writes the column tables to files
 * 
 * @param col_tables The column tables for each column
 * @param col_names The column names
 * @param res_path The path to the results folder
 * @param file_name The name of the file
 * 
 * @return void
 * 
 * **/
void omop_write_cross_tabs(std::unordered_map<std::string, std::unordered_map<std::string, unsigned long long>> col_tables,
                       std::vector<std::string> col_names,
                       std::string res_path,
                       std::string file_name) {
    // Going through each column in the file
    for(auto col_name: col_names) {
        // Checking if we made a table of the column
        if(col_tables[col_name].size() > 1) {
            // Results file path
            std::vector<std::string> full_res_path_vec = {res_path, "processed/reports/counts/col_counts/", file_name, "_", col_name, "_table.tsv"};
            std::string full_res_path = concat_string(full_res_path_vec);

            // Opening file
            std::ofstream res_file;
            res_file.open(full_res_path); check_out_open(res_file, full_res_path);
            
            // Writing
            res_file << col_name << "\tCOUNT\n"; 
            for(const std::pair<const std::string, unsigned long long>& elem: col_tables[col_name]) {
                res_file << elem.first << "\t" << elem.second << "\n";
            }

            // Closing
            res_file.close();
        }
    }
}
