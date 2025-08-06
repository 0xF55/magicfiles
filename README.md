# Magicfiles


`Magicfiles` is a powerfull python module to handle files using two main calsses:

- `FileObj` class to handle one file and allows you to make operations like:
1. read,write,size,readlines,strippedlines,remove
2. copy_to,move_to,write_json,read_json,renameto,...

---

- `FileGroup` class to handle a group of files and allow you to make:
* filter_by_size,filter_by_ext,read_all,write_all,remove_all
* filter_non_empty,filter_exists,total_size,...

---

- the module depends on the os, shutil, json modules... but it provides simplicity for handling files.


# Features

- Speed up file operations
- Simple human syntax
- Json Handling
- Continuous updates to the module

# FileObj

```python
file = FileObj("data.txt")
```

- We can do this methods :

`exist()` - Check if file exists

`get_parent_dir()` - Get file directory path

`get_extension()` - Get file extension

`is_empty()` - Check if file is empty

`content()` - Read file content

`write()` - Write data to file

`lines()` - Read lines

`stripped_lines()` - Read stripped lines

`create()` - Create the file if not exist

`move_to()` - Move file to another directory

`copy_to()` - Copy file to another directory

`read_json()` - Read json data -> dict

`write_json()` - Write json data

`renameto()` - Rename the file

`self_remove()` - Remove the file

`size()` - Get file size

`created_at()` - Return creation date

`modified_at()` - Return modification date


---

# FileGroup

```python
fg = FileGroup("file1.txt","file2.txt","file3.txt")
```

- We can do this methods :

`files()` - Return list of `FileObj` instances

`filter_non_empty()` - Return list of non empty files 

`filter_by_ext()` - Filter files by extension (Returns list)

`total_size()` - Return sum of files sizes in bytes

`filter_exists()` - Return list of exist files

`read_all()` - Read all files (Returns dict)

`write_all()` - Write to all files

`remove_all()` - Remove all files

`create_all()` - Create all files (if not exist)

`move_all_to()` - Move all files to directory

`filter_by_size()` - Filter files by size (min and max or equal)

- Install

[![PyPI Downloads](https://static.pepy.tech/badge/magicfiles)](https://pepy.tech/projects/magicfiles)

```python
pip install magicfiles
```

- Example

```python
f1 = FileObj("data.txt")
f1.create()
f1.write("Hello World")
f1.rename("data_tmp.txt")
print(f1.size())
# you can use many functions .....
f1.remove()

fg = FileGroup("test1.txt","test2.txt","test3.txt")
fg.create_all()
fg.write_all("Hello World")

data: dict = fg.read_all()
print(data["test1.txt"]) # file1 content
# you can use many functions .....
fg.remove_all()
```
