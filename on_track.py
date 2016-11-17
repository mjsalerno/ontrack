import glob
import json
import os
import sys
import mutagen

info = None
files = glob.glob('*.json')
if len(files) != 1:
    print('Please have 1 json file in each folder.')
    sys.exit(1)

with open(files[0]) as data_file:
    info = json.load(data_file)

files = glob.glob('*.flac')
if len(files) != len(info['tracks']):
    print('the number of tracks given in the json is different than the number of files.')
    print('files: ' + str(len(files)) + ' tracks: ' + str(len(info['tracks'])))
    sys.exit(1)

for f in files:
    num = int(f.split()[0]) - 1
    print('fixing: ' + f)
    print('     album:       ' + info['album'])
    print('     artist:      ' + info['artist'])
    print('     disc:        ' + str(info['disc']))
    print('     total discs: ' + str(info['disc_total']))
    print('     comment:     ' + str(info['comment']))
    print('     title:       ' + str(info['tracks'][num]) + '\n')

    audio = mutagen.File(f)
    for name in audio:
        pass
        #print name + ' : ' + str(audio[name])

    audio['album'] = info['album']
    audio['artist'] = info['artist']
    audio['discnumber'] = str(info['disc'])
    audio['disctotal'] = str(info['disc_total'])
    audio['comment'] = info['comment']
    audio['title'] = info['tracks'][num]
    audio.save()

    os.rename(f, str(num+1).zfill(2) + ' ' + info['tracks'][num] + '.flac')
