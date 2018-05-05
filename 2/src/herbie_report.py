import os


# 找到所有的compiled.c文件，也就是包含了Herbie优化后程序代码的文件，将其中优化后程序组成一个C文件
def generate_herbie_cc():

    compiled_files = list()
    report_dir = '/Users/walker/Desktop/HerbieCases'
    for root, dirs, files in os.walk(report_dir):
        for file in files:
            if file == "compiled.c":
                compiled_files.append(os.path.join(root, file))

    compiled_files.sort()

    herbie_file = open("herbie.cc", "w")

    for compiled_file in compiled_files:

        [report_num, case_name] = compiled_file.split('/')[-3:-1]
        funcname = '_'.join(["herbie", report_num, case_name.replace('-', '_')])
        with open(compiled_file) as file:
            lines = file.readlines()
            start = next(i for i in range(len(lines)) if lines[i].startswith("double f_of"))
            end = next(i for i in range(len(lines)) if lines[i].startswith("}") and i > start) + 1
            lines[start] = lines[start].replace('f_of', funcname)
            for i in range(start, end):
                herbie_file.write(lines[i])
        herbie_file.write('\n')

    herbie_file.close()


def prepare(casename):

    casedir = "../case/" + casename
    os.makedirs(casedir, exist_ok=True)

    # 准备irram可执行文件
    irram_file = os.path.join(casedir, 'irram.cc')
    print(irram_file)


    # 准备herbie可执行文件
    herbie_file = os.path.join(casedir, 'herbie.cc')

    # 准备随机浮点数
    points_file = os.path.join(casedir, 'points.txt')


if __name__ == "__main__":
    prepare("sintan")
