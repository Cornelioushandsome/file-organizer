import os
import argparse
import sys
from pathlib import Path
import shutil
from datetime import datetime
#import colorama
class FileExtensions:
    videoExtensions = [
    ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".mpeg", ".mpg", ".3gp", ".m4v"
    ]
    imageExtensions = [
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp", ".ico", ".heic"
    ]
    audioExtensions = [
    ".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma", ".m4a", ".alac"
    ]
    documentExtensions = [
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".rtf", ".odt", ".ods", ".odp"
    ]   
    archiveExtensions = [
    ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"
    ]
    codeExtensions = [
    ".py", ".c", ".cpp", ".java", ".js", ".html", ".css", ".json", ".xml", ".sh", ".php", ".rb", ".go", ".rs"
    ]
    executableExtensions = [
    ".exe", ".bat", ".cmd", ".msi", ".app", ".deb"
    ]

def _checkFile(path: Path):
    if not path.exists():
        return False
    if not path.is_file():
        return False
    return True

def _checkFolder(path: Path):
    if not path.exists():
        print("Path does not exist")
        return False
    if not path.is_dir():
        print("Path is not a directory")
        return False
    return True

def getFileType(extension)->str:
    types = FileExtensions()
    if extension in types.archiveExtensions:
        return "archive"
    if extension in types.audioExtensions:
        return "audio"
    if extension in types.codeExtensions:
        return "code"
    if extension in types.documentExtensions:
        return "documents"
    if extension in types.executableExtensions:
        return "executables"
    if extension in types.imageExtensions:
        return "images"
    if extension in types.videoExtensions:
        return "videos"
    return "unknown"

def reorganize(fileList):
    for file in fileList:
        _, ext = os.path.splitext(file)
        fileType = getFileType(ext)
        if fileType =="unknown":
            print("Unknown file type; Skipping")
            continue

        folderPath = Path(fileType)
        sourcePath = Path(file)

        folderPath.mkdir(exist_ok=True)

        destination = folderPath / sourcePath

        shutil.move(str(sourcePath), str(destination))

        print(f"Moved: {file} to {destination}")

def deleteFile(filePath: Path):
    filePath = Path(filePath)
    if not _checkFile(filePath):
        raise NameError("Invalid filePath")
    
    try:
        filePath.unlink()
        print(f"Successfully deleted: {filePath}")
        return
    except Exception as e:
        print(f"Failed to delete file: {e}")
        return

def deleteFolder(folderPath: Path):
    folderPath = Path(folderPath)
    if not _checkFolder(folderPath):
        raise NameError("Invalid folder path")

    
    if folderPath.stat().st_size > 0:
        confirm = input(f"Folder: \"{folderPath}\" is not empty. Would you still like to delete anyway? [Y : N]")
        if confirm.lower != "y":
            print("canceled.")
            return  

    try:
        shutil.rmtree(folderPath)
        print(f"Successfully deleted: {folderPath}")
        return
    except Exception as e:
        print(f"Failed to delete file: {e}")
        return

def unorganize(folderPath: Path):
    folderPath = Path(folderPath)

    if not folderPath.is_dir():
        print("Folder Path is not a directory")
        return
    if not folderPath.exists():
        print("Folder Path does not exist")
        return
    
    for dirs, _, files in os.walk(folderPath, topdown=False): # folder path: Path  |   folders in path: list  |    files in the folder: list
        for file in files:
            file_path = Path(dirs) / file
            destination_path = folderPath / file
            
            if destination_path.exists():
                counter = 1
                new_destination = destination_path.with_stem(destination_path.stem + f"_{counter}")
                while new_destination.exists():
                    counter+=1
                    new_destination = destination_path.with_stem(destination_path.stem + f"_{counter}")
                destination_path = new_destination
            
            shutil.move(str(file_path), str(destination_path))
            print(f"Moved {file_path} to {destination_path} \n")

        if Path(dirs) != folderPath:
            try:
                os.rmdir(dirs)
                print(f"Removed directory: {dirs}")
            except Exception as e:
                print(f"Error removing subdirectory: {dirs} | Error: {e}")
                return

def rename(path: Path, newName: str):
    path = Path(path)

    if not path.exists():
        print(f"Path: {path} doesn't exist or was already renamed.")
        return
    
    old_path = path
    new_path = path.with_name((newName + path.suffix) if path.is_file() else newName)
    if new_path.exists():
        print("Path already exists")
        return
    try:
        path.rename(new_path)
        print(f"Successfully renamed {old_path} to {new_path}")
    except Exception as e:
        print(f"An error occured while renaming {old_path} | Error: {e}")
        return   

def backupFolder(folderPath: Path, root: Path=None):
    folderPath = Path(folderPath)
    if not _checkFolder(folderPath):
        raise NameError("Invalid folder path")  

    backupFolder = Path(root) if root else folderPath.parent/"backups"
    backupFolder.mkdir(exist_ok=True)

    time = datetime.now().strftime(r"%Y-%m-%d")
    backupPath = backupFolder / f"{backupFolder.name}_backup-{time}"
    try:
        shutil.copytree(folderPath, backupPath)
        print(f"Successfully backed up {folderPath} to {backupPath}")
        return
    except Exception as e:
        print(f"An error occured: {e}")
        return
    
def main():  #enter your code here
    pass

    
if __name__ == "__main__":
    os.chdir(r"")  #Enter directory here
    PATH = os.getcwd()
    main()
