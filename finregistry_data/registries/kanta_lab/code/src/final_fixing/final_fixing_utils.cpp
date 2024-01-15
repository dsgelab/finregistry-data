#include "../header.h"


void read_lab_id_abbrv_map(std::string file_path,
                           std::map<std::string, std::unordered_set<std::string>> &elems) {
   // open
    std::ifstream in_file;
    in_file.open(file_path);
    check_in_open(in_file, file_path, 1);
    // Read
    std::string line;
    std::map<std::string, std::unordered_set<std::string>> phs;
    char delim = find_delim(file_path);
    while (std::getline(in_file, line)) {
        std::vector<std::string> line_vec = split(line, &delim);
        elems[line_vec[0]].insert(line_vec[1]);
    }
    in_file.close();

    // Print first 10 elems of elems
    std::cout << "Printing first 10 elems of " << file_path << std::endl;
    for(auto &elem: elems) {
        std::cout << elem.first << " <--> ";
        for(auto &elem2: elem.second)
            std::cout << elem2 << " ";
        std::cout << std::endl;
    }
}

/**
 * @brief Fixes phs that often have no units
 * 
 * @param lab_id The lab id of the lab test
 * @param lab_abbrv The lab abbreviation of the lab test
 * @param lab_unit The lab unit of the lab test
 * 
 * @return void
 * 
 * Makes the units "ph" to preserve the information that this is a ph measurement.
*/
void fix_phs(std::string &lab_id,
             std::string &lab_abbrv,
             std::string &lab_unit,
             std::map<std::string, std::unordered_set<std::string>> &phs) {
    if(phs.find(lab_id) != phs.end()) {
        if(phs[lab_id].find(lab_abbrv) != phs[lab_id].end()) {
            if(lab_unit == "NA") lab_unit = "ph";
        }
    } 
}


/**
 * @brief Fixes titles that have random units and values even though they are not measurements
 * 
 * @param lab_id The lab id of the lab test
 * @param lab_abbrv The lab abbreviation of the lab test
 * @param lab_unit The lab unit of the lab test
 * @param lab_value The lab value of the lab test
 * 
 * @return void
 * 
 * Makes the units "ordered" to preserve the information that this title has been ordered for the patient.
*/
void fix_titles(std::string &lab_id,
                  std::string &lab_abbrv,
                  std::string &lab_unit,
                  std::string &lab_value,
                  std::map<std::string, std::unordered_set<std::string>> &titles) {

    if(titles.find(lab_id) != titles.end()) {
        if(titles[lab_id].find(lab_abbrv) != titles[lab_id].end()) {
            // this is actually a bug, want to remove the data and not 
            // make it pH but represents the current data
            lab_unit = "ordered";
        }
    }
}

/**
 * @brief Converts units from e6/l to e9/l
 * 
 * @param lab_value The lab value of the lab test
 * @param lab_unit The lab unit of the lab test
 * 
 * @return void
 * 
 * Converts units from e6/l to e9/l.
*/
void unit_conversion(std::string lab_value,
                     std::string lab_unit) {
    // Convert e6/l to e9/l
    if(lab_unit == "e6/l") {
        double lab_value_double = std::stod(lab_value);
        lab_value_double = lab_value_double / 1000;
        lab_value = std::to_string(lab_value_double);
        lab_unit = "e9/l";
    }
}

/**
 * @brief Fixes inrs that often have no units
 * 
 * @param lab_id The lab id of the lab test
 * @param lab_abbrv The lab abbreviation of the lab test
 * @param lab_unit The lab unit of the lab test
 * 
 * @return void
 * 
 * Makes the units "inr" to preserve the information that this is an inr measurement.
*/
void fix_inrs(std::string &lab_id,
              std::string &lab_abbrv,
              std::string &lab_unit) {
    std::unordered_set<std::string> inrs = {"4520 p-tt-inr", "4520 p-inr", "955 p-inr."};

    if((inrs.find(concat_string(std::vector<std::string>({lab_id, lab_abbrv}), " ")) != inrs.end()) & (lab_unit == "NA")) lab_unit = "inr";
}

/**
 * @brief Removes illegal units that are actually numbers
 * 
 * @param lab_unit The lab unit of the lab test
 * 
 * @return void
*/
void remove_illegal_units(std::string &lab_unit) {
    try {
        double lab_unit_double = std::stod(lab_unit);
        lab_unit = "NA";
    } catch(...) {
        return;
    }
}

/**
 * @brief Removes illegal measure years that are before 2014
 * 
 * @param date_time The date and time of the lab test
 * @param keep Whether the line should be kept or not
 * 
 * @return void
 * 
 * If the year of the lab test is before 2014, the line is removed.
*/
int remove_illegal_measure_year(std::string &date_time,
                                int keep) {
    std::string year = date_time.substr(0, 4);
    try {
        int year_int = std::stoi(year);
        if(year_int < 2014 || year_int > 2023) {
            keep = 0;
        } 
    } catch(...) {
        keep = 0;
    }
    return(keep);
}

/**
 * @brief Removes illegal values that are not numbers
 * 
 * @param lab_value The lab value of the lab test
 * @param lab_abnorm The lab abnormality of the lab test
 * @param lab_abbrv The lab abbreviation of the lab test
 * @param keep Whether the line should be kept or not
 * 
 * @return void
 * 
 * If the lab value is not a number, the line is removed. Additionally, negative values
 * are removed except for -h-ind, ab-hb-met, be and vekaas.
*/
int remove_illegal_values(std::string &lab_value, 
                          std::string &lab_abnorm, 
                          std::string &lab_abbrv,
                          int keep) {
    try {
        double lab_value_double = std::stod(lab_value);
        // Special cases of lab values that can be negative
        if((lab_abbrv == "-h-ind")) return(keep);
        if((lab_abbrv == "ab-hb-met")) return(keep);
        if(lab_abbrv.length() > 3) {
            if((lab_abbrv.substr(3, 2) == "be")) return(keep);
        } 
        if(lab_abbrv.length() >= 9) {
            if((lab_abbrv.substr(3, 6) == "vekaas")) return(keep);
        }
        // All other values should be positive
        if(lab_value_double < 0) {
            lab_value = "NA";
            // This means we end up having neither lab value nor abnormality
            if(lab_abnorm == "NA") keep = 0;  
        }
    // This means the lab value is not a number
    } catch(const std::invalid_argument& e) {
        lab_value = "NA";
        // This means we end up having neither lab value nor abnormality
        if(lab_abnorm == "NA") keep = 0;
    }
    return(keep);
}

/**
 * @brief Removes illegal measure statuses that are D or P
 * 
 * @param measure_status The measure status of the lab test
 * @param keep Whether the line should be kept or not
 * 
 * @return void
 * 
 * If the measure status is D or P, the line is removed. D stands for deleted information and P for a preliminary result. The entrie with missing information
 * are kept. We have found that this increases the coverage across different 
 * areas of Finland. Indicating that the actual status is missing from specific
 * providers.
 */
int remove_bad_measure_status(std::string measure_status,
                              int keep) {
    if(measure_status == "NA") return(keep);
    if(measure_status == "D") return(0);
    if(measure_status == "P") return(0);
    return(keep);
}

/**
 * @brief Fixes percentages that are in osuus (fraction) format
 * 
 * @param lab_value The lab value of the lab test
 * @param lab_unit The lab unit of the lab test
 * @param lab_abnorm The lab abnormality of the lab test
 * @param keep Whether the line should be kept or not
 * 
 * @return int
 * 
 * If the lab unit is osuus (fraction), the lab value is multiplied by 100 and the lab unit
 * turned to %. If the lab unit is already %, the lab value is kept as is.
*/
int fix_percentages(std::string &lab_value, 
                    std::string &lab_unit,
                    std::string &lab_abnorm,
                    int keep) {
    // Make osuus (fraction) and % the same
    if(lab_unit == "osuus") {
        lab_unit = "%";
        try {
            lab_value = std::to_string(std::stod(lab_value) * 100);
        } catch(const std::invalid_argument& e) {
            lab_value = "NA";
            // This means we end up having neither lab value nor abnormality
            if(lab_abnorm == "NA") keep = 0;
        }
    }

    return(keep);
}

/**
 * @brief Fixes abnormality abbreviations to be consistent
 * 
 * @param lab_abnorm The lab abnormality of the lab test
 * 
 * @return void
 * 
 * Fixes abnormality abbreviations to be consistent with the OMOP standard. This means replacing
 * < with L, > with H, POS with A and NEG with N. If the abbreviation is not one of these, it is
 * replaced with NA.
*/
void fix_abnorms(std::string &lab_abnorm) {
    if(lab_abnorm == "<") {
        lab_abnorm = "L";
    } else if(lab_abnorm == ">") {
        lab_abnorm = "H";
    } else if(lab_abnorm == "POS") {
        lab_abnorm = "A";
    } else if(lab_abnorm == "NEG") {
        lab_abnorm = "N";
    }
    
    if((lab_abnorm != "A") & (lab_abnorm != "AA") & (lab_abnorm != "H") & (lab_abnorm != "HH") & (lab_abnorm != "L") & (lab_abnorm != "LL") & (lab_abnorm != "N")) {
        lab_abnorm = "NA";
    }
}

/**
 * @brief Shuffles lab abnormality information to the correct columns
 * 
 * @param lab_value The value of the lab test
 * @param lab_abnorm The abnormality of the lab test
 * @param lab_unit The unit of the lab test
 * 
 * @return void
 * 
 * Moves lab unit information on abnormality to lab abnormality column and 
 * lab abnormality information to lab value column for binary tests where
 * abnormality is the only information.
*/
void shuffle_lab_abnorm_info(std::string &lab_value, 
                             std::string &lab_abnorm, 
                             std::string &lab_unit) {
    // Moving lab unit information on abnormality to lab abnormality column
    if((lab_unit == "A")) {
        lab_abnorm = "A";
        lab_unit = "NA";
    } else if(lab_unit == "N") {
        lab_abnorm = "N";
        lab_unit = "NA";
    } 

    // Moving lab abnormality information to lab value column for binary tests
    // where abnormality is the only information
    if(lab_value == "NA") {
        if((lab_abnorm == "A") | (lab_abnorm == "AA") | (lab_abnorm == "L") | (lab_abnorm == "LL") | (lab_abnorm == "H") | (lab_abnorm == "HH")) {
            lab_value = "1";
            lab_unit = "binary";
        } else if(lab_abnorm == "N") {
            lab_value = "0";
            lab_unit = "binary";
        } 
    }
}