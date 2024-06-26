import os
import hashlib
import time
import logging

logger = logging.getLogger(__name__)

class Dispatcher:
    def __init__(self, source):
        self.directories_list = []
        self.source_directory = source

    def add_directory(self, directory):
        self.directories_list.append(directory)

    def synchronize_directories(self, sync_interval):
        try:
            while True:
                self.source_directory.get_subdirectories_and_files()
                for directory in self.directories_list:
                    self._compare_directories(self.source_directory,directory)
                    self._compare_files(self.source_directory,directory)
                
                time.sleep(int(sync_interval))
        except KeyboardInterrupt:
            pass


    def _compare_directories(self, source, replica):
        for subdir in source.subdirectories:
            if subdir not in replica.subdirectories:
                logger.info('[CREATE] Created new subdirectory in replica: ' + subdir)
                replica.create_subdirectory(subdir)

        for subdir in replica.subdirectories:
            if subdir not in source.subdirectories:
                logger.info('[DELETE] Removed subdirectory in replica: ' + subdir)
                replica.remove_subdirectory(subdir)
    
    def _compare_files(self, source, replica):
        for file in source.files:
            if file not in replica.files:
                logger.info('[CREATE] Created new file in replica - ' + file)
                replica.create_or_update_file(os.path.join(source.path,file),file)

        for file in replica.files:
            if file not in source.files:
                logger.info('[DELETE] Removed file in replica - ' + file)
                replica.delete_file(file)
                continue
            
            if self._compare_files_hash(os.path.join(source.path,file),os.path.join(replica.path,file)):
                continue
            else:
                logger.info('[UPDATE] Updated file: ' + file)
                replica.create_or_update_file(os.path.join(source.path,file),file)
                
    def _compare_files_hash(self, source_file, file):
        with open(source_file, 'rb') as source_file_reader:
            with open(file, 'rb') as file_reader:
                if hashlib.md5(source_file_reader.read()).hexdigest() == hashlib.md5(file_reader.read()).hexdigest():
                    return True
                else: 
                    return False
    
    
class Directory:
    def __init__(self, path):
        self.path = path
        self.files = []
        self.subdirectories = []
        self.get_subdirectories_and_files()
    
    def create_or_update_file(self,source_file,file):
        os.system('cp '+ source_file + ' ' + os.path.join(self.path,file))
        if file not in self.files:
            self.files.append(file)
    
    def delete_file(self,file):
        if os.path.exists(os.path.join(self.path,file)):
            os.remove(os.path.join(self.path,file))
        self.files.remove(file)
    
    def create_subdirectory(self,subdirectory):
        os.mkdir(os.path.join(self.path,subdirectory))
        self.subdirectories.append(subdirectory)

    def remove_subdirectory(self,subdirectory):
        if os.path.exists(os.path.join(self.path,subdirectory)):
            os.system('rm -fr ' + os.path.join(self.path,subdirectory))
        self.subdirectories.remove(subdirectory)

    def get_subdirectories_and_files(self):
        subdirectories = []
        all_files = []

        for path, subdirs, files in os.walk(self.path):
            relative_path = os.path.relpath(path,self.path)
            for subdir in subdirs:
                subdirectories.append(os.path.join(relative_path, subdir))
            for name in files:
                all_files.append(os.path.join(relative_path, name))

        self.subdirectories = subdirectories
        self.files = all_files

def configure_logging(log_file):
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)

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

    sync_interval = input('Synchronization interval in seconds (eg. 300): ')

    if not sync_interval.isdigit():
        print('The synchronization interval you provided is not a digit.')
        exit()
    
    log_file = input('Log file path: ')
    if not os.path.isdir(os.path.dirname(log_file)):
        print('Directory of log file ' + log_file + ' does not exist.')
        exit()
    elif os.path.isdir(log_file):
        print('Log file path provided ' + log_file + ' is a directory.')
        exit()

    configure_logging(log_file)

    source_directory = Directory(source)
    replica_directory = Directory(replica)

    sync_dispatcher = Dispatcher(source_directory)
    sync_dispatcher.add_directory(replica_directory)

    sync_dispatcher.synchronize_directories(sync_interval)