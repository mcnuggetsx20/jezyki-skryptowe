from subprocess import run
from sys import argv
from os import getenv, listdir, path, makedirs
from datetime import datetime
from json import JSONDecodeError, dump, load as json_load
import mimetypes

def log_to_json(history_folder, og_path, output_format, output_path, program):

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
        "used program": program
    })

    with open(destination, "w") as json_file:
        dump(info, json_file, indent=4)

    print(f'Log dumped to {destination}')

if __name__ == '__main__' and len(argv) >= 2:
    # Getting all files from directory
    folder = argv[1]
    files = [path.join(folder, file) for file in listdir(folder)]
    # Getting types of files from arguments
    target_format_for_audio = next((f.split('=')[-1] for f in argv if f.startswith('--audio')), (print('Using mp4') or 'mp4'))
    target_format_for_image = next((f.split('=')[-1] for f in argv if f.startswith('--image')), (print('Using png') or 'png'))
    # Making output folder
    output_folder = getenv("CONVERTED_DIR", 'converted')
    makedirs(output_folder, exist_ok=True)

    for filename in files:
        used_program = ''
        # Creating new file name
        filename_short = filename.split('/')[-1]
        new_filename = filename_short.split('.')[0]
        new_filename =  f'{datetime.now().strftime("%Y%m%d")}-{new_filename}'
        # Checking file type
        mimestart = mimetypes.guess_type(filename_short)[0]
        if mimestart != None:
            mimestart = mimestart.split('/')[0]
        else:
            print(f"Ignorowanie ścieżki: {filename}")
            continue
        # Using ffmpeg for audio and video
        if mimestart in ['audio','video']:
            new_filename = path.join(output_folder, new_filename+f'.{target_format_for_audio}')

            result = run(
                ['ffmpeg', '-y', '-i', filename, new_filename], 
                capture_output=True,
                text=True,
            )
            used_program = 'ffmpeg'
            target_format = target_format_for_audio
        # Using imagemagick for 
        elif mimestart == 'image':
            new_filename = path.join(output_folder, new_filename+f'.{target_format_for_image}')

            result = run([
                "convert",  filename, new_filename ],
                  capture_output=True, text=True)
            used_program = 'imagemagick'
            target_format = target_format_for_image
        else:
            print(f'Ścieżka nie jest audio: {filename}')
        # Making log
        if result.returncode == 0:
            log_to_json(
                    history_folder = output_folder, 
                    og_path = filename, 
                    output_format = target_format, 
                    output_path = new_filename,
                    program = used_program
            )
        else:
            print(f'Conversion failed for: {filename}')


