import aeromatic_script_from_xml as aeromatic_xml
import aeromatic_script_editor as aeromatic_edit
import aeromatic_run as aeromatic
import avl_python_functions as avl
import avl_jsbsim_coefficient as avl_jsbsim
import jsbsim_run as jsbsim
import post_processing as pp
import os
import platform


def compute(desired_script_name: str, init_file_name: str, xml_file_path: str, aircraft_name: str, fcs_x_c: list):
    """
    :param desired_script_name: XML JSBSim script file for the desired manoeuvre
    :param init_file_name: XML JSBSim initialize file
    :param xml_file_path: XML geometry source file for the aircraft
    :param aircraft_name: name of the aircraft, will be the name of the aircraft folder
    :param fcs_x_c: flight control surfaces hinge positions - [ailerons, elevator, rudder]
    :return:
    """
    os_name = platform.system()  # required for executables choices

    # 1 : running Aeromatic to generate the JSBSim aircraft config file
    aeromatic_script_path = os.path.join('resources', 'aeromatic_script.txt')
    aeromatic_path = None
    if os_name == 'Darwin':
        aeromatic_path = os.path.join('resources', 'executables', 'mac', 'aeromatic')
    elif os_name == 'Windows':  # for Windows users
        aeromatic_path = os.path.join('resources', 'executables', 'win', 'aeromatic.exe')

    aeromatic_xml.generate_script(aeromatic_script_path, xml_file_path, aircraft_name)
    aeromatic_edit.edit_aeromatic_script(aeromatic_script_path, aircraft_name)  # useless?
    aeromatic.aeromatic_run(aeromatic_script_path, aeromatic_path)

    # 2 : running AVL
    geometry_template = os.path.join('resources', 'geom.avl')
    generated_geometry = os.path.join('avl_gen_files', 'gen_geom.avl')
    avl_session = os.path.join('avl_gen_files', 'session.txt')
    avl_output = os.path.join('avl_gen_files', 'out.txt')
    air_density = 0.8  # SI units
    avl_path = None
    if os_name == 'Darwin':  # for macOS users
        avl_path = os.path.join('resources', 'executables', 'mac', 'avl335')
    elif os_name == 'Windows':  # for Windows users
        avl_path = os.path.join('resources', 'executables', 'win', 'avl335.exe')

    avl.generate_geometry(geometry_template, generated_geometry, xml_file_path, fcs_x_c)
    avl.edit_avl_session(avl_session, generated_geometry, avl_output, air_density)
    avl.run_avl(avl_path, avl_session, generated_geometry, avl_output)

    # 3 : integrating AVL coefficients in JSBSim aircraft config file
    jsbsim_config_path = os.path.join('aircraft', aircraft_name, aircraft_name + '.xml')

    avl_jsbsim.integrate_avl_coef(avl_output, jsbsim_config_path)

    # 4 : running JSSim
    jsbsim_path = os.path.join('resources', 'JSBSim.py')

    jsbsim.copy_script_file(desired_script_name, aircraft_name)
    jsbsim.edit_jsbsim_script(desired_script_name, aircraft_name, init_file_name)
    jsbsim.run_jsbsim(jsbsim_path, aircraft_name, desired_script_name)
    jsbsim.remove_script_file(aircraft_name)

    print(avl_path)
    # 5 : post processing
    result = False
    if desired_script_name == 'yaw':
        delta_psi = 15
        t_lim = 7
        result = pp.process_rudder(aircraft_name, delta_psi, t_lim)
    elif desired_script_name == 'roll':
        delta_phi = -60
        t_lim = 11
        result = pp.process_roll(aircraft_name, delta_phi, t_lim)
    return result


aircraft_name = 'c172'
script = 'yaw'
init = 'airborne'
aircraft_xml_source = os.path.join('resources', 'data', 'aircraft.xml')
fcs_x_c = [0.8, 0.66, 0.62]  # aileron, elevator, rudder

print(compute(script, init, aircraft_xml_source, aircraft_name, fcs_x_c))

# folder for avl template and aeromatic script
