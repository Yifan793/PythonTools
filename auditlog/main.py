from extract_element import extract_all
from match_cn import match_cn
from modify_cs import modify
from modify_resx import modify_resx

if __name__ == '__main__':

    element_values = extract_all()
    output_file = 'extracted_elements.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        for value in element_values:
            f.write(f"{value}\n")

    match_cn(element_values)

    modify_resx()

    modify()
