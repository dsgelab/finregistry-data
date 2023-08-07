#include <fstream>
#include <sstream>
#include <iostream>
#include <string>
#include <vector>
#include <regex>
#include <unordered_map>
#include <unordered_set>
#include <algorithm>

using namespace std;

// Helper functions
std::vector<std::string> split(const std::string &s, const char *delim);
std::string concat_string(std::vector<std::string> elems, std::string sep = std::string(""));
void check_out_open(std::ofstream &file_stream, std::string file_path);
void check_in_open(std::ifstream &file_stream, std::string file_path);
std::string to_lower(std::string str);
std::string remove_chars(std::string str, char remove_char);
std::string clean_units(std::string lab_unit);
std::string get_omop_identifier(std::string lab_id,
                                std::string lab_abbreviation,
                                std::string lab_unit = std::string(""));

// Helper functions for minimal file creation
void fix_nas(std::vector<std::string> &final_line_vec);
std::string get_service_provider_name(std::unordered_map<std::string, std::string> &thl_sote_map,
                               std::string &service_provider_oid);
void get_lab_id_and_source(std::string &local_lab_id,
                           std::string &thl_lab_id,
                           std::string &lab_id,
                           std::string &lab_id_source);
std::string get_lab_abbrv(std::unordered_map<std::string, std::string> &thl_abbrv_map,
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
                          std::unordered_map<std::string, int> &all_dup_lines);

// Writing functions
void write_top_lab_data(std::string file_path,
                        std::string res_path, 
                        std::unordered_set<std::string> keep_omop_ids);


// Reading files function
void get_new_omop_concepts(std::unordered_map<std::string, std::string> &new_omops,
                           std::unordered_map<std::string, std::string> &omop_names,   
                           std::string file_path);
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
                                            std::ofstream &error_file,
                                            int &lines_valid_status);
void read_omop_file(std::string omop_concept_map_path,
                    std::unordered_map<std::string, std::unordered_map<std::string, std::string>>  &omop_concept_map,
                    std::unordered_map<std::string, std::string> &omop_names);
void get_lab_indv_counts(std::unordered_map<std::string, std::unordered_set<std::string>> &lab_indv_count,
                         std::string file_path);

// Helper functions for OMOP mapping
std::string get_omop_lab_source(std::string lab_id_source,
                                std::string service_provider);
std::string get_omop_id(std::unordered_map<std::string, std::unordered_map<std::string, std::string>> &omop_concept_map,
                        std::string omop_lab_source,
                        std::string omop_identifier);
std::string get_omop_name(std::string omop_id,
                          std::unordered_map<std::string, std::string> &omop_names);

// Helper functions for top OMOP concepts file creation
void get_keep_omop_ids(std::unordered_set<std::string> &keep_omop_ids, 
                       std::unordered_map<std::string, std::unordered_set<std::string>> &lab_indv_count);

// Helpfer functions final fixing
int fix_percentages(std::string &lab_value, 
                    std::string &lab_unit,
                    std::string &lab_abnorm,
                    int keep);
void fix_abnorms(std::string &lab_abnorm);
void shuffle_lab_abnorm_info(std::string &lab_value, 
                             std::string &lab_abnorm, 
                             std::string &lab_unit);
int remove_illegal_values(std::string &lab_value, 
                          std::string &lab_abnorm, 
                          std::string &lab_abbrv,
                          int keep);
void remove_illegal_units(std::string &lab_unit);
void fix_phs(std::string &lab_id,
             std::string &lab_abbrv,
             std::string &lab_unit);
void fix_inrs(std::string &lab_id,
              std::string &lab_abbrv,
              std::string &lab_unit);
void remove_illegal_units(std::string &lab_unit);   
int remove_illegal_measure_year(std::string &date_time,
                                int keep);
void fix_titles(std::string &lab_id,
                  std::string &lab_abbrv,
                  std::string &lab_unit,
                  std::string &lab_value);

// OMOP final fixing
void get_omop_unit_counts(std::unordered_map<std::string, std::unordered_map<std::string, int>> &omop_unit_count,
                          std::string file_path);
void get_omop_max_units(std::unordered_map<std::string, std::string> &omop_max_units,
                        std::string file_path);
int decide_keep_rows(std::string omop_id,
                     std::string lab_unit,
                     std::unordered_map<std::string, std::string> &omop_max_units);