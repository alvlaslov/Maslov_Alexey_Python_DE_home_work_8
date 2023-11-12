from research_diretory_lib.tools import *


def main():
    tested_path = str(input('Input directory for research: '))
    result = dir_observe(tested_path)
    create_json(result, os.getcwd(), 'result')
    create_pickle(result, os.getcwd(), 'result')
    create_csv(result, os.getcwd(), 'result')


if __name__ == '__main__':
    main()