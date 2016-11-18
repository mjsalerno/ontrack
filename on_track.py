import argparse
import glob
import json
import os
import sys
import mutagen


def main():
    parser = argparse.ArgumentParser(description='Generate info JSON for the on_track program.')

    parser.add_argument('--quiet', '-q', help='Only print out errors.', required=False, dest='q', action='store_true')
    parser.add_argument('--recursive', '-r', help='Go through all sub folders.', required=False, dest='recur', action='store_true')
    parser.add_argument('--extension', '-ex', help='Specify the file extensions of the music files.', type=str, required=False, dest='ex',
                            metavar='<extension>', default='flac')
    args = parser.parse_args()

    if not args.recur:
        fix_tracks(args.q, args.ex)
    else:
        start = os.getcwd()
        for root, dirs, files in os.walk('.'):
            if root == '.':
                continue
            print('chdir: ' + root)
            os.chdir(root)
            fix_tracks(args.q, args.ex)
            os.chdir(start)


def fix_tracks(q, ex):
    info = None
    files = glob.glob('*.json')
    if len(files) != 1:
        print('Please have 1 json file in each folder: ' + os.getcwd())
        sys.exit(1)

    with open(files[0]) as data_file:
        info = json.load(data_file)

    files = glob.glob('*.' + ex)
    if len(files) != len(info['tracks']):
        print('the number of tracks given in the json is different than the number of files.')
        print('files: ' + str(len(files)) + ' tracks: ' + str(len(info['tracks'])))
        print('dir: ' + os.getcwd())
        sys.exit(1)

    for f in files:
        num = int(f.split()[0]) - 1
        new_name = str(num+1).zfill(2) + ' ' + info['tracks'][num] + '.' + ex
        new_name = new_name.replace('/', '_')
        new_name = new_name.replace('\\', '_')
        if not q:
            print('fixing: ' + f)
            print('     album:       ' + info['album'])
            print('     artist:      ' + info['artist'])
            print('     disc:        ' + str(info['disc']))
            print('     total discs: ' + str(info['disc_total']))
            print('     comment:     ' + str(info['comment']))
            print('     title:       ' + str(info['tracks'][num]))
            print('     rename:      ' + new_name + '\n')

        audio = mutagen.File(f)

        audio['album'] = info['album']
        audio['artist'] = info['artist']
        audio['discnumber'] = str(info['disc'])
        audio['disctotal'] = str(info['disc_total'])
        audio['comment'] = info['comment']
        audio['title'] = info['tracks'][num]
        audio.save()

        os.rename(f, new_name)


if __name__ == "__main__":
    main()
