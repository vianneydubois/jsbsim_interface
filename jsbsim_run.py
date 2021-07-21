import os
import shutil
import xml.etree.ElementTree as et


def edit_jsbsim_script(script_name: str, aircraft_name: str, init_file_name: str):
    # updates the script with the aircraft name and the initialize file
    jsbsim_script_path = os.path.join('aircraft', aircraft_name, 'scripts', script_name + '.xml')
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


def run_jsbsim(jsbsim_source_path: str, aircraft_name: str, script_name: str):
    # runs jsbsim with the aircraft name and the selected script
    jsbsim_script_path = os.path.join('aircraft', aircraft_name, 'scripts', script_name + '.xml')
    command = 'python3 '
    command += jsbsim_source_path
    command += ' --script=' + jsbsim_script_path
    os.system(command)
    return


def copy_script_file(desired_script_name: str, aircraft_name: str):
    # copy the script and init files in the aircraft folder in vue of jsbsim run

    # create a 'scripts' folder
    scripts_folder_path = os.path.join('aircraft', aircraft_name, 'scripts')
    if not os.path.exists(scripts_folder_path):
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
        # copy source scriptq
        source_init = source.readlines()

        destination_path = os.path.join(scripts_folder_path, 'airborne.xml')
        with open(destination_path, 'w') as destination:
            # write into a new file
            destination.writelines(source_init)

    return


def remove_script_file(aircraft_name: str):
    # removes the 'scripts' folder created in the aircraft folder prior to jsbsim run
    scripts_folder_path = os.path.join('aircraft', aircraft_name, 'scripts')
    shutil.rmtree(scripts_folder_path)
    return


# AIRCRAFT_NAME = 'c172'
# INIT_FILE_NAME = 'airborne'
# SCRIPT_FILE_NAME = 'yaw'
#
# JSBSIM_SOURCE_PATH = os.path.join('resources', 'JSBSim.py')
#
# jsbsim_script_path = os.path.join('aircraft', AIRCRAFT_NAME, 'scripts', SCRIPT_FILE_NAME + '.xml')
#
# copy_script_file(SCRIPT_FILE_NAME, AIRCRAFT_NAME)
# edit_jsbsim_script(SCRIPT_FILE_NAME, AIRCRAFT_NAME, INIT_FILE_NAME)
# run_jsbsim(JSBSIM_SOURCE_PATH, AIRCRAFT_NAME, SCRIPT_FILE_NAME)
# remove_script_file(AIRCRAFT_NAME)
