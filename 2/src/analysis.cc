#include "points.h"

#include <cassert>
#include <iomanip>
#include <iostream>
#include <fstream>
#include <limits>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

int main(int argc, char *argv[]) {

    string input_file = "points.txt";
    string irram_result_file = "irram_result.txt";
    vector<string> herbie_result_file;
    string output_file = "result.csv";

    for (int i = 1; i < argc; ++i) {
        string opt(argv[i]);
        vector<string> v = split(opt, '=');
        if (v[0] == "--irram") {
            irram_result_file = v[1] ;
        } else if (v[0] == "--herbie") {
            herbie_result_file = split(v[1], ',');
        } 
    }

    ifstream ifs(input_file);
    string line;
    getline(ifs, line);
    ifs.close();
    int input_dimension = split(line, ' ').size();

    vector<vector<string>> input_points; 
    vector<string> irram_result;
    vector<vector<string>> herbie_result;

    string tmp;
    istringstream iss;

    // 读取输入
    ifs.open(input_file, ifstream::in);
    while (getline(ifs, line)) {
        input_points.push_back(vector<string>());
        iss.str(line);
        for (int i = 0; i < input_dimension; ++i) {
            iss >> tmp; 
            input_points.back().push_back(tmp);
        } 
    }
    ifs.close();

    // 读取irram运行结果
    ifs.open(irram_result_file, ifstream::in);
    while (ifs >> tmp) {
        irram_result.push_back(tmp);
    }
    ifs.close();
    
    // 读取herbie运行结果
    for (string hrf : herbie_result_file) {
        ifs.open(hrf, ifstream::in);
        herbie_result.push_back(vector<string>());
        while (ifs >> tmp) {
            herbie_result.back().push_back(tmp);
        }
        ifs.close();
    }

    // 保证输入输出数目一致
    cout << input_points.size() << " " << irram_result.size() << " " << herbie_result.front().size() << endl;
    assert(input_points.size() == irram_result.size() && irram_result.size() == herbie_result.front().size());
    for (auto r : herbie_result) {
        assert(r.size() == herbie_result.front().size());
    }

    ofstream ofs(output_file);
    ofs << scientific << setprecision(numeric_limits<double>::digits10);
    for (unsigned i = 0; i < input_points.size(); ++i) {
        for (auto p: input_points[i]) {
            //ofs << binary2double(p) << "(" <<  p << "),";
            ofs << binary2double(p) << ",";
        }        
        //ofs << binary2double(irram_result[i]) << "(" << irram_result[i] << "),";
        ofs << binary2double(irram_result[i]) << ",";
        for (auto hbr: herbie_result) {
            //ofs << binary2double(hbr[i])  << "(" << hbr[i] << "),";
            ofs << binary2double(hbr[i]) << ",";
            ofs << relative_error(irram_result[i], hbr[i]) << ",";
            ofs << herbie_error(irram_result[i], hbr[i]) << ",";
        }
        ofs << endl;
    }
    ofs.close();
    
}

