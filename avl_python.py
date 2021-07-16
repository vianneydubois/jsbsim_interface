import os
import subprocess as sp
import numpy as np
from openmdao.utils.file_wrap import InputFileGenerator, FileParser


def generate_geometry(input_template_path: str, input_generated_path: str,
                      aileron_x_c: float, elevator_x_c: float, rudder_x_c: float):
    mach = 0.78
    sref = 122.4
    bref = 34.1
    cref = 4.2
    sweep_0 = 0.472709635153824

    ## WING
    # section 0
    xle0 = 0
    yle0 = 0
    c0 = 5.968267075021899
    # section 2
    yle2 = bref/2
    xle2 = yle2 * np.tan(sweep_0)
    c2 = 1.6599009162290415
    # section 1
    yle1 = 0.8*bref/2
    xle1 = yle1 * np.tan(sweep_0)
    c1 = c0 + 0.8 * (c2 - c0)

    ## HORIZONTAL TAIL
    x_translate_ht = 19.341
    z_translate_ht = 2
    # section 0
    ht_xle0 = 0
    ht_yle0 = 0
    ht_c0 = 4.19446
    # section 1
    ht_xle1 = 3.8419
    ht_yle1 = 5.84509
    ht_c1 = 1.25834

    ## VERTICAL TAIL
    x_translate_vt = 17.137
    z_translate_vt = 2.749
    # section 0
    vt_xle0 = 0
    vt_zle0 = 0
    vt_c0 = 5.90875
    # section 1
    vt_xle1 = 5.724
    vt_zle1 = 6.70056
    vt_c1 = 1.77262


    parser = InputFileGenerator()
    parser.set_template_file(input_template_path)
    parser.set_generated_file(input_generated_path)

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


def run_avl(avl_path: str, avl_session_path: str, avl_stability_path: str):
    # Creating a string containing all the commands
    command_string = ""
    with open(avl_session_path, 'r') as avl_session:
        lines = avl_session.readlines()
        for line in lines:
            command_string += line

    command_string = command_string.encode('ascii')

    # if the output file already exists, it will make the execution crash since AVL will ask if the
    # file must be overwritten or not, and it will desynchronize the program
    if os.path.exists(avl_stability_path):
        os.remove(avl_stability_path)

    avl_ps = sp.Popen([avl_path], stdin=sp.PIPE, stdout=None, stderr=None)
    avl_ps.communicate(input=command_string)  # sending the commands to AVL


def read_output(avl_stability_path: str) -> list:
    # reading the output file path from the avl_session file
    #with open(avl_session_path, 'r') as avl_session:
     #   output_stab_path = avl_session.readlines()[6][:-1]  # removing the '\n' character

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


def compute_range(avl_path: str,
                  avl_session_path: str,
                  input_template_path: str,
                  input_generated_path: str,
                  avl_stability_path: str,
                  aileron_range: list,
                  elevator_range: list,
                  rudder_range: list) -> list:

    # number of AVL run to perform
    n_aileron = len(aileron_range)
    n_elevator = len(elevator_range)
    n_rudder = len(rudder_range)
    run_number = max(n_aileron, n_elevator, n_rudder)

    # completing the FCS dimensions lists so that they have the same length
    for list in [aileron_range, elevator_range, rudder_range]:
        n = len(list)
        if n < run_number:
            list += [list[-1]] * (run_number - n)


    control_derivatives = np.zeros((6, run_number))
    control_derivatives[::2] = aileron_range, elevator_range, rudder_range

    for i in range(run_number):
        generate_geometry(input_template_path, input_generated_path,
                          aileron_range[i], elevator_range[i], rudder_range[i])
        run_avl(avl_path, avl_session_path, avl_stability_path)
        control_derivatives[1::2, i] =  read_output(avl_stability_path)

    return control_derivatives