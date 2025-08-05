from os import path,remove,rename
from shutil import copy,move
from time import ctime
from json import loads,dump
from typing import List



def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("[!] File Not Found")
        except PermissionError:
            print("[!] Permission Error")
        except Exception as e:
            print(f"[!] An error occurred: {e}")
        return None
    
    return wrapper


class FileObj:
    """
    File Handling Object FileObj(file_names)
    """
    def __init__(self,file_name):
        self.file_name = file_name

    def exist(self) -> bool:
        """
        Check if file exists
        """
        return path.exists(self.file_name)
    
    def get_parent_dir(self) -> str:
        """
        Get the parent directory of the file.
        """
        return path.dirname(self.file_name)

    def get_extension(self) -> str:
        """
        Get the file extension.
        """
        return path.splitext(self.file_name)[1].strip(".")

    def is_empty(self) -> bool:
        return self.size() == 0

    @handle_exceptions
    def content(self) -> str:
        """
        Read File Content
        """
        with open(self.file_name,"r") as r:
            return r.read()

    @handle_exceptions
    def write(self,data,mode = "a") -> None:
        """
        Write Data to the file
        """
        with open(self.file_name,mode=mode) as w:
                w.write(data)

    @handle_exceptions
    def lines(self) -> List[str]:
        """
        Read Lines
        """
        with open(self.file_name,"r") as r:
            return r.readlines()

    @handle_exceptions
    def stripped_lines(self) -> List[str]:
        if self.file_name:
            strripped = [l.strip() for l in self.lines()]
            return strripped
        return []
    
    @handle_exceptions
    def create(self) -> bool:
        """
        Create File if not exist
        """
        if not self.exist():
            with open(self.file_name,"w"):
                pass
            return True
        return False
    
    @handle_exceptions
    def move_to(self,dst) -> None:
        """
        Move File To Dst
        """
        move(self.file_name,dst)

    @handle_exceptions
    def copy_to(self,dst) -> None:
        """
        Copy File To Dst
        """
        copy(self.file_name,dst)

    @handle_exceptions
    def read_json(self) -> dict:
        """
        Read File JSON Data
        """
        json_data = loads(self.content())
        return json_data

    @handle_exceptions
    def write_json(self,data: dict):
        """
        Write Json Data
        """
        with open(self.file_name,"w") as j:
            dump(data,j,indent=4)

    @handle_exceptions
    def renameto(self,dst: str) -> None:
        """
        Rename File
        """
        rename(self.file_name,dst)

    @handle_exceptions
    def self_remove(self) -> bool:
        """Remove/Delete File"""
        if self.exist():
            remove(self.file_name)
            return True
        return False
    
    @handle_exceptions
    def size(self) -> int:
        """
        Get File Size
        """
        return path.getsize(self.file_name)

    @handle_exceptions
    def created_at(self) -> str:
        """
        get Create date
        """
        return ctime(path.getctime(self.file_name))
    
    @handle_exceptions
    def modified_at(self) -> str:
        """
        get Modify date
        """
        return ctime(path.getmtime(self.file_name))

    def __eq__(self, other):
        try:
            return self.file_name == other.file_name
        except AttributeError:
            return False
        
    def __len__(self):
        try:
            return self.size() or 0
        except Exception:
            return 0

    def __str__(self):
        return "FileObj(%s)" % self.file_name
    
    def __repr__(self):
        return "<FileObj name='%s'>" % self.file_name

class FileGroup:
    def __init__(self,*files_names: str):
        self.files_names = files_names

    @property
    def files(self) -> List[FileObj]:
        """
        Return a list for FileObj instances for all provided files
        
        Each FileObj give you access to make operations like reading,writng....
        """
        file_objects = list([FileObj(f) for f in self.files_names])
        return file_objects
    
    def __getitem__(self, index: int):
        return FileObj(self.files_names[index])

    def __len__(self):
        return len(self.files_names)
    
    def __iter__(self):
        return iter(self.files)


    def filter_non_empty(self) -> List[FileObj]:
        """
        Return list for non empty files
        """
        not_empty = []
        if self.files_names:
            for f in self.files:
                if not f.is_empty():
                    not_empty.append(f)
            return not_empty
        return []
    
    def filter_by_ext(self,ext: str) -> List[FileObj]:
        """
        Filter files by extension (e.g, json)
        """
        ext = ext.strip(".") if ext.startswith(".") else ext
        exts = []
        if self.files_names:
            for f in self.files:
                if f.get_extension() == ext:
                    exts.append(f)
            return exts
        return []
    
    def total_size(self) -> int:
        """
        Get total files size
        """
        return sum(FileObj(f).size() or 0 for f in self.files_names)

    def filter_exists(self) -> List[FileObj]:
        """
        Filter by file exist
        """
        return [FileObj(f) for f in self.files_names if FileObj(f).exist()]

    def read_all(self) -> dict:
        """
        Return a dictionary with {file_name:file_content} to all files
        """
        return {f.file_name: f.content() for f in self.files}

    def write_all(self, data: str, append=True) -> None:
        """
        Write data to all files in the group
        """
        mode = "a" if append else "w"
        if self.files_names:
            for f in self.files:
                f.write(data,mode)

    def remove_all(self) -> None:
        """
        Remove all files
        """
        for f in self.files:
            f.self_remove()

    def create_all(self) -> None:
        """
        Create files that not exist
        """
        for f in self.files:
            f.create()

    def move_all_to(self,dst: str) -> None:
        """
        Move files to specifec folder
        """
        for f in self.files:
            f.move_to(dst)

    def filter_by_size(self,min: int = 0, max: int = 0,equal: int = 0):
        """
        Filter files by size (e.g, min=1024,max=4096) in Bytes
        """
        matches = []
        if self.files_names:
            if equal:
                for f in self.files:
                    if f.size() == equal:
                        matches.append(f)
            else:
                if not equal and max:
                    for f in self.files:
                        size = f.size()
                        if size and size >= min and size <= max :
                            matches.append(f)
            return matches
        
        return []