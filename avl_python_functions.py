import os
import subprocess as sp
import numpy as np
from openmdao.utils.file_wrap import InputFileGenerator, FileParser
import xml.etree.ElementTree as et


def generate_geometry(template_path: str, generated_file_path: str, geometry_source_path: str):
    aileron_x_c = 0.80
    elevator_x_c = 0.66
    rudder_x_c = 0.62

    geometry_source = et.parse(geometry_source_path)
    data = geometry_source.getroot().find('data')
    geometry = data.find('geometry')
    wing = geometry.find('wing')
    htail = geometry.find('horizontal_tail')
    vtail = geometry.find('vertical_tail')
    tlar = data.find('TLAR')

    mach = float(tlar.find('cruise_mach').text)
    sref = float(wing.find('area').text)
    bref = float(wing.find('span').text)
    cref = sref / bref

    ## WING
    c0 = float(wing.find('root_chord').text)
    c2 = float(wing.find('tip_chord').text)
    sweep_25 = np.deg2rad(float(wing.find('sweep_25').text))
    sweep_0 = np.arctan(np.tan(sweep_25) + 1 / 4 / bref / 2 * (c0 - c2))
    # section 0
    xle0 = 0
    yle0 = 0
    # section 1 - aileron inward limit
    aileron_in_limit = 0.8
    yle1 = aileron_in_limit * bref / 2
    xle1 = yle1 * np.tan(sweep_0)
    c1 = c0 + 0.8 * (c2 - c0)
    # section 2
    yle2 = bref / 2
    xle2 = yle2 * np.tan(sweep_0)
    c2 = float(wing.find('tip_chord').text)

    ## HORIZONTAL TAIL
    x_translate_ht = float(htail.find('x_le_offset').text)
    z_translate_ht = float(htail.find('z_le_offset').text)
    # section 0
    ht_xle0 = 0
    ht_yle0 = 0
    ht_c0 = float(htail.find('root_chord').text)
    # section 1
    ht_xle1 = float(htail.find('tip_x_offset').text)
    ht_yle1 = float(htail.find('span').text) / 2
    ht_c1 = float(htail.find('tip_chord').text)

    ## VERTICAL TAIL
    x_translate_vt = float(vtail.find('x_le_offset').text)
    z_translate_vt = float(vtail.find('z_le_offset').text)
    # section 0
    vt_xle0 = 0
    vt_zle0 = 0
    vt_c0 = float(vtail.find('root_chord').text)
    # section 1
    vt_xle1 = float(vtail.find('tip_x_offset').text)
    vt_zle1 = float(vtail.find('span').text)
    vt_c1 = float(vtail.find('tip_chord').text)

    ## Completing the template file
    parser = InputFileGenerator()
    parser.set_template_file(template_path)
    parser.set_generated_file(generated_file_path)

    parser.mark_anchor("#Mach")
    parser.transfer_var(float(mach), 1, 1)
    parser.reset_anchor()

    parser.mark_anchor("#Sref")
    parser.transfer_var(float(sref), 1, 1)
    parser.transfer_var(float(cref), 1, 2)
    parser.transfer_var(float(bref), 1, 3)
    parser.reset_anchor()

    # WING
    # section 0
    parser.mark_anchor("#Xle")
    parser.transfer_var(float(c0), 1, 4)
    # section 1
    parser.mark_anchor("#Xle")
    parser.transfer_var(float(xle1), 1, 1)
    parser.transfer_var(float(yle1), 1, 2)
    parser.transfer_var(float(c1), 1, 4)
    parser.mark_anchor("CONTROL")
    parser.transfer_var(float(aileron_x_c), 1, 3)
    # section 2
    parser.mark_anchor("#Xle")
    parser.transfer_var(float(xle2), 1, 1)
    parser.transfer_var(float(yle2), 1, 2)
    parser.transfer_var(float(c2), 1, 4)
    parser.mark_anchor("CONTROL")
    parser.transfer_var(float(aileron_x_c), 1, 3)

    # HORIZONTAL TAIL
    parser.reset_anchor()
    parser.mark_anchor('Stab')
    parser.mark_anchor('TRANSLATE')
    parser.transfer_var(float(x_translate_ht), 1, 1)
    parser.transfer_var(float(z_translate_ht), 1, 3)
    # section 0
    parser.mark_anchor("#Xle")
    parser.transfer_var(float(ht_c0), 1, 4)
    parser.mark_anchor("CONTROL")
    parser.transfer_var(float(elevator_x_c), 1, 3)
    # section 1
    parser.mark_anchor("#Xle")
    parser.transfer_var(float(ht_xle1), 1, 1)
    parser.transfer_var(float(ht_yle1), 1, 2)
    parser.transfer_var(float(ht_c1), 1, 4)
    parser.mark_anchor("CONTROL")
    parser.transfer_var(float(elevator_x_c), 1, 3)

    # VERTICAL TAIL
    parser.reset_anchor()
    parser.mark_anchor('Fin')
    parser.mark_anchor('TRANSLATE')
    parser.transfer_var(float(x_translate_vt), 1, 1)
    parser.transfer_var(float(z_translate_vt), 1, 3)
    # section 0
    parser.mark_anchor("#Xle")
    parser.transfer_var(float(vt_c0), 1, 4)
    parser.mark_anchor("CONTROL")
    parser.transfer_var(float(rudder_x_c), 1, 3)
    # section 1
    parser.mark_anchor("#Xle")
    parser.transfer_var(float(vt_xle1), 1, 1)
    parser.transfer_var(float(vt_zle1), 1, 3)
    parser.transfer_var(float(vt_c1), 1, 4)
    parser.mark_anchor("CONTROL")
    parser.transfer_var(float(rudder_x_c), 1, 3)

    parser.generate()

    return None


def edit_avl_session(avl_session_path: str, geometry_path: str, avl_output_path: str, density: float):

    geometry_path = os.path.abspath(geometry_path)
    avl_output_path = os.path.abspath(avl_output_path)

    parser = FileParser()
    parser.set_file(geometry_path)
    parser.mark_anchor('#Mach')
    mach = float(parser.transfer_var(1, 1))

    session_lines = ['LOAD', geometry_path]
    session_lines += ['OPER']
    session_lines += ['M', 'MN', str(mach)]
    session_lines += ['D', str(density), '']
    session_lines += ['X', 'ST', avl_output_path, '']
    session_lines += ['QUIT']

    with open(avl_session_path, 'w') as session:
        session.writelines('\n'.join(session_lines))
    return None


def run_avl(avl_path: str, avl_session_path: str, geometry_path: str, avl_output_path: str):

    edit_avl_session(avl_session_path, geometry_path, avl_output_path, 1.0)

    # Creating a string containing all the commands
    command_string = ""
    with open(avl_session_path, 'r') as avl_session:
        lines = avl_session.readlines()
        for line in lines:
            command_string += line

    command_string = command_string.encode('ascii')

    # if the output file already exists, it will make the execution crash since AVL will ask if the
    # file must be overwritten or not, and it will desynchronize the program
    if os.path.exists(avl_output_path):
        os.remove(avl_output_path)

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


avl_session_path = 'avl_gen_files/session.txt'
avl_geometry_path = 'avl_gen_files/gen_geom.avl'
avl_output_path = 'avl_gen_files/stab.txt'
avl_template_path = 'resources/geom.avl'
avl_exe_path = 'resources/executables/avl335'
aircraft_data_path = 'resources/data/aircraft.xml'


generate_geometry(avl_template_path, avl_geometry_path, aircraft_data_path)
run_avl(avl_exe_path, avl_session_path, avl_geometry_path, avl_output_path)

