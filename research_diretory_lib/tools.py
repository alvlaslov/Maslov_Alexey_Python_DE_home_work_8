import json
import csv
import pickle
import os


def create_json(in_dct: dict, path: str, file_name: str) -> None:
    file_path = os.path.join(path, file_name + '.json')
    with open(file_path, 'w', encoding='utf-8') as f_out:
        json.dump(in_dct, f_out, indent=4)


def create_csv(in_dct: dict, path: str, file_name: str) -> None:
    file_path = os.path.join(path, file_name + '.csv')
    data = [['Path', 'Type', 'Name', 'Size', 'Parent_dir', ]]
    for key_, val_ in in_dct.items():
        data.append([key_, *val_.values()])
    with open(file_path, 'w', encoding='utf-8') as f_out:
        write_csv = csv.writer(f_out, dialect='excel', delimiter=';')
        write_csv.writerows(data)


def create_pickle(in_dct: dict, path: str, file_name: str) -> None:
    file_path = os.path.join(path, file_name + '.bin')
    with open(file_path, 'wb') as f_out:
        pickle.dump(in_dct, f_out)


def dct_formatter(total_dct: dict[str, dict[str]],
                  path: str,
                  item_name: str,
                  item_type: str) -> None:
    if item_type == 'file':
        total_dct[path] = dict(unit_type='File',
                               unit_name=item_name,
                               unit_size=os.path.getsize(os.path.join(path, item_name)),
                               parent_dir=os.path.split(path)[-1])
    elif item_type == 'dir':
        total_dct[path] = dict(unit_type='Directory',
                               unit_name=item_name,
                               unit_size=determine_size(os.path.join(path, item_name)),
                               parent_dir=os.path.split(os.path.abspath(path))[-1])


def determine_size(count_path: str,
                   dir_size: int = 0) -> float:
    for sub_item in os.walk(count_path):
        if sub_item[2]:
            dir_size += sum([os.path.getsize(os.path.join(sub_item[0], file))
                             for file in sub_item[2]])
        if sub_item[1]:
            dir_size += sum([determine_size(os.path.join(sub_item[0], subdir))
                             for subdir in sub_item[1]])
    return dir_size


def dir_observe(aim_path: str,
                total_dct: dict = None) -> dict[str, dict[str]]:
    if total_dct is None:
        total_dct = {}
        basic_path = os.path.split(os.path.abspath(aim_path))
        dct_formatter(total_dct,
                      os.path.join(*basic_path[:-1]),
                      basic_path[-1],
                      'dir')

    for item in os.listdir(aim_path):
        check_path = os.path.join(aim_path, item)
        if os.path.isfile(check_path):
            dct_formatter(total_dct, aim_path, item, 'file')
        elif os.path.isdir(check_path):
            dct_formatter(total_dct, aim_path, item, 'dir')
            dir_observe(os.path.join(aim_path, item), total_dct)
    return total_dct


if __name__ == '__main__':
    tested_path = str(input('Input directory for research: '))
    result = dir_observe(tested_path)
    create_json(result, os.getcwd(), 'result')
    create_pickle(result, os.getcwd(), 'result')
    create_csv(result, os.getcwd(), 'result')
