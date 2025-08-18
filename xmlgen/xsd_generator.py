from lxml import etree
from .xml_parser import load_xml
from .schema_inferer import infer_type
from collections import Counter


class XSDGenerator:
    def __init__(self):
        self.ns_map = {"xs": "http://www.w3.org/2001/XMLSchema"}
        self.xsd = None
        self.processed_elements = set()  # Track processed elements
        self.repeated_elements = set()  # Track elements that occur multiple times
        self.typestrict = False  # Flag to control type inference

    def generate_xsd(self, xml_path):
        """
        Generates an XSD schema for the given XML file.

        Parameters:
        - xml_path (str): Path to the XML file.
        """
        xml_tree = load_xml(xml_path)
        if xml_tree is not None:
            # Detect repeated elements
            self.repeated_elements = self.find_repeated_elements(xml_tree.getroot())

            self.xsd = etree.Element("{http://www.w3.org/2001/XMLSchema}schema", nsmap=self.ns_map)
            self.process_element(xml_tree.getroot(), self.xsd, is_root=True)
            return etree.tostring(self.xsd, pretty_print=True).decode()
        else:
            return "Failed to generate XSD schema."

    def find_repeated_elements(self, root):
        """
        Identifies elements that occur multiple times under the same parent in the XML structure.

        Parameters:
        - root (etree.Element): The root element of the XML tree.

        Returns:
        - set: A set of element names that occur multiple times under the same parent.
        """
        repeated_elements = set()
        self._count_elements(root, repeated_elements)
        return repeated_elements

    def _count_elements(self, element, repeated_elements):
        """
        Recursively counts occurrences of each element under the same parent in the XML tree.

        Parameters:
        - element (etree.Element): The current XML element.
        - repeated_elements (set): A set to track elements that occur multiple times under the same parent.
        """
        child_names = [child.tag.split('}')[-1] for child in element]
        for name, count in Counter(child_names).items():
            if count > 1:
                repeated_elements.add(name)
        for child in element:
            self._count_elements(child, repeated_elements)

    def process_element(self, element, parent, min_occurs="0", is_root=False):
        """
        Recursively processes an XML element to generate its XSD representation.

        Parameters:
        - element (etree.Element): The current XML element.
        - parent (etree.Element): The parent element in the XSD schema.
        - min_occurs (str): The minOccurs value for the element.
        - is_root (bool): Whether the current element is the root element.
        """
        ns = "{http://www.w3.org/2001/XMLSchema}"
        element_name = element.tag.split('}')[-1]

        # Skip if the element is already processed
        if element_name in self.processed_elements:
            return
        self.processed_elements.add(element_name)

        # Determine maxOccurs logic based on repeated elements at the same level
        max_occurs = "unbounded" if element_name in self.repeated_elements else "1"

        # Create the element definition
        element_def = etree.SubElement(parent, f"{ns}element", name=element_name)
        if not is_root:
            element_def.set("minOccurs", min_occurs)
        if max_occurs != "1":
            element_def.set("maxOccurs", max_occurs)

        has_children = len(element) > 0
        has_attributes = len(element.attrib) > 0
        has_text = element.text and element.text.strip()

        if has_children or has_attributes:
            complex_type = etree.SubElement(element_def, f"{ns}complexType")
            if has_text:
                # Use simpleContent if the element has both text and attributes
                simple_content = etree.SubElement(complex_type, f"{ns}simpleContent")
                extension = etree.SubElement(simple_content, f"{ns}extension", base="xs:string")
                for attr_name, attr_value in element.attrib.items():
                    attr_type = infer_type(attr_value) if self.typestrict else "xs:string"
                    etree.SubElement(extension, f"{ns}attribute", name=attr_name, type=attr_type)
            else:
                # Use sequence for child elements
                sequence = etree.SubElement(complex_type, f"{ns}sequence")
                for child in element:
                    self.process_element(child, sequence, min_occurs)
                for attr_name, attr_value in element.attrib.items():
                    attr_type = infer_type(attr_value) if self.typestrict else "xs:string"
                    etree.SubElement(complex_type, f"{ns}attribute", name=attr_name, type=attr_type)
        elif has_text:
            # If the element only has text, set its type directly
            element_def.set("type", infer_type(element.text) if self.typestrict else "xs:string")


if __name__ == "__main__":
    generator = XSDGenerator()
    xml_path = "tests/xml_files/valid_basic.xml"  # Update this path to your XML file.
    xsd_schema = generator.generate_xsd(xml_path)
    if xsd_schema:
        # print("XSD Schema Generated Successfully:")
        print(xsd_schema)
    else:
        print("Failed to generate XSD schema.")
