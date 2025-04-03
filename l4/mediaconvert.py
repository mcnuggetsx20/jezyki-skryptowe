from subprocess import run
from sys import argv
from os import getenv, listdir, path, makedirs
from datetime import datetime
from json import JSONDecodeError, dump, load as json_load

def log_to_json(history_folder, og_path, output_format, output_path):

    destination = path.join(history_folder, 'history.json')
    try:
        with open(destination, 'r') as json_file:
            info = json_load(json_file)

    except(FileNotFoundError, JSONDecodeError):
        info = list()

    info.append({
        "time": str(datetime.now()),
        "original path": path.realpath(og_path),
        "output format": output_format,
        "output path": path.realpath(output_path),
    })

    with open(destination, "w") as json_file:
        dump(info, json_file, indent=4)

    print(f'Log dumped to {destination}')

if __name__ == '__main__' and len(argv) == 3:
    folder = argv[1]
    files = [path.join(folder, file) for file in listdir(folder)]
    target_format = argv[-1]

    output_folder = getenv("CONVERTED_DIR", 'converted')
    makedirs(output_folder, exist_ok=True)

    for filename in files:
        filename_short = filename.split('/')[-1]

        new_filename = filename_short.split('.')[0]
        new_filename += f'.{target_format}'
        new_filename =  f'{datetime.now().strftime("%Y%m%d")}-{new_filename}'

        new_filename = path.join(output_folder, new_filename)

        result = run(
            ['ffmpeg', '-y', '-i', filename, new_filename], 
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            log_to_json(
                    history_folder = output_folder, 
                    og_path = filename, 
                    output_format = target_format, 
                    output_path = new_filename,
            )
        else:
            print('Conversion failed!')


