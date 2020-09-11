#!/usr/bin/env python3

import tekore as tk
from sys import argv
import warnings

def login():
	user_token = tk.prompt_for_user_token(
		client_id,
		client_secret,
		redirect_uri,
		scope=tk.scope.every
	)
	return user_token


config_file = "/home/kip/.config/polybar/spotify-status/config.cfg"
#config_file = "/home/kip/spotify-status/config.cfg"

warnings.simplefilter('error')

try:
	conf = tk.config_from_file(config_file, return_refresh=True)
except tk.MissingConfigurationWarning:
	print("Missing config, login again manually")
	exit()

warnings.simplefilter('ignore')

user_token = tk.refresh_user_token(*conf[:2], conf[3])

spotify = tk.Spotify(user_token)

play = ""
pause = ""
previous = ""
next = ""

if len(argv) > 1:
	track = spotify.playback_currently_playing()
	if argv[1] == "track":
		
		tk.config_to_file(config_file, (conf[0], conf[1], conf[2], user_token.refresh_token))		# Only update the creds file when showing the track to avoid duplicates or something
	
		if isinstance(track, tk.model.CurrentlyPlaying): 
			track_name = track.item.name
			track_artists = track.item.artists
			track_artist_names = track_artists[0].name

			for i in range(1, len(track_artists)):
				track_artist_names += ", " + track_artists[i].name

			print(track_name + " - " + track_artist_names)
		else:
			print(" - ")

	elif argv[1] == "playpause_dry":
		if isinstance(track, tk.model.CurrentlyPlaying):
			if track.is_playing:
				print(pause)
			else:
				print(play)
		else:
			print(play)
	
	elif argv[1] == "playpause":
		if isinstance(track, tk.model.CurrentlyPlaying):
			if track.is_playing:
				spotify.playback_pause()
				print(play)
			else:
				spotify.playback_resume()
				print(pause)
		else:
			print(play)

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

