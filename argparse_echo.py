import sys

if __name__ == '__main__':
    for i, arg in enumerate(sys.argv[1:]):
        print(f'{i}:\t{arg}')
