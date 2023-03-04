from pathlib import Path
import time
import pathlib
import shutil
import fnmatch
import sys

folder_extension = {'Images': ['.jpeg', '.png', '.jpg', '.svg', '.bmp'],
                    'Video': ['.avi', '.mp4', '.mov', '.mkv'],
                    'Documents': ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
                    'Audio': ['.mp3', '.ogg', '.wav', '.amr'],
                    'Archives': ['.zip', '.gz', '.tar', '.rar'],
                    'Other': None}

lst_extension = ['.jpeg', '.png', '.jpg', '.svg', '.bmp', '.avi', '.mp4', '.mov', '.mkv',
                    '.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx', '.mp3', '.ogg', '.wav', '.amr',
                    '.zip', '.gz', '.tar', '.rar']

exception_lst = []
images_count = 0
video_count = 0
documents_count = 0
audio_count = 0
archives_count = 0
other_files_count = 0

def greate_sort_folder(path: Path, folder_name: str):
    '''Create folders for sorted files, if the names are occupied - rename the existing ones and greate new'''

    try:
        path.joinpath(folder_name).mkdir()
                
    except FileExistsError:
        images = Path(str(path) + '\\' + folder_name)
        target = str(path) + '\\Old_' + folder_name + '_' + time.strftime('%Y%m%d%H%M%S')
        images.rename(target)
        
        greate_sort_folder(path, folder_name)

def exception_search(path: Path, target_path: Path) -> bool:
    
    for name in exception_lst:
        if fnmatch.fnmatch(str(target_path), str(path / name) + '**/*') or \
            fnmatch.fnmatch(str(target_path), str(path / name)):
            return True
        
    return False

def sort_process(path: Path, path_target: Path, name_file: str, extension: str) -> str:
    '''sort by extension into folders.
        Return the new file StrPath'''
    for folder, folder_key in folder_extension.items():
        if extension in folder_key:
            
            if folder == 'Archives':
                target = str(path) + '\\Archives\\' + pathlib.PurePath(Path(str(path) + '\\Archives\\' + name_file)).stem
                shutil.unpack_archive(str(path_target), target)
                path_target.unlink()
                count_files(folder)
                return(target)                
            
            target = str(path) + '\\' + folder + '\\' + name_file
            path_target.replace(target)
            count_files(folder)
            return(target)
    
    else:
        target = str(path) + '\\Other\\' + name_file
        path_target.replace(target)
        count_files('Other')
        return(target)
    
def normalize(name: str, count: int) -> str:
    ''' replace with '_' all characters except Latin and numbers.
        also add the files count and time'''
    new_name = ''
    for chr in name:
        if len(new_name) > 15:
            break
        if 65 <= ord(chr) <= 90 or 97 <= ord(chr) <= 122 or 48 <= ord(chr) <= 57:
            new_name += chr
        else:
            new_name += '_'   
    new_name += '_' + str(count) + '_' + time.strftime('%Y_%m_%d_%H_%M_%S')
             
    return new_name

def count_files(type_file: str):
    '''count files by type'''

    if type_file == 'Images':
        global images_count
        images_count += 1
    if type_file == 'Video':
        global video_count
        video_count += 1
    if type_file == 'Documents':
        global documents_count
        documents_count += 1
    if type_file == 'Audio':
        global audio_count
        audio_count += 1
    if type_file == 'Archives':
        global archives_count
        archives_count += 1
    if type_file == 'Other':
        global other_files_count
        other_files_count += 1

def main():
    
    path = Path(sys.argv[1]) 
    result = 'result.txt' 
    count_files = 0
    folders_lst = []
    changing_files = ''
    changing_folders = ''

    for folder_name in folder_extension:
        greate_sort_folder(path, folder_name)
        exception_lst.append(folder_name)
        exception_lst.append(result)
    
    for item in path.glob('**/*'):
        
        if exception_search(path, item):
            continue
        
        if item.is_dir():
            folders_lst.append(item)
            
        if item.is_file():
            extension = pathlib.PurePath(item).suffix
            name = normalize(pathlib.PurePath(item).stem, count_files) + extension
            count_files += 1
            p = sort_process(path, item, name, extension)
            changing_files += '  ' + str(item) + ' --->    ' + p + '\n'
                    
    for folder in reversed(folders_lst):
        folder.rmdir()
        changing_folders += '  ' + str(folder) + '---> deleted\n'


    with open(path / result, 'w') as fb:
        fb.write(f'Sort result:\n\nFound folders:\n{changing_folders}\nFound files {count_files}:\n\
Images = {images_count}\nVideo = {video_count}\nDocuments = {documents_count}\n\
Audio = {audio_count}\nArchives = {archives_count}\nOther = {other_files_count}\n\n\
Remove to:\n{changing_files}') 


if __name__ == "__main__":
    main()