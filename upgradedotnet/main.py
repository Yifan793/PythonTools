import os
import subprocess
import re


if __name__ == '__main__':
    target_extension = ".csproj"

    for root, dirs, files in os.walk('D:\\workspace\\forguncy2\\forguncyjp'):
        for file in files:
            # if file.endswith(target_extension):
            #     file_path = os.path.join(root, file)
            #     print(file_path)
            #
            #     command = f"upgrade-assistant upgrade \"{file_path}\" --operation Inplace --targetFramework net8.0 --non-interactive"
            #
            #     output_file = f"output_{file}.txt"
            #     with open(output_file, 'w', encoding='utf-8') as f:
            #         f.write(f"Output for {file}:\n")
            #
            #         process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
            #                                    cwd=root)
            #         output, error = process.communicate()
            #
            #         f.write(output.decode("utf-8", 'ignore'))
            #         f.write("\n")
            #         f.write(error.decode("utf-8", 'ignore'))
            #         f.write("\n\n")
            if file.endswith(".sln"):
                file_path = os.path.join(root, file)
                print(file_path)

    # # 遍历文件夹，查找包含"failed"字段的txt文件
    # files_with_failed = []
    # for file in os.listdir("./"):
    #     if file.endswith(".txt"):
    #         file_path = os.path.join("./", file)
    #         with open(file_path, 'r') as f:
    #             content = f.read()
    #             pattern = r'failed'
    #             matches = re.findall(pattern, content, re.IGNORECASE)
    #             if len(matches) > 1:
    #                 files_with_failed.append(file_path)
    #
    # for file in files_with_failed:
    #     print(file)
