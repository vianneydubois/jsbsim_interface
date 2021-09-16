# Edits the aeromatic script :
# with the desired path for the output folder
# it is considered that the aircraft is a piston engine, propeller driven aircraft

# WARNING : the aircraft dir can not be a child of another dir, aeromatic seems to ignore
# the last dir if the path is too long

import os.path


def edit_aeromatic_script(aeromatic_script_path: str, aircraft_name: str):

    with open(aeromatic_script_path, 'r+') as aeromatic_script:
        script_lines = aeromatic_script.readlines()

        aircraft_dir = 'aircraft'

        script_lines[0] = os.path.abspath(aircraft_dir) + '\n'
        script_lines[3] = aircraft_name + '\n'
        script_lines[28] = aircraft_name + '_engine\n'
        script_lines[34] = aircraft_name + '_prop\n'

        aeromatic_script.seek(0)
        aeromatic_script.writelines(script_lines)

    return None
