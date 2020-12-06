#!/usr/bin/env python3

import tekore as tk
from sys import argv
from time import sleep
import warnings
import configparser


def login():
	user_token = tk.prompt_for_user_token(
		client_id,
		client_secret,
		redirect_uri,
		scope=tk.scope.every
	)
	return user_token

def run_program():

	config_file = "/home/kip/.config/polybar/spotify-status/config.cfg"
#	config_file = "/home/kip/spotify-status/config.cfg"

	config = configparser.ConfigParser()
	config.read(config_file)

	tail = False
	cutoff = -1
	vibe = True
	config_vibe = True


	if "settings" in config:
		if "tail" in config["settings"]:
			tail = True if config["settings"]["tail"] == "True" else tail
		if "active" in config["settings"]:
			if config["settings"]["active"] == "False":
				return
		if "cutoff" in config["settings"]:
			cutoff = int(config["settings"]["cutoff"])

	try:
		warnings.simplefilter('error')
		
		try:
			conf = tk.config_from_file(config_file, return_refresh=True)
		except tk.MissingConfigurationWarning:
			print("fuckfuck config")
			return
			config_vibe = False
			raise Exception("")

		warnings.simplefilter('ignore')
	
		user_token = tk.refresh_user_token(*conf[:2], conf[3])
	
		spotify = tk.Spotify(user_token)
			
	except:
		vibe = False

	play = ""
	pause = ""
	previous = ""
	next = ""
	saved = ""
	notsaved = ""
	
	if len(argv) > 1:
		try:
			track = spotify.playback_currently_playing()
		except:
			track = 0
			vibe = False

		if argv[1] == "track":
			try:
				if not vibe:
					raise Exception("WE NOT GOOD FAM")

				tk.config_to_file(config_file, (conf[0], conf[1], conf[2], user_token.refresh_token))		# Only update the creds file when showing the track to avoid duplicates or something
				while True:		
		
					if isinstance(track, tk.model.CurrentlyPlaying): 
						track_name = track.item.name
						track_artists = track.item.artists
						track_artist_names = track_artists[0].name
	
						for i in range(1, len(track_artists)):
							track_artist_names += ", " + track_artists[i].name
					
						toPrint = track_name + " - " + track_artist_names
					
						if cutoff > 0 and len(toPrint) > cutoff:
							toPrint = toPrint[:cutoff - 3]
							toPrint += "..."
					
						print(toPrint, flush=True)
					else:
						print(" - ", flush=True)

					if not tail:
						break
					sleep(1)
					track = spotify.playback_currently_playing()
			except:
				if config_vibe:
					print(" - ", flush=True)
				else:
					print("Missing config, login again manually")
				return

		elif argv[1] == "playpause_dry":
			try:
				while True:
					if isinstance(track, tk.model.CurrentlyPlaying):
						if track.is_playing:
							print(pause, flush=True)
						else:
							print(play, flush=True)
					else:
						print(play, flush=True)
				
					if not tail:
						break
					sleep(1)
					track = spotify.playback_currently_playing()
			except:
				print(play)
				return

		elif argv[1] == "playpause":
			try:
				if isinstance(track, tk.model.CurrentlyPlaying):
					if track.is_playing:
						spotify.playback_pause()
						print(play)
					else:
						spotify.playback_resume()
						print(pause)
				else:
					print(play)
			except:
				print(play)
				return

		elif argv[1] == "saved":
			try:
				id = track.item.uri.split(':')[-1]
				print(saved if spotify.saved_tracks_contains([id])[0] else notsaved)
			except:
				print(notsaved)
				return

		elif argv[1] == "save":
			try:
				id = track.item.uri.split(':')[-1]

				if spotify.saved_tracks_contains([id])[0]:
					spotify.saved_tracks_delete([id])
					print(notsaved)
				else:
					spotify.saved_tracks_add([id])
					print(saved)

			except:
				print(notsaved)
				return

		elif argv[1] == "previous_dry":
			print(previous)
	
		elif argv[1] == "next_dry":
			print(next)

		elif argv[1] == "previous":
			try:
				spotify.playback_previous()
			except:
				pass
			print(previous)

		elif argv[1] == "next":
			try:
				spotify.playback_next()
			except:
				pass
			print(next)

		else:
			print("Unknown argument")


if __name__ == "__main__":
	run_program()

