from lxml import etree
from pathlib import Path


ns = {"mei":"http://www.music-encoding.org/ns/mei",
        "xml":"http://www.w3.org/XML/1998/namespace"}

XML_ID = "{http://www.w3.org/XML/1998/namespace}id"

def change_octave(filepath:Path, add_octave:int=1):

    # parse document
    tree = etree.parse(filepath, etree.XMLParser(recover=True))
    root = tree.getroot()

    # get all notes with @oct
    notes = root.xpath(".//mei:note[@oct]", namespaces=ns)

    for note in notes:
        # add add_octave to original value of @oct
        new_oct = int(note.get("oct")) + add_octave
        # check whether new oct value lies outside of SPN values, if so - skip
        if new_oct < 0 or new_oct > 9:
            print(f"New octave value for note with xml:id '{note.get(XML_ID, 'unspecified')}' would be outside of SPN values - skipped.")
            continue
        note.set("oct", str(new_oct))

    # Write back, preserving XML declaration and processing instructions
    with open(filepath, "wb") as f:
        tree.write(f, encoding="UTF-8", pretty_print=True, xml_declaration=True)
