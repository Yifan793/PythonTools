import re
import xml.etree.ElementTree as ET

from util import update_schema, extract_values


def extract_ts_data(file_path):
    ts_data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    matches = re.findall(r"(\w+):\s*'([^']*)'", content)
    for key, value in matches:
        ts_data[key] = value

    return ts_data


def update_xml(file_path, updates):
    tree = ET.parse(file_path)
    root = tree.getroot()

    for data in root.findall('data'):
        name = data.get('name')
        if name in updates:
            value_element = data.find('value')
            if value_element is not None:
                value_element.text = updates[name]

    tree.write(file_path, encoding='utf-8', xml_declaration=True)
    update_schema(file_path)


def modify():
    file_path = './match_cn_audit.txt'
    more_than_two_file_path = './match_manual.txt'
    ja_ts_path = 'D:\\workspace\\forguncy2\\forguncy-frontend\\AdminPortal\\src\\localization\\resources\\locale\\kr.ts'
    en_ts_path = 'D:\\workspace\\forguncy2\\forguncy-frontend\\AdminPortal\\src\\localization\\resources\\locale\\en.ts'
    cs_path = 'D:\\workspace\\forguncy2\\forguncy\\ForguncyResource\\Resources.ko-KR.resx'

    extracted_keys = extract_values(file_path)
    extracted_values_more_than_two = extract_values(more_than_two_file_path)
    ja_ts_data = extract_ts_data(ja_ts_path)
    en_ts_data = extract_ts_data(en_ts_path)

    updates = {}
    for item in extracted_keys:
        ts_key = item[0][3:]
        cs_key = item[1][0][10:]
        if ts_key in ja_ts_data and ja_ts_data[ts_key] != en_ts_data[ts_key]:
            updates[cs_key] = ja_ts_data[ts_key]

    for item in extracted_values_more_than_two:
        ts_key = item[0][3:]
        cs_keys = item[1]
        if ts_key in ja_ts_data and ja_ts_data[ts_key] != en_ts_data[ts_key]:
            for cs_key in cs_keys:
                updates[cs_key[10:]] = ja_ts_data[ts_key]

    update_xml(cs_path, updates)
