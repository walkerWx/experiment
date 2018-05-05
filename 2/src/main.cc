#include <bitset>
#include <cstdint>
#include <random>
#include <iostream>
#include <iomanip>

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

int main() {
    std::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);

    while (true) {
        /*
        double begin, end;
        std::cin >>  begin >> end;
        uint64_t offset = double_num_between(begin, end);
        std::cout << std::bitset<64>(offset) << std::endl; 
        std::cout << generate_double_by_offset(begin, offset) << std::endl;
        */
        std::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);

        std::cout << double_num_between(0.0,1.0) << std::endl;
        std::cout << generate_random_double(-1.0,1E100) << std::endl;
        getchar(); 
    }
}
