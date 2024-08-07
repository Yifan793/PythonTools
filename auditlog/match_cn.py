import xml.etree.ElementTree as ET
import re


def extract_cs_data(file_path):
    cs_data = {}
    tree = ET.parse(file_path)
    root = tree.getroot()

    for data in root.findall('data'):
        name = data.get('name')
        value = data.find('value').text
        cs_data[name] = value

    return cs_data


def extract_ts_data(file_path):
    ts_data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    matches = re.findall(r"(\w+):\s*'([^']*)'", content)
    for key, value in matches:
        ts_data[key] = value

    return ts_data


def is_cs_audit_string(value):
    return value.find('AuditLog') != -1 or value.find('LogOperationDetail') != -1 or value.find('LogOperation') != -1 \
        or value.find('UserServiceOperation') != -1 or value.find('WebSecurityOperation') != -1 \
        or value.find('WindowsDomainOperation') != -1 or value.find('LogOperationModuleName') != -1


def match_values(cs_data, ts_data, extracted_elements, filter_data):
    value_to_keys_map_ts = {}
    value_to_keys_map_cs = {}

    for key, value in ts_data.items():
        if value not in value_to_keys_map_ts:
            value_to_keys_map_ts[value] = []
        value_to_keys_map_ts[value].append("RS." + key)

    for key, value in cs_data.items():
        if value not in value_to_keys_map_cs:
            value_to_keys_map_cs[value] = []
        value_to_keys_map_cs[value].append("Resources." + key)

    result = []
    result_more_than_two = []
    result_more_than_two_all = []
    for str_value, cs_keys in value_to_keys_map_cs.items():
        if str_value in value_to_keys_map_ts:
            ts_keys = value_to_keys_map_ts[str_value]
            all_keys = ts_keys + cs_keys
            if not filter_data:
                result.append(all_keys)
            else:
                filtered_cs_keys = [s for s in cs_keys if is_cs_audit_string(s)]
                # filtered_cs_keys = [s for s in cs_keys if is_cs_audit_string(s) or s in extracted_elements]
                audit_keys = ts_keys + filtered_cs_keys
                if len(filtered_cs_keys) > 0:
                    if len(audit_keys) == 2:
                        result.append(audit_keys)
                    else:
                        result_more_than_two.append([ts_keys[0]] + filtered_cs_keys)
                        result_more_than_two_all.append(audit_keys)

    if filter_data:
        output_audit_more_than_two_file = 'match_cn_audit_more_than_two.txt'
        with open(output_audit_more_than_two_file, 'w', encoding='utf-8') as f:
            for value in result_more_than_two:
                f.write(f"{value}\n")

        output_audit_more_than_two_all_file = 'match_cn_audit_more_than_two_all.txt'
        with open(output_audit_more_than_two_all_file, 'w', encoding='utf-8') as f:
            for value in result_more_than_two_all:
                f.write(f"{value}\n")

    return result


def match_cn(extracted_elements):
    cs_file_path = 'D:\\workspace\\forguncy2\\forguncy\\ForguncyResource\\Resources.zh-CN.resx'
    ts_file_path = 'D:\\workspace\\forguncy2\\forguncy-frontend\\AdminPortal\\src\\localization\\resources\\locale\\cn.ts'

    cs_data = extract_cs_data(cs_file_path)
    ts_data = extract_ts_data(ts_file_path)

    result_audit = match_values(cs_data, ts_data, extracted_elements, True)
    result_all = match_values(cs_data, ts_data, extracted_elements, False)

    output_audit_file = 'match_cn_audit.txt'
    with open(output_audit_file, 'w', encoding='utf-8') as f:
        for value in result_audit:
            f.write(f"{value}\n")

    output_all_file = 'match_cn_all.txt'
    with open(output_all_file, 'w', encoding='utf-8') as f:
        for value in result_all:
            f.write(f"{value}\n")
