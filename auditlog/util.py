import ast


def update_schema(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    with open('./wrong_schema.txt', 'r', encoding='utf-8') as file:
        old_text = file.read().replace("\n\n", "\n    \n")

    with open('./correct_schema.txt', 'r', encoding='utf-8') as file:
        new_text = file.read()

    content = content.replace(old_text, new_text)
    content = content.replace(old_text.replace("    ", "  "), new_text)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def extract_values(file_path):
    result = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parsed_line = ast.literal_eval(line.strip())
            if isinstance(parsed_line, list) and len(parsed_line) >= 2:
                ts_key = parsed_line[0]
                cs_keys = []
                for key in parsed_line[1:]:
                    cs_keys.append(key)
                result.append((ts_key, cs_keys))

    return result