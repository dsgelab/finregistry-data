#include "header.h"
template <typename Out>

/*/
    Splits a string based on a given delimiter. Copied from https://stackoverflow.com/questions/236129/how-do-i-iterate-over-the-words-of-a-string
*/
void split(const std::string &s, 
           const char *delim, 
           Out result) {
    std::istringstream iss(s);
    std::string item;
    while (std::getline(iss, item, *delim)) {
        *result++ = item;
    }
}

/*/
    Splits a string based on a given delimiter. Copied from https://stackoverflow.com/questions/236129/how-do-i-iterate-over-the-words-of-a-string
*/
std::vector<std::string> split(const std::string &s, 
                                const char *delim) {
    std::vector<std::string> elems;
    split(s, delim, std::back_inserter(elems));
    return elems;
}


std::string concat_string(const std::vector<std::string> &elems, std::string sep) {    
    std::stringstream ss;
    long unsigned int count = 0;
    for(auto elem: elems) {
        ss << elem;
        if(count < elems.size()-1)
            ss << sep;
        count++;
    }
    std::string final = ss.str();
    return(final);
} 

std::string concat_string(const std::unordered_set<string> &elems, std::string sep) {    
    std::stringstream ss;
    long unsigned int count = 0;
    for(auto elem: elems) {
        ss << elem;
        if(count < elems.size()-1)
            ss << sep;
        count++;
    }
    std::string final = ss.str();
    return(final);
} 

//     std::string concat = std::accumulate(std::make_move_iterator(v.begin()),
//                                          std::make_move_iterator(v.end()),
//                                          std::string());
//  https://en.cppreference.com/w/cpp/iterator/move_iterator

// Transform a string to lower case
std::string to_lower(std::string str) {
    std::transform(str.begin(), str.end(), str.begin(), ::tolower);
    return(str);
}

std::string remove_chars(std::string str,
                         char remove_char) {
    str.erase(std::remove_if(str.begin(), str.end(), [remove_char](char c) {
        return c == remove_char;}), str.end());
    return(str);
}

std::string get_lab_id_omop_identifier(std::string lab_id,
                                       std::string lab_abbrv,
                                       std::string lab_unit,
                                       char sep) {

    // Currently identifying the OMOP concept by the lab ID and abbreviation.
    add_quotation(lab_id, sep);
    add_quotation(lab_abbrv, sep);
    add_quotation(lab_unit, sep);
    std::vector<std::string> omop_identifier_vec = {lab_id, lab_abbrv, lab_unit};
    std::string omop_identifier = concat_string(omop_identifier_vec, &sep);

    return(omop_identifier);
} 

std::string get_omop_identifier(std::string omop_id,
                                std::string omop_name,
                                std::string lab_unit,
                                char sep) {

    // Currently identifying the OMOP concept by the lab ID and abbreviation.
    add_quotation(omop_id, sep);
    add_quotation(omop_name, sep);
    add_quotation(lab_unit, sep);
    std::vector<std::string> omop_identifier_vec = {omop_id, omop_name, lab_unit};
    std::string omop_identifier = concat_string(omop_identifier_vec, &sep);

    return(omop_identifier);
} 

/** 
 * @brief Splits a string based on a given delimiter ignoring any delimiter inside "".
 * 
 * @param input string to split
 * @param delimiter delimiter to split on
 * 
 * @return vector of strings
 * 
 * @details
 * Splits a string based on a given delimiter. Produced by chatGPT. 
 * Splits string and ignored delimiter inside "". 
 */
std::vector<std::string> splitString(const std::string &input, 
                                     char delim) {
  std::vector<std::string> tokens;
  std::istringstream ss(input);
  std::string token;
  bool inQuotedString = false;
  
  for (char c : input) {
    if (c == '"') {
      inQuotedString = !inQuotedString; // Toggle quoted string state
    } else if ((c == delim && !inQuotedString)) {
      tokens.push_back(token);
      token.clear();
    } else {
      token += c;
    }
  }
  tokens.push_back(token); // Add the last token
  
  return tokens;
}

/**
 * @brief Cleans units by removing characters like " ", "_", etc
 * 
 * @param lab_unit Unit to clean
 * 
 * @return Cleaned unit
 * 
 * @details
 * Removes all character in the string " ", "_", ",", ".", "-", ")", "(", "{", "}", "'", "?", "!".
*/
std::string clean_units(std::string lab_unit) {
    lab_unit = remove_chars(lab_unit, ' ');
    lab_unit = remove_chars(lab_unit, '_');
    lab_unit = remove_chars(lab_unit, ',');
    lab_unit = remove_chars(lab_unit, '.');
    lab_unit = remove_chars(lab_unit, '-');
    lab_unit = remove_chars(lab_unit, ')');
    lab_unit = remove_chars(lab_unit, '(');
    lab_unit = remove_chars(lab_unit, '{');
    lab_unit = remove_chars(lab_unit, '}');
    lab_unit = remove_chars(lab_unit, '\'');
    lab_unit = remove_chars(lab_unit, '?');
    lab_unit = remove_chars(lab_unit, '!');

    return(lab_unit);
}

/**
 * @brief Creates a single string combining the OMOP ID and OMOP Name that can be 
 * used to identify the concept and written directly to results files
*/
std::string get_omop_info(std::string omop_id, std::string omop_name, char delim) {
    add_quotation(omop_id, delim);
    std::string omop_info = concat_string(std::vector<std::string>({omop_id, omop_name}), std::string(1, delim));
    return(omop_info);
}

/**
 * @brief Creates a single string combining the lab abbreviation and its unit that can be 
 * used to identify the concept and written directly to results files
*/
std::string get_lab_info(std::string lab_abbrv, std::string lab_unit, char delim) {
    add_quotation(lab_abbrv, delim);
    std::string lab_info = concat_string(std::vector<std::string>({lab_abbrv, lab_unit}), std::string(1, delim));
    return(lab_info);
}

/**
 * @brief Creates a single string combining the Lab ID, the lab info (see get_lab_info function),
 *  and the omop_info (see get_omop_info function) that can be 
 * used to identify the concept and written directly to results files
*/
std::string get_lab_id_omop_info(std::string lab_id, 
                                 std::string lab_info,
                                 std::string omop_info,
                                 char delim) {
    add_quotation(lab_id, delim);
    std::string lab_id_omop_info = concat_string(std::vector<std::string>({lab_id, lab_info, omop_info}), std::string(1, delim));
    return(lab_id_omop_info);                             
}

std::string get_lab_id_abbrv(std::string lab_id, 
                             std::string lab_abbrv) {
    std::string lab_id_abbrv = concat_string(std::vector<std::string>({lab_id, lab_abbrv}), std::string("_"));
    return(lab_id_abbrv); 
}

void add_quotation(std::string &str,
                   char delim) {
    if(str.find(delim) != std::string::npos) {
        str = concat_string(std::vector<std::string>({"\"", str,  "\""}));
    }
}