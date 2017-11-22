#!/usr/bin/python
# -*- coding:utf-8 -*-

import json

class Path:

    """path文件封装类"""

    def __init__(self, path_file):

        with open(path_file) as f:
            data = json.load(f)

        self.program_name = data['program_name']
        self.function_name = data['function_name']

        self.variables = data['variables']
        self.input_variables = data['input_variables']
        self.paths = data['paths']
        self.constrains = data['constrains']
        self.return_expr = data['return']

        self.loops = dict()

        for loopid in data['loops'].keys():
            self.loops[loopid] = Loop(data['loops'][loopid])

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

    def get_return_expr(self):
        return self.return_expr

    def get_loops(self):
        return self.loops

class Loop:

    """Loop封装类"""

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

    def get_loop_body(self):
        return self.loop_body


'''
path_file = '../case/harmonic/harmonic.pth'
path = Path(path_file)
loops = path.get_loops()
for loop in loops:
    print(loops[loop].get_loop_body())
'''
