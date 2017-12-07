#!/usr/bin/python
# -*- coding:utf-8 -*-

import json


class PathData:

    """path文件封装类"""

    def __init__(self, path_file):

        with open(path_file) as f:
            data = json.load(f)

        self.data = data

        self.program_name = data['program_name']
        self.function_name = data['function_name']

        self.variables = data['variables']
        self.input_variables = data['input_variables']

        self.return_expr = data['return']

        # initialize procedures
        self.procedures = None
        self.init_procedures()

        # initialize loops
        self.loops = None
        self.init_loops()

        # initialize paths
        # must initialize loops and procedures first as when initialize paths we need loops and procedures information
        self.paths = None
        self.init_paths()

    def init_procedures(self):
        self .procedures = dict()
        for procedure_id in self.data['procedures'].keys():
            self.procedures[procedure_id] = self.get_procedure(procedure_id)

    def init_loops(self):
        self.loops = dict()
        for loop_id in self.data['loops'].keys():
            self.loops[loop_id] = self.get_loop(loop_id)

    def init_paths(self):
        self.paths = list()
        for path in self.data['paths']:
            self.paths.append(Path(path, self))

    def get_program_name(self):
        return self.program_name

    def get_function_name(self):
        return self.function_name

    def get_variables(self):
        return self.variables.keys()

    def get_variable_type(self, var):
        return self.variables[var]

    def get_input_variables(self):
        return self.input_variables

    # 返回path文件中所包含的所有变量，包括全局变量以及循环中涉及到的临时变量
    def get_all_variables(self):
        all_variables = list()
        all_variables.extend(self.get_variables())
        for _, loop in self.get_loops():
            all_variables.extend(loop.get_variables())
        return all_variables

    def get_paths(self):
        return self.paths

    def get_return_expr(self):
        return self.return_expr

    def get_loops(self):
        return self.loops

    def get_loop(self, loop_id):
        if loop_id in self.loops.keys():
            return self.loops[loop_id]
        elif loop_id in self.data['loops'].keys():
            self.loops[loop_id] = Loop(loop_id, self)
            return self.loops[loop_id]
        else:
            return None

    def get_procedures(self):
        return self.procedures

    def get_procedure(self, procedure_id):
        if procedure_id in self.procedures.keys():
            return self.procedures[procedure_id]
        elif procedure_id in self.data['procedures'].keys():
            self.procedures[procedure_id] = Procedure(procedure_id, self)
            return self.procedures[procedure_id]
        else:
            return None

    def add_procedure(self, procedure):
        self.procedures[procedure.get_id()] = procedure

    def clear_paths(self):
        self.paths = list()

    def add_path(self, path):
        self.paths.append(path)

    def to_json(self):

        data = dict()
        data['program_name'] = self.get_program_name()
        data['function_name'] = self.get_function_name()
        data['variables'] = self.variables
        data['input_variables'] = self.input_variables

        data['loops'] = dict()
        for loop_id, loop in self.get_loops().items():
            data['loops'][loop_id] = loop.to_json()

        data['procedures'] = dict()
        for procedure_id, procedure in self.get_procedures().items():
            data['procedures'][procedure_id] = procedure.to_json()

        data['paths'] = [path.to_json() for path in self.paths]

        return data

    def output_json(self, path_file):
        data = self.to_json()
        with open(path_file, 'w') as f:
            json.dump(data, f, indent=4)


class Loop:

    """Loop封装类, 一个Loop指代一段循环的代码，包括了所涉及到的临时变量和它们的初始化，循环体等内容"""

    def __init__(self, id, path_data):

        loop_json = path_data.data['loops'][id]

        self.id = id
        self.variables = loop_json['variables']
        self.initialize = loop_json['initialize']

        # in fact, loop body is a list of path
        self.loop_body = list()
        for lb in loop_json['loop_body']:
            self.loop_body.append(Path(lb, path_data))

    def get_id(self):
        return self.id

    def get_variables(self):
        return self.variables.keys()

    def get_variable_type(self, var):
        return self.variables[var]

    def get_initialize_expr(self, var):
        return self.initialize[var]

    def get_initialize_list(self):
        return self.initialize

    def get_loop_body(self):
        return self.loop_body

    @staticmethod
    def get_type():
        return 'loop'

    def to_json(self):
        data = dict()
        data['variables'] = self.variables
        data['initialize'] = self.initialize
        data['loop_body'] = self.get_loop_body()
        return data

    def to_cpp_code(self, indent=0):
        code = indent*'\t'+'{\n'
        # temporary variables initialize
        for var, update_expr in self.get_initialize_list().items():
            code += (indent+1)*'\t' + var + ' = ' + update_expr + ';\n'

        code += (indent+1)*'\t'+'while(true) {\n'

        # loop body
        for lb in self.get_loop_body():
            code += lb.to_cpp_code(indent+2)

        code += (indent+1)*'\t'+'}\n'
        code += indent*'\t'+'}\n'
        return code


class Procedure:

    """Procedure封装类, 一个Procedure指代一段顺序执行的代码，我们用所涉及到的所有变量的更新式来记录这段代码所代表的语义"""

    def __init__(self, id, path_data):
        self.id = id
        self.procedure = path_data.data['procedures'][id]

    def get_id(self):
        return self.id

    def set_id(self, new_id):
        self.id = new_id

    def get_update_expr(self, var):
        if var not in self.procedure.keys():
            return None
        else:
            return self.procedure[var]

    def set_update_expr(self, var, update_expr):
        self.procedure[var] = update_expr

    def get_procedure(self):
        return self.procedure

    @staticmethod
    def get_type():
        return 'procedure'

    def to_json(self):
        return self.procedure

    def to_cpp_code(self, indent=0):
        code = ''
        for var, update_expr in self.procedure.items():
            code += indent*'\t'+var + ' = ' + update_expr + ';\n'
        return code


class Path:

    """单条路径的封装类，包含了约束、实现类型以及对应的路径信息"""

    def __init__(self, path_json, path_data):

        self.constrain = path_json['constrain']

        if 'implement' in path_json.keys():
            self.implement = path_json['implement']
        else:
            self.implement = None

        if 'break' in path_json.keys() and path_json['break'] == 'true':
            self.loop_break = True
        else:
            self.loop_break = None

        # path_list为一个Procedure与Loop的列表，代表了一条路径
        self.path_list = []
        for p in path_json['path']:
            if p.startswith('procedure'):
                self.path_list.append(path_data.get_procedure(p[len('procedure:'):]))
            elif p.startswith('loop'):
                self.path_list.append(path_data.get_loop(p[len('loop:'):]))

    def set_implement(self, implement):
        self.implement = implement

    def add_constrain(self, constrain):
        self.constrain = '(' + self.constrain + ')' + '&&' + '(' + constrain + ')'

    def get_path_list(self):
        return self.path_list

    def set_path_list(self, path_list):
        self.path_list = path_list

    def to_json(self):
        data = dict()
        data['constrain'] = self.constrain
        data['path'] = list()
        for p in self.get_path_list():
            data['path'].append(p.get_type() + ':' + p.get_id())

        if self.implement:
            data['implement'] = self.implement

        return data

    def to_cpp_code(self, indent=0):
        code = ''
        code += indent*'\t' + 'if(' + self.constrain + ') {\n'
        for m in self.path_list:
            code += m.to_cpp_code(indent+1)
        if self.loop_break:
            code += (indent+1)*'\t'+'break;\n'
        code += indent*'\t'+'}\n'
        return code


# Unit test
'''
path_file = '../case/harmonic/harmonic.pth'
pd = PathData(path_file)

for path in pd.get_paths():
    print(path.to_cpp_code())
'''
