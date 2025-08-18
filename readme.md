# XSD Creator and Validator

The **XSD Creator** is a Python-based tool designed to generate XSD schemas from XML files and validate XML files against their corresponding XSD schemas. It also includes a utility to download XML files from URLs specified in a CSV file.

---

## Features
- **Generate XSD Schemas**: Automatically create XSD schemas from XML files.
- **Validate XML Files**: Validate XML files against their corresponding XSD schemas.
- **Batch Processing**: Process multiple XML files in a folder.
- **Type Strictness**: Optionally enable strict type inference for XSD generation.
- **Download XML Files**: Download XML files from URLs specified in a CSV file.

---

## Requirements
To use the XSD Creator, ensure the following dependencies are installed:

1. **Python 3.7 or higher**
2. **Required Python Libraries**:
   - `lxml`
   - `requests`

Install the required libraries using pip:
```bash
pip install -r requirements.txt
```

---

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd xsd_creator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure the following folder structure exists:
   ```
   xsd_creator/
   ├── xmlgen/                # Contains the XSD generation logic
   │   ├── xsd_generator.py   # Core logic for generating XSD schemas
   │   ├── xml_parser.py      # XML parsing utilities
   │   ├── schema_inferer.py  # Type inference for XSD generation
   ├── xsd_creator.py         # Main script for creating and validating XSDs
   ├── urls.csv               # CSV file with URLs for XML downloads
   ├── download_xml.py        # Script to download XML files from URLs
   ├── xml_files/             # Folder to store XML files
   ├── xsd_files/             # Folder to store generated XSD files
   └── readme.me              # Documentation for the project
   ```

---

## Usage
The XSD Creator can be used via the command line. Below are the available options and examples.

### Command-Line Options
| Option         | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `-c, --create` | Create an XSD schema from the specified XML file or all XML files in a folder. |
| `-v, --validate` | Validate the specified XML file or all XML files in a folder against their corresponding XSD schemas. |
| `-f, --file`   | Path to a specific XML file to process.                                     |
| `-l, --list`   | Process all XML files in the specified folder.                              |
| `-t, --typestrict` | Enable strict type checking when creating XSD schemas.                  |

### Examples
1. **Generate an XSD schema for a single XML file**:
   ```bash
   python xsd_creator.py -c -f xml_files/importfeed.xml
   ```

2. **Validate a single XML file against its XSD schema**:
   ```bash
   python xsd_creator.py -v -f xml_files/importfeed.xml
   ```

3. **Generate XSD schemas for all XML files in a folder**:
   ```bash
   python xsd_creator.py -c -l xml_files
   ```

4. **Validate all XML files in a folder against their XSD schemas**:
   ```bash
   python xsd_creator.py -v -l xml_files
   ```

5. **Enable strict type checking during XSD generation**:
   ```bash
   python xsd_creator.py -c -f xml_files/importfeed.xml -t
   ```

---

## Download XML Files
Use the `download_xml.py` script to download XML files from URLs specified in `urls.csv`. The downloaded files will be saved in the `xml_files` folder.

### Example
Run the script:
```bash
python download_xml.py
```

---

## Error Handling
- If a file or folder is not found, an appropriate error message will be displayed.
- Validation errors will be logged in the console for debugging.

---

## License
This project is licensed under the MIT License. Feel free to use and modify it as needed.

---

## Contributions
Contributions are welcome! If you encounter any issues or have suggestions for improvement, feel free to open an issue or submit a pull request.