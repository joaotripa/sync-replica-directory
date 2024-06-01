import os
import hashlib

class Dispatcher:
    def __init__(self):
        self.directories_list = []

    def add_directory(self, directory):
        self.directories_list.append(directory)

    def synchronize_directories(self):
        return
    
    def _compare_directories(self):
        return
    
    def _compare_files(self):
        return
    
    
class Directory:
    def __init__(self, path):
        self.path = path
        self.files = os.listdir(path)
    
    def create_file(self,file):
        return
    
    def update_file(self,file):
        return
    
    def delete_file(self,file):
        return

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

    source_dir = Directory(source)
    replica_dir = Directory(replica)

    sync_dispatcher = Dispatcher()
    sync_dispatcher.add_directory(source_dir)
    sync_dispatcher.add_directory(replica_dir)