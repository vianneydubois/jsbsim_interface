# Runs AeromatiC++

import subprocess as sp


def aeromatic_run(aeromatic_script_path, aeromatic_path):
    # Creating a string containing all the commands
    command_string = ''
    with open(aeromatic_script_path, 'r') as aeromatic_script:
        lines = aeromatic_script.readlines()
        for line in lines:
            command_string += line

    command_string = command_string.encode('ascii')

    aeromatic_ps = sp.Popen([aeromatic_path], stdin=sp.PIPE, stdout=None, stderr=None)
    aeromatic_ps.communicate(input=command_string)  # sending the commands to aeromatic
    return None
