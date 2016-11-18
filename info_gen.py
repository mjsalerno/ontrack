#!/usr/bin/env python
import argparse
import json


def main():
    parser = argparse.ArgumentParser(description='Generate info JSON for the on_track program.')

    parser.add_argument('--artist', help='Specify the name of the artist.', type=str, required=True, dest='art',
                        metavar='<artist>')

    parser.add_argument('--album', help='Specify the name of the album.', type=str, required=True, dest='alb',
                        metavar='<album>')

    parser.add_argument('--disc-total', '-dt', help='Specify the number of discs.', type=int, required=True, dest='dt',
                        metavar='<disc total>')

    parser.add_argument('--tracks', '-t', help='Specify the tracks file.', type=str, required=True, dest='tracks',
                        metavar='<tracks file>')

    parser.add_argument('--comments', '-c', help='Specify the comments file.', type=str, required=True, dest='comm',
                        metavar='<comments file>')

    parser.add_argument('--output-dir', '-o', help='Specify the output directory.', type=str, required=False,
                        dest='dir', metavar='<comments file>', default='./')

    args = parser.parse_args()

    if not args.dir.endswith(('\\', '/')):
        args.dir += '/'

    album = args.alb  # 'Bob Dylan: The 1966 Live Recordings'
    artist = args.art  # 'Bob Dylan'
    disc_total = args.dt  # 36

    with open(args.tracks) as tracks:
        track_lst = tracks.readlines()
    track_index = 0
    disc = 1

    with open(args.comm) as comments:
        for com in comments:
            info = {'album': album, 'comment': com.strip(), 'artist': artist, 'disc': disc, 'disc_total': disc_total,
                    'tracks': []}

            for i in range(track_index, len(track_lst)):
                track = track_lst[i].strip()

                if len(track) == 0:
                    with open(args.dir + 'info-' + str(disc).zfill(2) + '.json', 'w') as fp:
                        json.dump(info, fp, indent=4)
                    track_index = i + 1
                    disc += 1
                    break
                else:
                    info['tracks'].append(track)


if __name__ == "__main__":
    main()
