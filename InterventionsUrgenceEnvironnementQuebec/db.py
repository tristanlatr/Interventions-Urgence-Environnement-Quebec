import os
import json
import time
import threading
import datetime
from shutil import copyfile

# Database default files
DEFAULT_DB_FILE='db.json'

# Unique key
UNIQUE="url"

# Writing into the database file is thread safe
write_lock = threading.Lock()

class JsonDataBase():
    '''Interface to JSON database file.'''

    def __init__(self, filepath=DEFAULT_DB_FILE):
        """
        Pass filepath='null' to ignore DB
        """
        self.filepath=filepath
        if self.filepath=='null':
            self.data=[]
        else:
            self.data=self._build_db(self.filepath)
            self.update_and_write_items(self.data)

    # Read database
    def _build_db(self, filepath):
        '''Load database and returns the list from JSON file'''
        data=[]
        if os.path.isfile(filepath):
            with open(filepath, 'r', encoding='utf-8') as data_fd:
                data=json.load(data_fd)
            print("Load database: %s"%filepath)
        else:
            print("The database file %s do not exist. It will be created."%(filepath))
        return data

    def update_and_write_items(self, items=None):
        '''Update the databse with newly found items and/or older items updated.  
        Keep same order add append new item at the bottom.  '''
        new_data = False

        if not items: return
        if self.filepath=='null': return
        
        for item in items:
            item=dict(item)
            new=True
            for r in self.data:
                if r[UNIQUE]==item[UNIQUE]:
                    self.data[self.data.index(r)].update(item)
                    new=False
                    new_data=True
                    break
            if new: 
                self.data.append(item)
                new_data=True
        
        # Write method thread safe
        while write_lock.locked():
            time.sleep(0.01)
        write_lock.acquire()
        with open(self.filepath,'w', encoding='utf-8') as data_fd:
            json.dump(self.data, data_fd, indent=4)
            write_lock.release()
        
        return new_data

    def search(self, term):
        '''
        Find the existing item in DB based on the a unique identifier
        Return a dict or None
        '''
        item = [r for r in self.data if term == r[UNIQUE] ]
        if len(item)>0: 
            return item[0]
        else: 
            return None
