"""
Generates an Aeromatic++ script file from an XML data file
"""

import os.path
import xml.etree.ElementTree as ET


def generate_script(aeromatic_script_path: str, xml_file_path: str, aircraft_name: str):
    aircraft_dir = 'aircraft'

    script = open(aeromatic_script_path, 'r+')
    script_lines = script.readlines()

    # output directory
    script_lines[0] = os.path.abspath(aircraft_dir) + '\n'
    # aircraft name
    script_lines[3] = aircraft_name + '\n'
    script_lines[28] = aircraft_name + '_engine\n'
    script_lines[34] = aircraft_name + '_prop\n'

    doc = ET.parse(xml_file_path)
    root = doc.getroot()
    geometry = root.find('data').find('geometry')
    tlar = root.find('data').find('TLAR')
    weight = root.find('data').find('weight')
    propulsion = root.find('data').find('propulsion')
    landing_gear = root.find('data').find('landing_gear')

    # stall speed
    script_lines[7] = "{:.3f}".format(float(tlar.find('approach_speed').text) / 1.3 * 3.6) + '\n'
    # MTWO
    script_lines[8] = weight.find('aircraft').find('MTOW').text + '\n'
    # OWE
    script_lines[9] = weight.find('aircraft').find('OWE').text + '\n'
    # Ixx
    script_lines[10] = weight.find('inertia').find('Ixx').text + '\n'
    # Iyy
    script_lines[11] = weight.find('inertia').find('Iyy').text + '\n'
    # Izz
    script_lines[12] = weight.find('inertia').find('Izz').text + '\n'
    # length
    script_lines[13] = geometry.find('fuselage').find('length').text + '\n'
    # wing shape (0 : straight, 1 : elliptical, 2 : delta)
    script_lines[14] = '0' + '\n'
    # wing span
    script_lines[15] = geometry.find('wing').find('span').text + '\n'
    # wing area
    script_lines[16] = geometry.find('wing').find('area').text + '\n'
    # wing aspect ratio
    script_lines[17] = geometry.find('wing').find('aspect_ratio').text + '\n'
    # wing taper ratio
    script_lines[18] = "{:.3f}".format(float(geometry.find('wing').find('tip_chord').text) / float(
        geometry.find('wing').find('root_chord').text)) + '\n'
    # wing root chord
    script_lines[19] = geometry.find('wing').find('root_chord').text + '\n'
    # wing incidence
    script_lines[20] = geometry.find('wing').find('incidence').text + '\n'
    # wing dihedral
    script_lines[21] = geometry.find('wing').find('dihedral').text + '\n'
    # wing sweep quarter chord
    script_lines[22] = geometry.find('wing').find('sweep_25').text + '\n'
    # horizontal tail area
    script_lines[23] = geometry.find('horizontal_tail').find('area').text + '\n'
    # horizontal_tail lever arm
    script_lines[24] = geometry.find('horizontal_tail').find('arm').text + '\n'
    # vertical tail area
    script_lines[25] = geometry.find('vertical_tail').find('area').text + '\n'
    # vertical tail lever arm
    script_lines[26] = geometry.find('vertical_tail').find('arm').text + '\n'
    # propulsion
    script_lines[27] = 'yes' + '\n'
    # engine name
    #
    # engine count
    script_lines[29] = geometry.find('propulsion').find('count').text + '\n'
    # engine layout (0 : fwd fuselage, 2 : aft fuselage, 3 : wings)
    script_lines[30] = geometry.find('propulsion').find('layout').text + '\n'
    # engine type (0 : piston, 1 : turboprop, 2 : turbine, 3 : rocket, 4 : electric)
    script_lines[31] = propulsion.find('engine').find('type').text + '\n'
    # engine power
    script_lines[32] = propulsion.find('engine').find('power').text + '\n'
    # engine max rpm
    script_lines[33] = propulsion.find('engine').find('max_rpm').text + '\n'
    # engine name
    #
    # propeller diameter
    script_lines[35] = propulsion.find('propeller').find('diameter').text + '\n'
    # propeller fixed pitch
    if float(propulsion.find('propeller').find('fixed_pitch').text):
        script_lines[36] = 'yes' + '\n'
    else:
        script_lines[36] = 'no' + '\n'
    # landing gear
    script_lines[37] = 'yes' + '\n'
    # landing gear retractable
    if float(landing_gear.find('retractable').text):
        script_lines[38] = 'yes' + '\n'
    else:
        script_lines[38] = 'no' + '\n'
    # nose/tail LG type (0 : steering, 1 : castering, 2 : fixed)
    script_lines[39] = landing_gear.find('type').text + '\n'
    # taildragger
    if float(landing_gear.find('taildragger').text):
        script_lines[40] = 'yes' + '\n'
    else:
        script_lines[40] = 'no' + '\n'
    # flaps
    if float(geometry.find('extra').find('flaps').text):
        script_lines[41] = 'yes' + '\n'
    else:
        script_lines[41] = 'no' + '\n'
    # spoilers
    if float(geometry.find('extra').find('spoilers').text):
        script_lines[42] = 'yes' + '\n'
    else:
        script_lines[42] = 'no' + '\n'
    # chute
    if float(geometry.find('extra').find('chute').text):
        script_lines[43] = 'yes' + '\n'
    else:
        script_lines[43] = 'no' + '\n'

    script.seek(0)
    script.writelines(script_lines)
    script.close()


XML_PATH = 'resources/data/aircraft.xml'

AIRCRAFT_NAME = 'c172'

AEROMATIC_SCRIPT_FOLDER = 'resources'
AEROMATIC_SCRIPT_FILE = 'script_aeromatic.txt'

aeromatic_script_path = os.path.join(AEROMATIC_SCRIPT_FOLDER, AEROMATIC_SCRIPT_FILE)

generate_script(aeromatic_script_path, XML_PATH, AIRCRAFT_NAME)
