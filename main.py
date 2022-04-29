import argparse
from pathlib import Path
import shutil

parser = argparse.ArgumentParser(description='sorting  files')
parser.add_argument('--source', '-s', required=True, help='Source folder')
args = vars(parser.parse_args())

source = args.get('source')

# file formats
images = ['JPEG', 'PNG', 'JPG', 'SVG']
video = ['AVI', 'MP4', 'MOV', 'MKV']
documents = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']
music = ['MP3', 'OGG', 'WAV', 'AMR']
archive = ['ZIP', 'GZ', 'TAR']

legend = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'yo',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'y',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'h',
    'ц': 'ts',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'shch',
    'ъ': 'y',
    'ы': 'y',
    'ь': "'",
    'э': 'e',
    'ю': 'yu',
    'я': 'ya',

    'А': 'A',
    'Б': 'B',
    'В': 'V',
    'Г': 'G',
    'Д': 'D',
    'Е': 'E',
    'Ё': 'Yo',
    'Ж': 'Zh',
    'З': 'Z',
    'И': 'I',
    'Й': 'Y',
    'К': 'K',
    'Л': 'L',
    'М': 'M',
    'Н': 'N',
    'О': 'O',
    'П': 'P',
    'Р': 'R',
    'С': 'S',
    'Т': 'T',
    'У': 'U',
    'Ф': 'F',
    'Х': 'H',
    'Ц': 'Ts',
    'Ч': 'Ch',
    'Ш': 'Sh',
    'Щ': 'Shch',
    'Ъ': 'Y',
    'Ы': 'Y',
    'Ь': "'",
    'Э': 'E',
    'Ю': 'Yu',
    'Я': 'Ya',
}


def normalize(_str):
    latin_string = _str
    tbl = latin_string.maketrans(legend)
    latin_string = latin_string.translate(tbl)

    for _ in latin_string:
        if _ in "!@#$%^&*()=+-?|[]{}\/":
            latin_string = latin_string.replace(_, "_")
    return latin_string


def move_file(file: Path) -> None:
    ext = file.suffix
    category = categorization(str(ext).upper().replace(".", ""))

    if category == 'other':
        return
    if str(ext).replace(".", "").upper() in archive:
        shutil.unpack_archive(file, Path(source + '/archive/' + file.stem))
        file.unlink()
    else:
        new_path = Path(source + '/' + category)
        new_path.mkdir(exist_ok=True, parents=True)
        latin_filename = normalize(file.name)
        shutil.move(file, new_path / latin_filename)


def categorization(file_type):
    if file_type in images:
        return "images"
    elif file_type in video:
        return "video"
    elif file_type in documents:
        return "documents"
    elif file_type in music:
        return "music"
    elif file_type in archive:
        return "archive"
    else:
        return "other"


def read_folder(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            if str(el.name).lower() in ['images', 'video', 'documents', 'music', 'archive']:
                continue
            else:
                read_folder(el)
        else:
            move_file(el)


def del_empty_folder(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            if not bool(sorted(el.rglob('*'))):
                el.rmdir()
            del_empty_folder(el)


def main():
    read_folder(Path(source))
    del_empty_folder(Path(source))


if __name__ == "__main__":
    main()
