#!/usr/bin/python
# -*- coding:utf-8 -*-

import json


class PathData:

    """path文件封装类"""

    def __init__(self, path_file):

        with open(path_file) as f:
            data = json.load(f)

        self.program_name = data['program_name']
        self.function_name = data['function_name']

        self.variables = data['variables']
        self.input_variables = data['input_variables']

        self.return_expr = data['return']

        # initialize loops
        self.loops = dict()
        for loop_id in data['loops'].keys():
            self.loops[loop_id] = Loop(loop_id, data['loops'][loop_id])

        # initialize procedures
        self .procedures = dict()
        for procedure_id in data['procedures'].keys():
            self.procedures[procedure_id] = Procedure(procedure_id, data['procedures'][procedure_id])

        # initialize paths
        # must initialize loops and procedures first as when initialize paths we need loops and procedures information
        self.paths = list()
        for path in data['paths']:
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

    def get_paths(self):
        return self.paths

    def get_return_expr(self):
        return self.return_expr

    def get_loops(self):
        return self.loops

    def get_loop(self, loop_id):
        return self.loops[loop_id]

    def get_procedures(self):
        return self.procedures

    def get_procedure(self, procedure_id):
        return self.procedures[procedure_id]

    def clear_paths(self):
        self.paths = dict()

    def add_path(self, path_id, path):
        self.paths[path_id] = path

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

    def __init__(self, id, loop_json):

        self.id = id
        self.variables = loop_json['variables']
        self.initialize = loop_json['initialize']
        self.loop_body = loop_json['loop_body']

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


class Procedure:

    NOT_EXIST = "not exist"

    """Procedure封装类, 一个Procedure指代一段顺序执行的代码，我们用所涉及到的所有变量的更新式来记录这段代码所代表的语义"""

    def __init__(self, id, procedure_json):
        self.id = id
        self.procedure = procedure_json

    def get_id(self):
        return self.id

    def get_update_expr(self, var):
        if var not in self.procedure.keys():
            return self.NOT_EXIST
        else:
            return self.procedure[var]

    @staticmethod
    def get_type():
        return 'procedure'

    def to_json(self):
        return self.procedure


class Path:

    """单条路径的封装类，包含了约束、实现类型以及对应的路径信息"""

    def __init__(self, path_json, path_data):

        self.constrain = path_json['constrain']

        if 'implement' in path_json.keys():
            self.implement = path_json['implement']
        else:
            self.implement = 'NONE'

        self.path = []
        for p in path_json['path']:
            if p.startswith('procedure'):
                self.path.append(path_data.get_procedure(p[len('procedure:'):]))
            elif p.startswith('loop'):
                self.path.append(path_data.get_loop(p[len('loop:'):]))

    def set_implement(self, implement):
        self.implement = implement

    def add_constrain(self, constrain):
        self.constrain = '(' + self.constrain + ')' + '&&' + '(' + constrain + ')'

    def to_json(self):
        data = dict()
        data['constrain'] = self.constrain
        data['path'] = list()
        for p in self.path:
            data['path'].append(p.get_type() + ':' + p.get_id())
        return data


# Unit test
path_file = '../case/harmonic/harmonic.pth'
pd = PathData(path_file)

print(pd.to_json())

for path in pd.get_paths():
    print(path.to_json())

