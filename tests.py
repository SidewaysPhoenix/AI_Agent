from functions.get_files_info import get_files_info
from functions.get_files_info import schema_get_files_info

print(get_files_info({'directory': '.'}))
print(get_files_info({'directory': 'pkg'}))