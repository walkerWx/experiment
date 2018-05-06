#include "points.h"


template<typename Out>
void split(const std::string &s, char delim, Out result) {
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, delim)) {
        *(result++) = item;
    }
}

std::vector<std::string> split(const std::string &s, char delim) {
    std::vector<std::string> elems;
    split(s, delim, std::back_inserter(elems));
    return elems;
}



int main(int argc, char *argv[]) {

    std::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);

    // 解析命令行参数
    int num = 256; // 生成输入个数，默认256个
    int dimension = 1; // 维度，每个输入对应几个浮点数，默认1维
    std::string file = "points.txt";   // 结果文件，默认当前文件夹下的points.txt
    double begin, end; // 随机取浮点数范围，命令行参数中以 --range=[begin, end] 给出，默认范围是所有浮点数
    bool range = false;
    for (int i = 1; i < argc; ++i) {
        std::string opt(argv[i]);
        std::vector<std::string> v = split(opt, '=');
        if (v[0] == "--num") {
            num = std::stoi(v[1]);           
        } else if (v[0] == "--dimension"){
            dimension = std::stoi(v[1]);          
        } else if (v[0] == "--file") {
            file = v[1]; 
        } else if (v[0]== "--range") {
            range = true; 
            v[1] = v[1].substr(v[1].find("[")+1, v[1].find("]"));
            begin = std::stod(split(v[1], ',')[0]);
            end = std::stod(split(v[1], ',')[1]);
        }
    }

    std::cout << "Preparing points..." << std::endl;
    std::cout << "Generate [" << num << "] random double values" << std::endl;
    std::cout << "The input dimension is [" << dimension << "]" << std::endl;
    if (range) {
        std::cout << "Value ranging from [" << begin << "] to [" << end << "]" << std::endl;
    } else {
        std::cout << "Value ranging from all range" << std::endl;
    }
    std::cout << "Writing to file [" << file << "]" <<  std::endl;
    
    std::ofstream ofs;
    ofs.open(file);
    for (int i = 0; i < num; ++i) {
        for (int j = 0; j < dimension; ++j) {
            if (range) {
                double d = generate_random_double(begin, end);
                std::cout << d << std::endl;
                ofs << double2binary(d) << " ";
            } else {
                double d = generate_random_double();
                std::cout << d << std::endl;
                ofs << double2binary(d) << " ";
            }
        }
        ofs << "\n";
    }   
    ofs.close();

    std::cout << "Done!" << std::endl;

}
