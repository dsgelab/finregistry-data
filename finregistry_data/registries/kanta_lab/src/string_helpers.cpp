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


std::string concat_string(std::vector<std::string> elems, 
                          std::string sep) {
    std::stringstream ss;
    for(auto elem: elems) {
        ss << elem << sep;
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

