#include "header.h"

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

void check_in_open(std::ifstream &file_stream, 
                   std::string file_path) {
    if(!file_stream.is_open())  {
        std::vector<std::string> error_msg_vec = {"Error when opening ", file_path};
        std::string error_msg = concat_string(error_msg_vec);
        const char* error_msg_char = error_msg.c_str();
        perror(error_msg_char);
        exit(EXIT_FAILURE);
    }
}