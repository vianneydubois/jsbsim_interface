# Edits the aeromatic script :
# with the desired path for the output folder
# it is supposed that the aircraft is a piston engine, propeller driven aircraft

# what needs to be done : create a folder for the JSBSim script and init files

# WARNING : the aircraft dir can not be a child of another dir, aeromatic seems to ignore
# the last dir if the path is too long


import os.path

AEROMATIC_SCRIPT_FOLDER = 'resources'
AEROMATIC_SCRIPT_FILE = 'script_aeromatic.txt'

AIRCRAFT_NAME = 'tb9'


aeromatic_script_path = os.path.join(AEROMATIC_SCRIPT_FOLDER, AEROMATIC_SCRIPT_FILE)
aircraft_dir = 'aircraft'

with open(aeromatic_script_path, 'r+') as aeromatic_script:
    script_lines = aeromatic_script.readlines()

    script_lines[0] = os.path.abspath(aircraft_dir) + '\n'
    script_lines[3] = AIRCRAFT_NAME + '\n'
    script_lines[28] = AIRCRAFT_NAME + '_engine\n'
    script_lines[34] = AIRCRAFT_NAME + '_prop\n'

    aeromatic_script.seek(0)
    aeromatic_script.writelines(script_lines)
