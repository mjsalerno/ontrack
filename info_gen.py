import json

album = 'Bob Dylan: The 1966 Live Recordings'
artist = 'Bob Dylan'
disc_total = 36

with open('tracks.txt') as tracks:
    track_lst = tracks.readlines()
track_index = 0
disc = 1

with open('comments.txt') as comments:
    for com in comments:
        info = {'album': album, 'comment': com.strip(), 'artist': artist, 'disc': disc, 'disc_total': disc_total, 'tracks': []}

        for i in range(track_index, len(track_lst)):
            track = track_lst[i].strip()

            if len(track) == 0:
                with open('result.json', 'w') as fp:
                    json.dump(info, fp, indent=4)
                track_index = i + 1
                disc += 1
                break
            else:
                info['tracks'].append(track)
