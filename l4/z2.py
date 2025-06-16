import os
import sys

def list_path_directories():
    path_dirs = os.environ.get("PATH", "").split(os.pathsep)
    for directory in path_dirs:
        print(directory)

def list_executables():
    path_dirs = os.environ.get("PATH", "").split(os.pathsep)
    for directory in path_dirs:
        if os.path.isdir(directory):
            print(f"{directory}:")
            try:
                files = os.listdir(directory)
                executables = [f for f in files if os.path.isfile(os.path.join(directory, f)) and os.access(os.path.join(directory, f), os.X_OK)]
                for exe in executables:
                    print(f"\t{exe}")
            except:
                continue
            print()


if __name__ == "__main__":
    args = sys.argv[1:]
    
    if "--directories" in args:
        list_path_directories()
    if "--executables" in args:
        list_executables()
