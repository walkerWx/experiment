#ifndef POINTS_H
#define POINTS_H

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
double generate_random_double(); 

// 生成[begin, end)之间随机的双精度浮点数
double generate_random_double(double begin, double end);

// 统计[begin, end)之间双精度浮点数个数
uint64_t double_num_between(double begin, double end); 

// 生成双精度浮点数d后面第offset个浮点数
double generate_double_by_offset(double d, uint64_t offset);

// 将一个长度为64的01字符串转为double
double binary2double(std::string str);

// 将一个double转换为64位长的01字符串
std::string double2binary(double d);

#endif
