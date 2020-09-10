#!/usr/bin/env python3

import tekore as tk
from sys import argv

def login():
	user_token = tk.prompt_for_user_token(
		client_id,
		client_secret,
		redirect_uri,
		scope=tk.scope.every
	)
	return user_token


config_file = "/home/kip/.config/polybar/spotify-status/config.cfg"

conf = tk.config_from_file(config_file, return_refresh=True)
user_token = tk.refresh_user_token(*conf[:2], conf[3])

spotify = tk.Spotify(user_token)

tk.config_to_file(config_file, (None, None, None, user_token.refresh_token))

play = ""
pause = ""
previous = ""
next = ""

if len(argv) > 1:
	track = spotify.playback_currently_playing()
	if argv[1] == "track":
		track_name = track.item.name
		track_artists = track.item.artists
		track_artist_names = track_artists[0].name

		for i in range(1, len(track_artists)):
			track_artist_names += ", " + track_artists[i].name

		print(track_name + " - " + track_artist_names)

	elif argv[1] == "playpause_dry":
		if track.is_playing:
			print(pause)
		else:
			print(play)
	
	elif argv[1] == "playpause":
		if track.is_playing:
			spotify.playback_pause()
			print(play)
		else:
			spotify.playback_resume()
			print(pause)

	elif argv[1] == "previous_dry":
		print(previous)
	
	elif argv[1] == "next_dry":
		print(next)

	elif argv[1] == "previous":
		spotify.playback_previous()
		print(previous)

	elif argv[1] == "next":
		spotify.playback_next()
		print(next)

	else:
		print("Unknown argument")

