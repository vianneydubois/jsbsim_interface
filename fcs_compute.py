import aeromatic_script_from_xml as aeromatic_xml
import aeromatic_script_editor as aeromatic_edit
import aeromatic_run as aeromatic
import avl_python_functions as avl
import avl_jsbsim_coefficient as avl_jsbsim
import jsbsim_run as jsbsim
import os


# aeromatic run : function


def compute(desired_script_name, init_file_name, aeromatic_script_path, xml_file_path, aircraft_name, aeromatic_path):
    # 1 : run aeromatic to generate the JSBSim aircraft config file
    # aeromatic_xml.generate_script(aeromatic_script_path, xml_file_path, aircraft_name)
    # aeromatic_edit.edit_aeromatic_script(aeromatic_script_path, aircraft_name)
    # aeromatic.aeromatic_run(aeromatic_script_path, aeromatic_path)

    # 2 : run AVL
    #avl.generate_geometry('resources/geom.avl', 'avl_gen_files/gen_geom.avl', xml_file_path)
    #avl.edit_avl_session('avl_gen_files/session.txt', 'avl_gen_files/gen_geom.avl', 'avl_gen_files/out.txt', 0.8)
    #avl.run_avl('resources/executables/avl335', 'avl_gen_files/session.txt',
    #            'avl_gen_files/gen_geom.avl', 'avl_gen_files/out.txt')

    # 3 : integrate AVL coefficients in JSBSim aircraft config file
    jsbsim_config_path = os.path.join('aircraft', aircraft_name, aircraft_name + '.xml')
    #avl_jsbsim.integrate_avl_coef('avl_gen_files/out.txt', jsbsim_config_path)

    # 4 : run JSSim
    jsbsim.copy_script_file(desired_script_name, aircraft_name)
    jsbsim.edit_jsbsim_script(desired_script_name, aircraft_name, init_file_name)
    jsbsim.run_jsbsim('resources/JSBSim.py', aircraft_name, desired_script_name)
    jsbsim.remove_script_file(aircraft_name)

    # 5 : post processing
    return None


aeromatic_script_path = os.path.join('resources', 'aeromatic_script.txt')
aeromatic_path = os.path.join('resources', 'executables', 'aeromatic')
aircraft_name = 'new_cessna'
aircraft_xml_source = 'resources/data/aircraft.xml'

compute('roll', 'airborne', aeromatic_script_path, aircraft_xml_source, aircraft_name, aeromatic_path)
