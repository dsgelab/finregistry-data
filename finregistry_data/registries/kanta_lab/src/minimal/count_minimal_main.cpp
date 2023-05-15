#include "../header.h"

int main(int argc, char *argv[]) {
     // File and delimiter
    const char *delim = ";";
    // Defining zero as reading whole file here
    unsigned long long n_rows = 0;
    int n_cols = 15;

    std::string file_path = argv[1];
    std::string res_path = argv[3];


    // Opening
    std::vector<std::string> report_path_vec = {res_path, "processed/reports/counts/all_minimal_col_tabs.csv"};    
    std::string report_path = concat_string(report_path_vec, std::string(""));
    std::ifstream in_file;
    in_file.open(file_path); 
    check_in_open(in_file, file_path); 


    // Defining result variables
    std::vector<std::string> col_names;
    // Table of each value for the different columns
    std::unordered_map<std::string, std::unordered_map<std::string, unsigned long long>> col_tables; 
    unsigned long long line_count = 0;
    unsigned long long total_line_count = 0;

    int skip_count = 0;
    // Reading file line by line
    std::string line;
    while(std::getline(in_file, line)) {
        // Split values and copy into resulting vector
        std::vector<std::string> line_vec = split(line, delim);
        if(int(line_vec.size()) == n_cols)  {
            // Column names
            if(line_count == 0) {
                // Copying the first line elements into the column vector
                std::copy(line_vec.begin(), line_vec.end(), std::back_inserter(col_names));
            } else {
                update_col_tabs(line_vec, col_names, col_tables);
            }
            line_count++;
            total_line_count++;
        } else {
            cout << "Skipping line: " << total_line_count << " size: " << line.size() << " no of columns: " << line_vec.size() << " " << line << endl;
            skip_count++;
            total_line_count++;
        }
    }
    cout << "line number: " << line_count << " closing" << endl;
    cout << "skipped: " << skip_count << endl;
    // Closing
    in_file.close();
    error_file.close();
    // Writing results
    omop_write_cross_tabs(col_tables, col_names, n_cols, res_path, file_name);
}

