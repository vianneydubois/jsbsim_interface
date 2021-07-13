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


def run_jsbsim(jsbsim_source_path, jsbsim_script_path):
    command = 'python3 '
    command += jsbsim_source_path
    command += ' --script=' + jsbsim_script_path
    os.system(command)
    return


JSBSIM_SCRIPT_PATH = 'aircraft/cessna_172/scripts/trim_cruise.xml'
AIRCRAFT_NAME = 'cessna_172'
INIT_FILE_NAME = 'airborne'

JSBSIM_SOURCE_PATH = '/Users/vianneydubois/PycharmProjects/jsbsim_interface/resources/JSBSim.py'

edit_jsbsim_script(JSBSIM_SCRIPT_PATH, AIRCRAFT_NAME, INIT_FILE_NAME)

run_jsbsim(JSBSIM_SOURCE_PATH, JSBSIM_SCRIPT_PATH)

# knowing the aircraft name, the program should know the paths, OR knowing the path, it should know the name
# the script should be taken from a script library, then copied in the desired aircraft file
# then sim is ran
# then the custom script is deleted
