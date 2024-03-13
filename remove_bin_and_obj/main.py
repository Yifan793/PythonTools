import os
import shutil

def remove_file(path):
    aimedDir = ['obj', 'bin']

    c = 0
    for root, dirs, files in os.walk(path):
        for i in dirs:
            if i in aimedDir:
                dir = os.path.join(root, i)
                print(c, dir)
                shutil.rmtree(dir)
                c += 1
    input('删除完毕，请按回车键以退出。')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    remove_file('D:\workspace\\forguncy2\\forguncy')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
