import os
import xml.etree.ElementTree as et


def edit_jsbsim_script(jsbsim_script_path: str, aircraft_name: str, init_file_name: str):
    script = et.parse(jsbsim_script_path)
    root = script.getroot()
    use = root.find('use')

    use.attrib['aircraft'] = aircraft_name  # update aircraft name
    use.attrib['initialize'] = 'scripts/' + init_file_name  # update init file name

    # edit output name
    output_name = 'aircraft/' + aircraft_name + '/result.csv'
    root.find('output').attrib['name'] = output_name

    script_str = et.tostring(root)

    with open(jsbsim_script_path, 'w') as script_file:
        script_file.write('<?xml version="1.0" encoding="utf-8"?>\n')
        script_file.write('<?xml-stylesheet type="text/xsl" href="http://jsbsim.sf.net/JSBSimScript.xsl"?>\n')
        script_file.write(script_str.decode())

    return


def run_jsbsim(jsbsim_source_path: str, jsbsim_script_path: str):
    command = 'python3 '
    command += jsbsim_source_path
    command += ' --script=' + jsbsim_script_path
    os.system(command)
    return


def copy_script_file(desired_script_name: str, aircraft_name: str):

    # create a 'scripts' folder
    scripts_folder_path = os.path.join('aircraft', aircraft_name, 'scripts')
    os.makedirs(scripts_folder_path)

    # copy script file
    source_path = os.path.join('resources', 'sim_scripts', desired_script_name + '.xml')
    with open(source_path, 'r') as source:
        # copy source script
        source_script = source.readlines()

        destination_path = os.path.join(scripts_folder_path, desired_script_name + '.xml')
        with open(destination_path, 'w') as destination:
            # write into a new file
            destination.writelines(source_script)

    # copy initialize file
    init_source_file = os.path.join('resources', 'sim_init', 'airborne.xml')
    with open(init_source_file, 'r') as source:
        # copy source script
        source_init = source.readlines()

        destination_path = os.path.join(scripts_folder_path, '.xml')
        with open(destination_path, 'w') as destination:
            # write into a new file
            destination.writelines(source_init)

    return


def remove_script_file(aircraft_name: str):
    # remove the 'scripts' folder
    return


JSBSIM_SCRIPT_PATH = 'aircraft/cessna_172/scripts/trim_cruise.xml'
AIRCRAFT_NAME = 'cessna_172'
INIT_FILE_NAME = 'airborne'

JSBSIM_SOURCE_PATH = '/Users/vianneydubois/PycharmProjects/jsbsim_interface/resources/JSBSim.py'

edit_jsbsim_script(JSBSIM_SCRIPT_PATH, AIRCRAFT_NAME, INIT_FILE_NAME)

run_jsbsim(JSBSIM_SOURCE_PATH, JSBSIM_SCRIPT_PATH)

copy_script_file('ok', 'c172')

# knowing the aircraft name, the program should know the paths, OR knowing the path, it should know the name
# the script should be taken from a script library, then copied in the desired aircraft file
# then sim is ran
# then the custom script is deleted

# a generic folder with all the init files and all the scripts
#