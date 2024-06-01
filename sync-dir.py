import os

if __name__ == "__main__":

    source = input('Path to source directory: ')

    if not os.path.isdir(source):
        print('Source directory ' + source + ' does not exist.')
        exit()

    replica = input('Path to replica directory: ')
    
    if not os.path.isdir(replica):
        create_dir = input('Replica directory ' + source + ' does not exist. Do you want to create it? [Y/n] ')

        if create_dir.lower() == 'y' or create_dir.lower() == '':
            os.mkdir(replica)
        else:
            print('Can\'t synchronize directories without a replica directory.')
            exit()