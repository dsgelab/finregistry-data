#include "header.h"

/**
 * @brief Writes update every 10000000 lines about how long the program has taken so far
 * 
 * @param n_lines Number of lines read so far
 * @param begin Time point when the program started
 * 
 * @return void
*/
void write_line_update(int n_lines, 
                       std::chrono::steady_clock::time_point &begin,
                       int line_limit) {
    if(n_lines % line_limit == 0) {
        std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();

        std::cout << "Lines read = " << n_lines << " Time took = " << std::chrono::duration_cast<std::chrono::minutes>(end - begin).count() << "[min]" << std::endl;
    } 
}

/**
 * @brief Writes end of run summary about how long the program has taken
 * 
 * @param begin Time point when the program started
 * 
 * @return void
*/
void write_end_run_summary(std::chrono::steady_clock::time_point &begin) {
    std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
    std::cout << "Time took = " << std::chrono::duration_cast<std::chrono::minutes>(end - begin).count() << "[minutes]" << std::endl;
    std::cout << "Time took = " << std::chrono::duration_cast<std::chrono::seconds>(end - begin).count() << "[seconds]" << std::endl;

}

/**
 * @brief Checks whether the std::ofstream is open
 * 
 * @param file_stream std::ofstream to be checked
 * @param file_path Path to the file
 * 
 * @return void
 * 
 * @note Exits the program if the file is not open and prints the error message.
*/
void check_out_open(std::ofstream& file_stream, 
                    std::string file_path) {
    if(!file_stream.is_open())  {
        std::vector<std::string> error_msg_vec = {"Error when opening ", file_path};
        std::string error_msg = concat_string(error_msg_vec);
        const char* error_msg_char = error_msg.c_str();
        perror(error_msg_char);
        exit(EXIT_FAILURE);
    }
}

/**
 * @brief Checks whether the std::ifstream is open
 * 
 * @param file_stream std::ifstream to be checked
 * @param file_path Path to the file
 * 
 * @return void
 * 
 * @note Exits the program if the file is not open and prints the error message.
*/
int check_in_open(std::ifstream &file_stream, 
                   std::string file_path,
                   int stop_if_not_open) {
    if(!file_stream.is_open())  {
        if(stop_if_not_open == 1) {
            std::vector<std::string> error_msg_vec = {"Error when opening ", file_path};
            std::string error_msg = concat_string(error_msg_vec);
            const char* error_msg_char = error_msg.c_str();
            perror(error_msg_char);
            exit(EXIT_FAILURE);
        } else {
            std::vector<std::string> error_msg_vec = {"Could not open ", file_path, " , skipping file."};
            return(0);
        }
    }
    return(1);
}

/**
 * @brief Learns the delimiter of a file
 * 
 * @param in_file File to be read
 * 
 * @return char Separator
*/
char find_delim(std::string file_path) {
    char delim;

    // Opening file
    std::ifstream in_file; in_file.open(file_path); check_in_open(in_file, file_path);
    std::string line;

    int n_lines = 0;
    int tabs_found = 0;
    int semicolons_found = 0;
    int commas_found = 0;

    while(std::getline(in_file, line)) {
        // Ignore lines that start with #

        if(line[0] != '#') {
            if(line.find('\t') != std::string::npos) tabs_found++;
            if(line.find(';') != std::string::npos) semicolons_found++;
            if(line.find(',') != std::string::npos) commas_found++;
        } 
        n_lines++;
        if(n_lines == 1000) break;
    }

    if((tabs_found > semicolons_found) & (tabs_found > commas_found)) {
        delim = '\t';
    } else if((semicolons_found > tabs_found) & (semicolons_found > commas_found)) {
        delim = ';';
    } else {
        delim = ',';
    }
    in_file.close();

    in_file.open(file_path); check_in_open(in_file, file_path);
    n_lines = 0;
    int first_line = 1;
    long unsigned int n_elems_per_line = 0;

    while(std::getline(in_file, line)) {
        // Ignore lines that start with #

        if(line[0] != '#') {
            std::vector<std::string> line_arr = splitString(line, delim);
            if(first_line == 1) {
                n_elems_per_line = line_arr.size();
                first_line = 0;
            } else {
                if(line_arr.size() != n_elems_per_line) {
                    std::cout << "Error: inconsistent number of elements in line " << n_lines << std::endl;
                    std::cout << "Using delimiter " << delim << std::endl;
                    std::cout << "Based on first line expected " << n_elems_per_line << " elements, got " << line_arr.size() << std::endl;
                    std::cout << "Current line: " << line << std::endl;
                    exit(EXIT_FAILURE);
                }
            }
        }
        n_lines++;
        if(n_lines == 1000) break;
    }

    in_file.close();
    return(delim);
}

std::string get_no_omop_header(char delim) {
    std::vector<std::string> header_vec = {"FINREGISTRYID", "LAB_DATE_TIME", "LAB_SERVICE_PROVIDER", "LAB_ID", "LAB_ID_SOURCE", "LAB_ABBREVIATION", "LAB_VALUE", "LAB_UNIT", "LAB_ABNORMALITY", "MEASUREMENT_STATUS", "REFERENCE_VALUE_TEXT", "DATA_SYSTEM", "DATA_SYSTEM_VERSION"};
    std::string header = concat_string(header_vec, std::string(1, delim));
    return(header);
}

std::string get_header(char delim) {
    std::vector<std::string> header_vec = {"FINREGISTRYID", "LAB_DATE_TIME", "LAB_SERVICE_PROVIDER", "LAB_ID", "LAB_ID_SOURCE", "LAB_ABBREVIATION", "LAB_VALUE", "LAB_UNIT", "OMOP_ID", "OMOP_NAME", "LAB_ABNORMALITY", "MEASUREMENT_STATUS", "REFERENCE_VALUE_TEXT", "DATA_SYSTEM", "DATA_SYSTEM_VERSION"};
    std::string header = concat_string(header_vec, std::string(1, delim));
    return(header);
}

std::string get_header_final(char delim) {
    std::vector<std::string> header_vec = {"FINREGISTRYID", "LAB_DATE_TIME", "LAB_SERVICE_PROVIDER", "LAB_ID", "LAB_ID_SOURCE", "LAB_ABBREVIATION", "LAB_VALUE", "LAB_UNIT", "OMOP_ID", "OMOP_NAME", "LAB_ABNORMALITY", "MEASUREMENT_STATUS", "REFERENCE_VALUE_TEXT"};
    std::string header = concat_string(header_vec, std::string(1, delim));
    return(header);
}