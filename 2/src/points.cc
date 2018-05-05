#include <bitset>
#include <cstdint>
#include <fstream>
#include <random>
#include <iostream>
#include <iomanip>
#include <iterator>
#include <sstream>
#include <string>
#include <vector>

// 生成随机双精度浮点数
double generate_random_double() {

    std::random_device rd;
    std::default_random_engine generator(rd());    
    std::bernoulli_distribution distribution(0.5);

    uint64_t n = 0;
    for (uint64_t i = 0; i < 64; i++) {
        bool b = distribution(generator);
        if (!b) {
            n = n & ~((uint64_t)1 << i);
        }
        else {
            n = n | ((uint64_t)1 << i);
        }
    }

    double d = *(double *)(&n);

    if (d == d) {
        return d;
    }
    return generate_random_double(); 
}

// 统计[begin, end)之间双精度浮点数个数
uint64_t double_num_between(double begin, double end) {

    if (end <= begin) return 0;

    //uint64_t u_begin = *(uint64_t *)(&begin); 
    uint64_t u_end = *(uint64_t *)(&end);

    //uint64_t sign_mask = uint64_t(1) << 63;
    uint64_t frac_mask = 0;
    for (int i = 0; i < 52; ++i) {
        frac_mask |= uint64_t(1) << i; 
    }
    uint64_t exp_mask = 0;
    for (int i = 52; i < 63; ++i) {
        exp_mask |= uint64_t(1) << i;
    }

    //std::cout << "sign mask:" << std::bitset<64>(sign_mask) << std::endl;
    //std::cout << "exp  mask:" << std::bitset<64>(exp_mask) << std::endl;
    //std::cout << "frac mask:" << std::bitset<64>(frac_mask) << std::endl;

    //std::cout << std::bitset<64>(u_begin) << std::endl;
    //std::cout << std::bitset<64>(u_end) << std::endl;

    if (begin  == 0.0) {
        return (u_end&exp_mask)+(u_end&frac_mask); 
    }
    if (begin < 0 && 0 < end) {
        return double_num_between(0.0, -begin)+double_num_between(0.0, end); 
    }
    if (0 < begin) {
        return double_num_between(0.0, end)-double_num_between(0.0, begin);
    }
    if (end <= 0) {
        return double_num_between(0.0, -begin)-double_num_between(0.0, -end); 
    }
    return 0;
}

// 生成双精度浮点数d后面第offset个浮点数
double generate_double_by_offset(double d, uint64_t offset) {
    
    if (d == 0.0) {
        return *(double *)(&offset);
    }
    
   if (d > 0) {
        return generate_double_by_offset(0.0, offset+double_num_between(0.0, d));
   }

   if (d < 0) {
        if (offset >= double_num_between(d, 0.0)) {
            return generate_double_by_offset(0.0, offset-double_num_between(d, 0.0));
        } else {
            return -generate_double_by_offset(0.0,double_num_between(0.0, -d)-offset);
        }
   }
    return 0;
}

// 生成[begin, end)之间随机的双精度浮点数
double generate_random_double(double begin, double end) {

    if (begin >= end) {
        std::cerr << "Can't sample a double between [" <<  begin << ", " << end <<  "]" << std::endl; 
        return 0;
    }

    uint64_t distance = double_num_between(begin, end);
    std::random_device rd;   
    std::mt19937_64 generator(rd());
    std::uniform_int_distribution<uint64_t> distribution(0, distance);

    uint64_t offset = distribution(generator);
    return generate_double_by_offset(begin, offset);      
}

// 将一个长度为64的01字符串转为double
double binary2double(std::string str) {
    std::bitset<64> bitset64(str);
    return bitset64.to_ulong();
}

// 将一个double转换为64位长的01字符串
std::string double2binary(double d) {
    uint64_t u = *(uint64_t *)(&d);
    std::bitset<64> bitset64(u);
    return bitset64.to_string();
}

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
                ofs << double2binary(generate_random_double(begin, end)) << " ";
            } else {
                ofs << double2binary(generate_random_double()) << " ";
            }
        }
        ofs << "\n";
    }   
    ofs.close();

    std::cout << "Done!" << std::endl;

        /*
    while (true) {
        double begin, end;
        std::cin >>  begin >> end;
        uint64_t offset = double_num_between(begin, end);
        std::cout << std::bitset<64>(offset) << std::endl; 
        std::cout << generate_double_by_offset(begin, offset) << std::endl;
        std::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);

        std::cout << double_num_between(0.0,1.0) << std::endl;
        std::cout << generate_random_double(-1.0,1E100) << std::endl;
        getchar(); 
    }
        */
}
