import re
from app import generate_lyricle
from utils import TypeScriptSeralizer


def strip_whitespace(lst):
    res = []
    for r in lst:
        res.append(r.strip())
    return res


def extract():
    with open("validGuesses.ts") as fp:
        file_data = fp.read()
    results = re.findall("song: (.*),", file_data)
    results = [res.strip("'") for res in results]
    results = [strip_whitespace(res.split("─")) for res in results]

    return results


def main():
    results = extract()
    to_file = []
    for track in results:
        artist = track[0]
        song = track[1]
        try:
            json_response = generate_lyricle(song, artist)
        except:
            continue
        to_file.append(json_response)
    ts_string = TypeScriptSeralizer.decorate(to_file)
    with open("output.ts", "w", encoding="latin-1") as fp:
        fp.write(ts_string)


if __name__ == "__main__":
    main()
