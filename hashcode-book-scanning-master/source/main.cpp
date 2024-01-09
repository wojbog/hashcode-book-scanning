/*
 * main.cpp
 *
 *  Created on: 1 March, 2020
 *  Author(s): Ahmed Morsy & Amr ELzawawy
 */

#include <iostream>
#include <unistd.h>
#include "hashcode_solver.h"

#define NUM_ARGS 3
#define INPUT_FILE_ARG_POS 1
#define OUTPUT_FILE_ARG_POS 2
using namespace std;

struct WrongArgumentsException : public exception {
   const char * what () const throw () {
      return "Wrong number of arguments passed. Requires Two correct file path arguments, one for input and one for output";
   }
};

inline bool file_exists (const std::string& name) {
    return ( access( name.c_str(), F_OK ) != -1 );
}

int main(int argc, char** argv) {
    char* input_file;
    char* output_file;
    // Double checks args and the file existence and throws my fancy expection otherwise.
    if(argc == NUM_ARGS){
        input_file = argv[INPUT_FILE_ARG_POS];
        output_file = argv[OUTPUT_FILE_ARG_POS];
        if(!(file_exists(input_file) || file_exists(output_file)))
            throw WrongArgumentsException();
    }
    else 
        throw WrongArgumentsException();
    
    read_input(input_file);
    solve_problem(output_file);
}