# a file to test interacting with xml files

from xml.dom import minidom


doc = minidom.Document()

root = doc.createElement('aircraft')
doc.appendChild(root)

geometry = doc.createElement('geometry')

wing = doc.createElement('wing')
geometry.appendChild(wing)

htail = doc.createElement('htail')
geometry.appendChild(htail)

root.appendChild(geometry)

propulsion = doc.createElement('propulsion')
doc.createElement('')
root.appendChild(propulsion)

xml_str = doc.toprettyxml(indent="  ")

print(xml_str)

