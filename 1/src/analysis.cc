/*
    解析跑herbie实验用例产生的结果文件，将每个输入对应的irram输出，优化后程序输出，herbie输出打印到result.csv文件，控制台输打印该用例对应的最大herbie误差，相对误差以及对应输入，计算式等信息
    用法: analysis --irram=[irram结果文件] --opt=[优化后程序的结果文件] --herbie=[herbie结果文件，以逗号分隔]
    示例: ../../src/analysis --irram=irram_result.txt --opt=opt_result.txt --herbie=herbie_report5_17_expq3problem342_result.txt,herbie_report2_17_expq3problem342_result.txt,herbie_report4_17_expq3problem342_result.txt,herbie_report3_17_expq3problem342_result.txt,herbie_report0_17_expq3problem342_result.txt,herbie_report8_17_expq3problem342_result.txt,herbie_report7_17_expq3problem342_result.txt,herbie_report1_17_expq3problem342_result.txt,herbie_report6_17_expq3problem342_result.txt,herbie_report9_17_expq3problem342_result.txt 
*/
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
    string opt_result_file = "opt_result.txt";
    vector<string> herbie_result_file;
    string output_file = "result.csv";

    for (int i = 1; i < argc; ++i) {
        string opt(argv[i]);
        vector<string> v = split(opt, '=');
        if (v[0] == "--irram") {
            irram_result_file = v[1];
        } else if (v[0] == "--herbie") {
            herbie_result_file = split(v[1], ',');
        } else if (v[0] == "--opt") {
            opt_result_file = v[1];
        }
    }

    ifstream ifs(input_file);
    string line;
    getline(ifs, line);
    ifs.close();

    vector<vector<string>> input_points; 
    vector<string> irram_result;
    vector<string> opt_result;
    vector<vector<string>> herbie_result;

    string tmp;
    istringstream iss;

    // 读取输入
    ifs.open(input_file, ifstream::in);
    while (getline(ifs, line)) {
        input_points.push_back(vector<string>());
        vector<string> input_point_stable = split(line, ' ');
        if (input_point_stable.back() == "True" || input_point_stable.back() == "False") {
            input_point_stable = vector<string>(input_point_stable.begin(), input_point_stable.end()-1);
        }
        input_points[input_points.size()-1] = input_point_stable;
    }
    ifs.close();

    // 读取irram运行结果
    ifs.open(irram_result_file, ifstream::in);
    while (ifs >> tmp) {
        irram_result.push_back(tmp);
    }
    ifs.close();

    // 读取优化后程序运行结果
    ifs.open(opt_result_file, ifstream::in);
    while (ifs >> tmp) {
        opt_result.push_back(tmp);
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
    assert(input_points.size() == irram_result.size() && irram_result.size() == herbie_result.front().size() && input_points.size() == opt_result.size());
    for (auto r : herbie_result) {
        assert(r.size() == herbie_result.front().size());
    }

    int max_herbie_error_HI = -1; // herbie运行结果与iRRAM运行结果的最大herbie误差, HI代表Herbie vs iRRAM
    string mhe_irram_out_HI = "";
    string mhe_herbie_out_HI = "";
    vector<string> mhe_input_HI;
    string mhe_file_HI = "";


    double max_relative_error_HI = -1.0; // herbie运行结果与iRRAM运行结果的最大相对误差, HI代表Herbie vs iRRAM
    string mre_irram_out_HI = "";
    string mre_herbie_out_HI = "";
    vector<string> mre_input_HI;
    string mre_file_HI = "";

    int max_herbie_error_OI = -1; // 优化后程序运行结果与iRRAM运行结果的最大herbie误差, OI代表Herbie vs iRRAM
    string mhe_irram_out_OI = "";
    string mhe_opt_out_OI = "";
    vector<string> mhe_input_OI;

    double max_relative_error_OI = -1.0; // 优化后运行结果与iRRAM运行结果的最大相对误差, OI代表Herbie vs iRRAM
    string mre_irram_out_OI = "";
    string mre_opt_out_OI = "";
    vector<string> mre_input_OI;


    double re = 0.0;
    int he = 0;
    ofstream ofs(output_file);
    ofs << scientific << setprecision(numeric_limits<double>::digits10);
    // 每个输入
    for (unsigned i = 0; i < input_points.size(); ++i) {
        
        // 输出程序输入
        for (auto p: input_points[i]) {
            //ofs << binary2double(p) << "(" <<  p << "),";
            ofs << binary2double(p) << ",";
        }        
        // 输出irram结果
        //ofs << binary2double(irram_result[i]) << "(" << irram_result[i] << "),";
        ofs << binary2double(irram_result[i]) << ",";

        // 输出herbie结果
        for (unsigned j = 0; j < herbie_result.size(); ++j) {
            vector<string> hbr = herbie_result[j];

            // 输出hebie结果与irram结果的相对误差
            ofs << binary2double(hbr[i]) << ",";
            re = relative_error(irram_result[i], hbr[i]);
            if (re > max_relative_error_HI) {
                max_relative_error_HI = re; 
                mre_irram_out_HI = irram_result[i];
                mre_herbie_out_HI = hbr[i];
                mre_input_HI = input_points[i];
                mre_file_HI = herbie_result_file[j];
            }
            ofs << re << ",";

            // 输出herbie结果与irram结果的herbie误差
            he = herbie_error(irram_result[i], hbr[i]);
            if (he > max_herbie_error_HI) {
                max_herbie_error_HI = he;
                mhe_irram_out_HI = irram_result[i];
                mhe_herbie_out_HI = hbr[i];
                mhe_input_HI = input_points[i];
                mhe_file_HI = herbie_result_file[j];
            }
            ofs << he << ",";
        }

        // 输出优化后程序的结果
        ofs << binary2double(opt_result[i]) << ",";
        re = relative_error(irram_result[i], opt_result[i]);
        if (re > max_relative_error_OI) {
            max_relative_error_OI = re; 
            mre_irram_out_OI = irram_result[i];
            mre_opt_out_OI = opt_result[i];
            mre_input_OI = input_points[i];
        }
        ofs << re << ",";

        he = herbie_error(irram_result[i], opt_result[i]);
        if (he > max_herbie_error_OI) {
            max_herbie_error_OI = he; 
            mhe_irram_out_OI = irram_result[i];
            mhe_opt_out_OI = opt_result[i];
            mhe_input_OI = input_points[i];
        }
        ofs << he << ",";
        ofs << endl;
    }
    ofs.close();

    cout << scientific << setprecision(numeric_limits<double>::digits10);

    cout << "Max herbie error between [iRRAM] and [Herbie]: " << max_herbie_error_HI << endl;
    cout << "Input :" << endl;
    for (auto p : mhe_input_HI) {
        cout << p << " " << binary2double(p) << " " << endl;
    }
    cout << "iRRAM output:\n" << mhe_irram_out_HI << " " << binary2double(mhe_irram_out_HI) << endl;
    cout << "Herbie output:\n" << mhe_herbie_out_HI << " " << binary2double(mhe_herbie_out_HI) << endl;
    cout << "in file : " << mhe_file_HI << endl << endl; 

    cout << "Max herbie error between [iRRAM] and [Optimized]: " << max_herbie_error_OI << endl;
    cout << "Input :" << endl;
    for (auto p : mhe_input_OI) {
        cout << p << " " << binary2double(p) << " " << endl;
    }
    cout << "iRRAM output:\n" << mhe_irram_out_OI << " " << binary2double(mhe_irram_out_OI) << endl;
    cout << "Optimized output:\n" << mhe_opt_out_OI << " " << binary2double(mhe_opt_out_OI) << endl << endl;

    cout << "Max relative error between [iRRAM] and [Herbie]: " << max_relative_error_HI << endl;
    cout << "Input :" << endl;
    for (auto p : mre_input_HI) {
        cout << p << " " << binary2double(p) << " " << endl;
    }
    cout << "iRRAM output:\n" <<  mre_irram_out_HI << " " << binary2double(mre_irram_out_HI) << endl;
    cout << "Herbie output:\n" << mre_herbie_out_HI << " " << binary2double(mre_herbie_out_HI) << endl;
    cout << "in file : " << mre_file_HI << endl << endl;

    cout << "Max relative error between [iRRAM] and [Optimized]: " << max_relative_error_OI << endl;
    cout << "Input :" << endl;
    for (auto p : mre_input_OI) {
        cout << p << " " << binary2double(p) << " " << endl;
    }
    cout << "iRRAM output:\n" <<  mre_irram_out_OI << " " << binary2double(mre_irram_out_OI) << endl;
    cout << "Optimized output:\n" << mre_opt_out_OI << " " << binary2double(mre_opt_out_OI) << endl << endl;

}

