#include "../header.h"

/**
* @brief Takes the `all_minimal_omop.csv` file from std::cin and creates column tables
for each relevant column. 
* Needs the following arguments commandline arguments:
*    - file_name: The name of the file being read. Needed for the results file being descriptive.
*    - results_file_path: Path to the results directory.
* Example usages:
* @code
* cat all_minimal_omop.csv | ./col_tabs [file_name] [results_file_path]
* zstdcat all_minimal_omop.csv.zst | ./col_tabs [file_name] [results_file_path]
* @endcode
* Expects the columns to be FINREGISTRYID;DATE_TIME;service_provider_name;LAB_ID;LAB_ABBREVIATION;LAB_VALUE;LAB_UNIT;LAB_ABNORMALITY;OMOP_ID;OMOP_NAME;OMOP_ABBREVIATION;OMOP_UNIT
* Skips column tables for columns DATE_TIME, LAB_VALUE, and OMOP_NAME
* Expects the file delimeter to be ";".
**/
int main(int argc, char *argv[]) {
    std::string file_name = argv[1];
    std::string res_path = argv[2];

    // Defining result variables
    std::vector<std::string> col_names;
    // Table of each value for the different columns
    std::unordered_map<std::string, std::unordered_map<std::string, unsigned long long>> col_tables; 
    unsigned long long total_line_count = 0;

    // Reading in file from std::cin
    std::string line;
    while(std::getline(std::cin, line)) {
        // Split values and copy into resulting vector
        std::vector<std::string> line_vec = split(line, ";");
        // Column names
        if(total_line_count == 0) {
            // Copying the first line elements into the column names vector
            std::copy(line_vec.begin(), line_vec.end(), std::back_inserter(col_names));
        } else {
            update_col_tabs(line_vec, col_names, col_tables);
        }
        total_line_count++;
    }

    // Writing results
    omop_write_cross_tabs(col_tables, col_names, res_path, file_name);
}

