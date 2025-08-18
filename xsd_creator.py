import os
from lxml import etree
from xmlgen import XSDGenerator


def create_xsd_from_xml(file, typestrict=False):
    """
    Create an XSD schema from an XML file.

    Parameters:
    - file (str): The path to the XML file to be converted to XSD.
    - typestrict (bool): If True, the generator will be strict about types. Default is False.
    """
    generator = XSDGenerator()
    generator.typestrict = typestrict
    xsd_schema = generator.generate_xsd(file)
    return xsd_schema


def validate_xml_against_xsd(xmlfile, xsdfile) -> bool:
    with open(xmlfile, 'rb') as file:
        xml = file.read()

    with open(xsdfile, 'rb') as xsd_file:
        xsd_doc = etree.parse(xsd_file)
        xsd = etree.XMLSchema(xsd_doc)

    xml_doc = etree.fromstring(xml)
    result = xsd.validate(xml_doc)
    if not result:
        print(f"Validation failed for {xmlfile}:")
        print(xsd.error_log)  # Optional: Log der Validierungsfehler ausgeben
    return result


def list_xml_files(directory):
    """
    List all XML files in a given directory.

    Parameters:
    - directory (str): The path to the directory to search for XML files.

    Returns:
    - list: A list of XML file paths.
    """
    try:
        files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.xml')]
        return files
    except NotADirectoryError:
        print(f"Directory not found: {directory}")
        return []


def check_file_exists(file_path):
    """
    Check if a file exists.

    Parameters:
    - file_path (str): The path to the file to check.

    Returns:
    - bool: True if the file exists, False otherwise.
    """
    return os.path.isfile(file_path)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="XSD Creator and Validator",
        epilog=(
            "Examples:\n"
            "  python xsd_creator.py -c -f xml_files/importfeed.xml\n"
            "  python xsd_creator.py -v -f xml_files/importfeed.xml\n"
            "  python xsd_creator.py -v -l xml_files\n"
            "  python xsd_creator.py -c -l xml_files\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter  # Preserve formatting for examples
    )
    parser.add_argument('-c', '--create', action='store_true', help='Create an XSD schema from the specified XML file or all XML files in a folder.')
    parser.add_argument('-v', '--validate', action='store_true', help='Validate the specified XML file or all XML files in a folder against their corresponding XSD schemas.')
    parser.add_argument('-f', '--file', type=str, help='Path to a specific XML file to process')
    parser.add_argument('-l', '--list', type=str, help='Process all XML files in the specified folder.')
    parser.add_argument('-t', '--typestrict', action='store_true', help='Enable strict type checking when creating XSD schemas.')
    args = parser.parse_args()

    # Ensure either --create or --validate is specified
    if not args.create and not args.validate:
        parser.error("You must specify at least one action: --create or --validate.")

    # Ensure either --file or --list is specified
    if not args.file and not args.list:
        parser.error("You must specify a target: --file or --list.")

    typestrict = args.typestrict
    xml_file = args.file
    xml_list = args.list
    create = args.create
    validate = args.validate

    PATH_FOR_XSD = "xsd_files"
    os.makedirs(PATH_FOR_XSD, exist_ok=True)

    try:
        if xml_list:
            files = list_xml_files(xml_list)
            print(f"Start processing {len(files)} XML files...")
            print("-" * 40)
            for f in files:
                if not check_file_exists(f):
                    print(f"File not found: {f}")
                    continue
                if create:
                    print(f"Creating XSD for {f}...")
                    xsd_schema = create_xsd_from_xml(f, typestrict)
                    xsd_file = os.path.join(PATH_FOR_XSD, os.path.basename(f).replace(".xml", "-scheme.xsd"))
                    with open(xsd_file, "w") as xsd_f:
                        xsd_f.write(xsd_schema)
                    print(f"XSD created: {xsd_file}")

                if validate:
                    print(f"Validating {f} against its XSD...")
                    xsd_file = os.path.join(PATH_FOR_XSD, os.path.basename(f).replace(".xml", "-scheme.xsd"))
                    if not check_file_exists(xsd_file):
                        print(f"XSD file not found: {xsd_file}")
                        continue
                    res = validate_xml_against_xsd(f, xsd_file)
                    print(f"Validation result for {f}: {res}")
                print("-" * 40)
        if xml_file:
            file = xml_file
            if not check_file_exists(file):
                print(f"File not found: {file}")
                exit(1)
            if create:
                print(f"Creating XSD for {file}...")
                xsd_schema = create_xsd_from_xml(file, typestrict)
                xsd_file = os.path.join(PATH_FOR_XSD, os.path.basename(file).replace(".xml", "-scheme.xsd"))
                with open(xsd_file, "w") as xsd_f:
                    xsd_f.write(xsd_schema)
                print(f"XSD created: {xsd_file}")
            if validate:
                print(f"Validating {file} against its XSD...")
                xsd_file = os.path.join(PATH_FOR_XSD, os.path.basename(file).replace(".xml", "-scheme.xsd"))
                if not check_file_exists(xsd_file):
                    print(f"XSD file not found: {xsd_file}")
                    exit(1)
                res = validate_xml_against_xsd(file, xsd_file)
                print(f"Validation result for {file}: {res}")
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
