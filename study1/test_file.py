import os


def read_file(filename, file_path):
    file_name = os.path.join(file_path, filename)
    with open(file_name, 'rb') as f:
        for line in f:
            print(line.decode('utf-8'))


def write_file(filename, cont_list):
    with open(filename, 'wb') as f:
        for line in cont_list:
            f.write(line.encode('utf-8'))


if __name__ == '__main__':
    file_name = 'test.txt'
    file_path = '/Users/sjw/Documents/workspace/GitHub/agent_study/'
    # cont_list = ["hello", "world"]
    # write_file(os.path.join(file_path, file_name), cont_list)  # 传完整路径

    read_file(file_name, file_path)