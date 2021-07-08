## Runs AeromatiC++
import os.path
import subprocess as sp

AEROMATIC_SCRIPT_FOLDER = 'resources'
AEROMATIC_SCRIPT_FILE = 'script_aeromatic.txt'
aeromatic_script_path = os.path.join(AEROMATIC_SCRIPT_FOLDER, AEROMATIC_SCRIPT_FILE)

AEROMATIC_EXE_FOLDER = os.path.expanduser('executables')
AEROMATIC_EXE_FILE = 'aeromatic'
aeromatic_path = os.path.join(AEROMATIC_EXE_FOLDER, AEROMATIC_EXE_FILE)

# Creating a sting containing all the commands
command_string = ''
with open(aeromatic_script_path, 'r') as aeromatic_script:
    lines = aeromatic_script.readlines()
    for line in lines:
        command_string += line

command_string = command_string.encode('ascii')

print(command_string)

aeromatic_ps = sp.Popen([aeromatic_path], stdin=sp.PIPE, stdout=None, stderr=None)
aeromatic_ps.communicate(input=command_string)  # sending the commands to AVL
