import xml.etree.ElementTree as ET
import sys

tree = ET.parse(sys.argv[1])
root = tree.getroot()

print(root)
for child in root:
    print(child.attrib['name'] + '=' + 'Symbols(name=\'' + child.attrib['name'] + '\', symbol=\'' + child.attrib['symbol'] +'\')')
