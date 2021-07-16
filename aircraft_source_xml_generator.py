from xml.etree.ElementTree import Element, SubElement, tostring, Comment
from xml.dom import minidom

tlar_list = [['approach_speed', 33.33, 'm/s']]

wing = ['wing',
        [['area', 16.17, 'm**2'],
         ['aspect_ratio', 7.48, ''],
         ['span', 11, 'm'],
         ['root_chord', 1.66, 'm'],
         ['tip_chord', 1.10, 'm'],
         ['sweep_25', 0, 'deg'],
         ['dihedral', 2, 'deg'],
         ['incidence', 0, 'deg']]
        ]
fuselage = ['fuselage',
            [['length', 8.28, 'm']]
            ]
horizontal_tail = ['horizontal_tail',
                   [['area', 3.83, 'm**2'],
                    ['arm', 5.27, 'm']]
                   ]
vertical_tail = ['vertical_tail',
                 [['area', 1.085, 'm**2'],
                  ['arm', 4.52, 'm']]
                 ]
propulsion_geometry = ['propulsion',
                 [['layout', 0, ''],
                  ['count', 1, '']]
                 ]
extra = ['extra',
                 [['flaps', 1, ''],
                  ['spoilers', 0, ''],
                  ['chute', 0, '']]
                 ]
geometry_list = [fuselage,
                 wing,
                 horizontal_tail,
                 vertical_tail,
                 propulsion_geometry,
                 extra]

mass_aircraft = ['aircraft',
                 [['MTOW', 1157, 'kg'],
                  ['OWE', 744, 'kg']]
                 ]
inertia = ['inertia',
        [['Ixx', 1285, 'kg m**2'],
         ['Iyy', 1825, 'kg m**2'],
         ['Izz', 2667, 'kg m**2']]
        ]
weight_list = [mass_aircraft,
               inertia]

engine = ['engine',
              [['type', 0, ''],
               ['power', 134, 'kW'],
               ['max_rpm', 2700, 'rpm']]
              ]
propeller = ['propeller',
             [['diameter', 2.03, 'm'],
              ['fixed_pitch', 1.0, '']]
             ]
propulsion_list = [engine,
                   propeller]

root = Element('FASTOAD_model')
data = SubElement(root, 'data')

landing_gear_list = [['retractable', 0.0, ''],
                ['type', 0, ''],
                ['taildragger', 0, '']]

tlar = SubElement(data, 'TLAR')
geometry = SubElement(data, 'geometry')
weight = SubElement(data, 'weight')
propulsion = SubElement(data, 'propulsion')
landing_gear = SubElement(data, 'landing_gear')

for child_elt in tlar_list:
    sub_child = SubElement(tlar, child_elt[0])
    sub_child.text = str(child_elt[1])
    sub_child.set('units', child_elt[2])

for child_elt in landing_gear_list:
    sub_child = SubElement(landing_gear, child_elt[0])
    sub_child.text = str(child_elt[1])
    sub_child.set('units', child_elt[2])

for geom_elt in geometry_list:
    child = SubElement(geometry, geom_elt[0])
    for child_elt in geom_elt[1]:
        sub_child = SubElement(child, child_elt[0])
        sub_child.text = str(child_elt[1])
        sub_child.set('units', child_elt[2])

for weight_elt in weight_list:
    child = SubElement(weight, weight_elt[0])
    for child_elt in weight_elt[1]:
        sub_child = SubElement(child, child_elt[0])
        sub_child.text = str(child_elt[1])
        sub_child.set('units', child_elt[2])

for propu_elt in propulsion_list:
    child = SubElement(propulsion, propu_elt[0])
    for child_elt in propu_elt[1]:
        sub_child = SubElement(child, child_elt[0])
        sub_child.text = str(child_elt[1])
        sub_child.set('units', child_elt[2])


xml_string = minidom.parseString(tostring(root)).toprettyxml()
print(xml_string)

with open('resources/data/aircraft.xml', 'w') as my_xml:
    my_xml.writelines(xml_string)
