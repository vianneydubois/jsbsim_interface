import xml.etree.ElementTree as et
from xml.dom import minidom
import numpy as np
from openmdao.utils.file_wrap import FileParser


def integrate_avl_coef(avl_output_path: str, jsbsim_config_path: str):
    # reads the coefficients in the AVL output file
    # inserts them in the JSBSim aircraft configuration file

    parser = FileParser()
    parser.set_file(avl_output_path)
    parser.mark_anchor('Cld1')
    Cld = np.rad2deg(parser.transfer_var(0, 6))
    parser.reset_anchor()
    parser.mark_anchor('Cmd2')
    Cmd = np.rad2deg(parser.transfer_var(0, 10))
    parser.reset_anchor()
    parser.mark_anchor('Cnd3')
    Cnd = np.rad2deg(parser.transfer_var(0, 12))

    doc = et.parse(jsbsim_config_path)
    root = doc.getroot()
    aerodynamics = root.find('aerodynamics')

    for ax in aerodynamics.iter('axis'):

        if ax.attrib['name'] == 'PITCH':
            for f in ax.iter('function'):
                if f.attrib['name'] == 'aero/moment/Pitch_elevator':
                    product = f.find('product')
                    table = product.find('table')
                    table_data = table.find('tableData').text
                    table_data = table_data.split()
                    table_data[1] = str(Cmd)
                    table_data_str = '\n' + str(table_data[0]) + ' ' + str(table_data[1])
                    table_data_str += '\n' + str(table_data[2]) + ' ' + str(table_data[3]) + '\n'
                    table.find('tableData').text = table_data_str

        if ax.attrib['name'] == 'ROLL':
            for f in ax.iter('function'):
                if f.attrib['name'] == 'aero/moment/Roll_aileron':
                    product = f.find('product')
                    table = product.find('table')
                    table_data = table.find('tableData').text
                    table_data = table_data.split()
                    table_data[1] = str(Cld)
                    table_data_str = '\n' + str(table_data[0]) + ' ' + str(table_data[1])
                    table_data_str += '\n' + str(table_data[2]) + ' ' + str(table_data[3]) + '\n'
                    table.find('tableData').text = table_data_str

        if ax.attrib['name'] == 'YAW':
            for f in ax.iter('function'):
                if f.attrib['name'] == 'aero/moment/Yaw_rudder':
                    product = f.find('product')
                    value = product.find('value')
                    value.text = str(-Cnd)

    # making a 'pretty' xml file (comments are excluded)
    xml_string = et.tostring(root)
    xml_dom = minidom.parseString(xml_string)
    xml_string = '\n'.join([line for line in xml_dom.toprettyxml().split('\n') if line.strip()])

    with open(jsbsim_config_path, 'w') as my_xml:
        my_xml.writelines(xml_string)

    return None



# avl_output_path = 'avl_gen_files/stab.txt'
# jsbsim_config_path = 'aircraft/c172/c172.xml'
#
# integrate_avl_coef(avl_output_path, jsbsim_config_path)
