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
            self.loops[loop_id] = Loop(data['loops'][loop_id])

        # initialize procedures
        self .procedures = dict()
        for procedure_id in data['procedures'].keys():
            self.procedures[procedure_id] = Procedure(data['procedure'][procedure_id])

        # initialize paths
        # must initialize loops and procedures first as when initialize paths we need loops and procedures information
        self.paths = dict()
        for path_id in data['paths']:
            self.paths[path_id] = Path(data['paths'][path_id], self)

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

    def get_path(self, path_id):
        return self.paths[path_id]

    def get_return_expr(self):
        return self.return_expr

    def get_loops(self):
        return self.loops

    def get_loop(self, loop_id):
        return self.loops[loop_id]

    def get_procedures(self):
        return self.procedures

    def get_procedure(self, procedure_id):
        return self.procedure[procedure_id]

    def clear_paths(self):
        self.paths = dict()

    def add_path(self, path_id, path):
        self.paths[path_id] = path

    def to_json(self):

        data = dict()
        data['program_name'] = self.get_program_name()
        data['function_name'] = self.get_function_name()
        data['variables'] = self.variables
        data['constrains'] = self.get_constrains()
        data['paths'] = self.get_paths()
        data['implements'] = self.get_implements()
        data['loops'] = dict()
        for loop_id, loop in self.get_loops().items():
            data['loops'][loop_id] = loop.to_json()

        return data

    def output_json(self, path_file):

        data = self.to_json()
        with open(path_file, 'w') as f:
            json.dump(data, f, indent=4)


class Loop:

    """Loop封装类, 一个Loop指代一段循环的代码，包括了所涉及到的临时变量和它们的初始化，循环体等内容"""

    def __init__(self, loop_json):

        self.variables = loop_json['variables']
        self.initialize = loop_json['initialize']
        self.loop_body = loop_json['loop_body']

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

    def to_json(self):
        data = dict()
        data['variables'] = self.variables
        data['initialize'] = self.initialize
        data['loop_body'] = self.get_loop_body()
        return data


class Procedure:

    NOT_EXIST = "not exist"

    """Procedure封装类, 一个Procedure指代一段顺序执行的代码，我们用所涉及到的所有变量的更新式来记录这段代码所代表的语义"""

    def __init__(self, procedure_json):
        self.procedure = procedure_json

    def get_update_expr(self, var):
        if var not in self.procedure.keys():
            return self.NOT_EXIST
        else:
            return self.procedure[var]


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
            if p.startswith('{procedure') and p.endswith('}'):
                self.path.append(path_data.get_procedure(p[len('{procedure:'):-len('}')]))
            elif p.startswith('{loop') and p.endswith('}'):
                self.path.append(path_data.get_loop(p[len('{loop:'):-len('}')]))

    def set_implement(self, implement):
        self.implement = implement

    def add_constrain(self, constrain):
        self.constrain = '(' + self.constrain + ')' + '&&' + '(' + constrain + ')'

