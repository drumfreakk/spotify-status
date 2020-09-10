#!/usr/bin/env python3

import tekore as tk
import time

def login():
	user_token = tk.prompt_for_user_token(
		client_id,
		client_secret,
		redirect_uri,
		scope=tk.scope.every
	)
	return user_token


config_file = "config.cfg"

conf = tk.config_from_file(config_file, return_refresh=True)
user_token = tk.refresh_user_token(*conf[:2], conf[3])

spotify = tk.Spotify(user_token)

tk.config_to_file(config_file, (None, None, None, user_token.refresh_token))

track = spotify.playback_currently_playing()
track_name = track.item.name
track_artists = track.item.artists
track_artist_names = track_artists[0].name

for i in range(1, len(track_artists)):
	track_artist_names += ", " + track_artists[i].name

print(track_name)
print(track_artist_names)

#spotify.playback_previous()
#spotify.playback_next()
#spotify.playback_pause()
#time.sleep(1)
#spotify.playback_resume()
