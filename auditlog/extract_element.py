import re
import os


# 2
def extract_property_message(text):
    pattern = re.compile(r'new\s+PropertyMessage\(\s*([^,\s]+)\s*,\s*[^)]+\s*\)', re.MULTILINE)

    matches = pattern.findall(text)

    return matches


# 2
def extract_property_bool_message(text):
    pattern = re.compile(r'new\s+PropertyBoolMessage\(\s*([^,\s]+)\s*,\s*[^)]+\s*\)', re.MULTILINE)

    matches = pattern.findall(text)

    return matches


# 3
def extract_property_key_value_message(text):
    pattern = re.compile(r'new\s+PropertyKeyValueMessage\(\s*([^,\s]+)\s*,\s*[^,\s]+(?:\s*,\s*[^)]+)?\s*\)', re.MULTILINE)

    matches = pattern.findall(text)

    return matches


# 3
def extract_update_message(text):
    pattern = re.compile(r'new\s+UpdateMessage\(\s*([^,\s]+)\s*,\s*[^,\s]+(?:\s*,\s*[^)]+)?\s*\)', re.MULTILINE)

    matches = pattern.findall(text)

    return matches


# 4
def extract_update_key_value_message(text):
    pattern = re.compile(r'new\s+UpdateKeyValueMessage\(\s*([^,\s]+)\s*,\s*[^,\s]+(?:\s*,\s*[^,\s]+){2}\s*\)',
                         re.MULTILINE)

    # 查找所有匹配的元素1
    matches = pattern.findall(text)

    return matches


def extract_all():
    directory = 'D:\\workspace\\forguncy2\\forguncy\\Forguncy.UserService2'
    results = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.cs'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        results.extend(extract_property_message(content))
                        results.extend(extract_property_bool_message(content))
                        results.extend(extract_property_key_value_message(content))
                        results.extend(extract_update_message(content))
                        results.extend(extract_update_key_value_message(content))
                except Exception as e:
                    print(f"无法读取文件 {file_path}: {e}")

    return results
