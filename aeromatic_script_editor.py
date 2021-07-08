# Edits the aeromatic script
# with the desired path an name for the ouput files/folder


import os.path

AEROMATIC_SCRIPT_FOLDER = 'resources'
AEROMATIC_SCRIPT_FILE = 'script_aeromatic.txt'
aeromatic_script_path = os.path.join(AEROMATIC_SCRIPT_FOLDER, AEROMATIC_SCRIPT_FILE)

aircraft_dir = 'resources' + os.path.sep + 'aircraft'

with open(aeromatic_script_path, 'r+') as aeromatic_script:
    script_lines = aeromatic_script.readlines()
    script_lines[0] = os.path.abspath(aircraft_dir) +'\n'
    aeromatic_script.seek(0)
    aeromatic_script.writelines(script_lines)
