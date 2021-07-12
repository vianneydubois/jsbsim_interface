import xml.etree.ElementTree as ET


XML_PATH = 'resources/data/aircraft.xml'

doc = ET.parse(XML_PATH)
root = doc.getroot()

geometry = root.find('data').find('geometry')

wing = geometry.find('wing')
lg = geometry.find('')

var = float(wing.find('sweep_25').text)

print(var)

