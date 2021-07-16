import os
import subprocess as sp
import numpy as np
from openmdao.utils.file_wrap import InputFileGenerator, FileParser


def run_avl(avl_path: str, avl_session_path: str, avl_stability_path: str):
    # Creating a string containing all the commands
    command_string = ""
    with open(avl_session_path, 'r') as avl_session:
        lines = avl_session.readlines()
        for line in lines:
            command_string += line

    command_string = command_string.encode('ascii')

    # if the output file already exists, it will make the execution crash since AVL will ask if the
    # file must be overwritten or not, and it will desynchronize the program
    if os.path.exists(avl_stability_path):
        os.remove(avl_stability_path)

    avl_ps = sp.Popen([avl_path], stdin=sp.PIPE, stdout=None, stderr=None)
    avl_ps.communicate(input=command_string)  # sending the commands to AVL

    return None


def read_output(avl_stability_path: str) -> list:

    parser = FileParser()
    parser.set_file(avl_stability_path)
    derivative_list = []

    parser.mark_anchor('Cld1')
    derivative_list.append(parser.transfer_var(0, 6))
    parser.reset_anchor()
    parser.mark_anchor('Cmd2')
    derivative_list.append(parser.transfer_var(0, 10))
    parser.reset_anchor()
    parser.mark_anchor('Cnd3')
    derivative_list.append(parser.transfer_var(0, 12))

    return derivative_list
