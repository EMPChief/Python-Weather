import xmltodict
import json
import re

"""
Converts an XML dictionary file containing word entries 
into a JSON file containing the entries.

Reads in the XML file, converts each entry into a JSON 
object, puts all entries in a JSON list, and writes the 
result to a JSON file.
"""


def convert_entry(entry):
    word_without_pattern = re.sub(r'#\w+#\d+', '', entry["@word"])

    return {
        "word": word_without_pattern,
        "status": entry["@status"],
        "gloss": entry["gloss"],
        "lf": entry["lf"]
    }


def convert_xml_to_json(xml_string):
    dict_data = xmltodict.parse(xml_string)
    entries = dict_data.get("wne", {}).get("entry", [])
    converted_entries = [convert_entry(entry) for entry in entries] if isinstance(
        entries, list) else [convert_entry(entries)]
    result_dict = {
        "entries": converted_entries
    }

    json_data = json.dumps(result_dict, indent=2)
    return json_data


def read_xml_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        xml_string = file.read()
    return xml_string


def save_json_file(json_data, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)


if __name__ == "__main__":
    xml_file_path = "wne-2006-12-06.xml"
    output_json_file_path = "dictionary.json"

    xml_string = read_xml_file(xml_file_path)
    json_data = convert_xml_to_json(xml_string)
    save_json_file(json_data, output_json_file_path)
