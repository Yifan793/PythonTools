import xml.etree.ElementTree as ET


from util import update_schema, extract_values


def update_xml(file_path, updates):
    tree = ET.parse(file_path)
    root = tree.getroot()

    for data in root.findall('data'):
        name = data.get('name')
        if name in updates:
            comment = data.find('comment')
            value = data.find('value')
            if comment is not None:
                if updates[name] not in comment.text:
                    comment.text = comment.text + updates[name]
            else:
                value.tail = value.tail + "  "
                new_comment = ET.Element('comment')
                new_comment.text = updates[name]
                new_comment.tail = '\n'
                data.append(new_comment)

    tree.write(file_path, encoding='utf-8', xml_declaration=True)
    update_schema(file_path)


def modify_resx():
    file_path = './match_cn_audit.txt'
    more_than_two_file_path = './match_manual.txt'
    cs_path = 'D:\\workspace\\forguncy2\\forguncy\\ForguncyResource\\Resources.ko-KR.resx'

    extracted_keys = extract_values(file_path)
    extracted_values_more_than_two = extract_values(more_than_two_file_path)

    updates = {}
    for item in extracted_keys:
        ts_key = item[0]
        cs_key = item[1][0][10:]
        updates[cs_key] = ts_key

    for item in extracted_values_more_than_two:
        ts_key = item[0]
        cs_keys = item[1]
        for cs_key in cs_keys:
            update_key = cs_key[10:]
            updates[update_key] = ts_key

    update_xml(cs_path, updates)
