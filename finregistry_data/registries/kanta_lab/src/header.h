#include <fstream>
#include <sstream>
#include <iostream>
#include <string>
#include <vector>
#include <regex>
#include <unordered_map>
#include <unordered_set>

using namespace std;

// Helper functions
std::vector<std::string> split(const std::string &s, const char *delim);
std::string concat_string(std::vector<std::string> elems, std::string sep = std::string(""));
void check_out_open(std::ofstream &file_stream, std::string file_path);
void check_in_open(std::ifstream &file_stream, std::string file_path);

// Helper functions for minimal file creation
void fix_nas(std::vector<std::string> &final_line_vec);
std::string get_service_provider_name(std::unordered_map<std::string, std::string> &thl_sote_map,
                               std::string &service_provider_oid);
void get_lab_id_and_source(std::string &local_lab_id,
                           std::string &thl_lab_id,
                           std::string &lab_id,
                           std::string &lab_id_source);
std::string get_lab_abbrv(std::unordered_map<std::string, std::string> thl_abbrv_map,
                          std::string &lab_id,
                          std::string &lab_id_source,
                          std::string &lab_name);
void write_row_count_report(std::string &report_path,
                            unsigned long long &total_line_count,
                            unsigned long long &valid_line_count,
                            unsigned long long &skip_count,
                            unsigned long long &dup_count,
                            unsigned long long &na_count);
void write_dup_lines_file(std::string &res_path,
                          std::string &file,
                          std::string &report_path,
                          std::ofstream &report_file,
                          std::unordered_map<std::string, int> &all_dup_lines);

// Writing functions
void omop_write_cross_tabs(std::unordered_map<std::string, std::unordered_map<std::string, unsigned long long>> col_tables,
                       std::vector<std::string> col_names,
                       std::string res_path,
                       std::string file_name);
void write_missing_res(unsigned long long **counts,
                       std::vector<std::string> col_names,
                       int n_cols,
                       std::string res_path,
                       std::string file_name);
void write_log(unsigned long long line_count, 
               unsigned long long total_line_count,
                       std::string res_path,
                       std::string file_name);

// Filling data structures functions
void update_missing_counts(std::vector<std::string> line, unsigned long long **counts);
void update_col_tabs(std::vector<std::string> line,
                       std::vector<std::string> &col_names,
                       std::unordered_map<std::string, std::unordered_map<std::string, unsigned long long>> &col_tables);
void omop_update_cross_tabs(std::vector<std::string> line,
                       std::vector<std::string> &col_names,
                       std::unordered_map<std::string, std::unordered_map<std::string, unsigned long long>> &col_tables);

// Reading files function
void get_previous_dup_lines(std::unordered_map<std::string, int> &all_dup_lines, 
                            std::string file,
                            std::string res_path);
void read_thl_sote_map(std::unordered_map<std::string, std::string> &thl_sote_map,
                   std::string thl_sote_path);
void read_thl_lab_id_abbrv_map(std::unordered_map<std::string, std::string> &thl_abbrv_map,
                      std::string thl_abbrv_path);
std::vector<std::string> read_correct_lines(std::string &line,
                                            unsigned long long &total_line_count,
                                            unsigned long long &skip_count,
                                            std::ofstream &error_file);
void read_omop_file(std::string omop_group_id_map_path,
                    std::unordered_map<std::string, std::string> &omop_group_id_map,
                    std::unordered_map<std::string, std::string> &omop_lab_id_map,
                    std::unordered_map<std::string, std::string> &omop_units,
                    std::unordered_map<std::string, std::string> &omop_names);