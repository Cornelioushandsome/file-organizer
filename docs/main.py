import os
import argparse
import sys
from pathlib import Path
import shutil
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
        name, ext = os.path.splitext(file)
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
    if not filePath.exists():
        raise NameError("FolderPath does not exist")
    if not filePath.is_file():
        raise NameError("FolderPath is not a directory")
    
    try:
        filePath.unlink()
        print(f"Successfully deleted: {filePath}")
        return
    except Exception as e:
        print(f"Failed to delete file: {e}")
        return

def deleteFolder(folderPath: Path):
    if not folderPath.exists():
        raise NameError("FolderPath does not exist")
    if not folderPath.is_dir():
        raise NameError("FolderPath is not a directory")
    
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
    
def main():
    pass
        
    
if __name__ == "__main__":
    main()
