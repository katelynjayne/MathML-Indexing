from xml.etree import ElementTree as ET

def clean_query(filename):
    try:
        tree = ET.parse(filename)
    except:
        return
    root = tree.getroot()

    parent_map = {c: p for p in root.iter() for c in p}
    annotations = root.findall('.//{http://www.w3.org/1998/Math/MathML}annotation')
    annotations.extend(root.findall('.//{http://www.w3.org/1998/Math/MathML}annotation-xml'))
    for annotation in annotations:
        parent = parent_map.get(annotation)
        parent.remove(annotation)

    ET.register_namespace("","http://www.w3.org/1998/Math/MathML")
    tree.write('cleaned_query.xml')
    with open("./cleaned_query.xml", 'r') as file:
        with open("./cleaner_query.xml", 'w') as out:
            lines = file.readlines()
            for line in lines:
                if not line.startswith("<html:") and not line.startswith("</html:"):
                    out.write(line)