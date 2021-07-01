#!/usr/bin/env python3

import tekore as tk
from sys import argv
from time import sleep
import warnings
import configparser
import random

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

	config = configparser.ConfigParser()
	config.read(config_file)

	tail = False
	tail_delay = 0
	cutoff = -1
	vibe = True
	config_vibe = True
	

	if "settings" in config:
		if "tail" in config["settings"]:
			tail = True if config["settings"]["tail"] == "True" else tail
		if "tail_delay" in config["settings"]:
			tail_delay = float(config["settings"]["tail_delay"])
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
#TODO: Make this relevant again


	play = ""
	pause = ""
	previous = ""
	next = ""
	saved = "saved" #""
	notsaved = "notsaved" #""

	# Only update the creds file when showing the track to avoid duplicates or something
#	if len(argv) > 1:
#		if argv[1] == "track":
#			tk.config_to_file(config_file, (conf[0], conf[1], conf[2], user_token.refresh_token))

	while True:
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
	
			
					if isinstance(track, tk.model.CurrentlyPlaying): 
						track_name = track.item.name
						track_artists = track.item.artists
						track_artist_names = track_artists[0].name

						# Cuz non-western characters dont exactly render properly
						if track_name == "佐賀事変" and track_artist_names == "フランシュシュ":
							track_name = "Sagajihen"
							track_artist_names = "Franchouchou"	
						
						for i in range(1, len(track_artists)):
							track_artist_names += ", " + track_artists[i].name
						
						toPrint = track_name + " - " + track_artist_names
						
						if cutoff > 0 and len(toPrint) > cutoff:
							toPrint = toPrint[:cutoff - 3]
							toPrint += "..."
						
						print(toPrint, flush=True)
					else:
						print(" - ", flush=True)
	
				except:
					if config_vibe:
						print(" - ", flush=True)
					else:
						print("Missing config, login again manually")

			elif argv[1] == "playpause_dry":
				try:
					if isinstance(track, tk.model.CurrentlyPlaying):
						if track.is_playing:
							print(pause, flush=True)
						else:
							print(play, flush=True)
					else:
						print(play, flush=True)
					
				except:
					print(play)

			elif argv[1] == "play":
				spotify.playback_resume()
				break
			elif argv[1] == "pause":
				spotify.playback_pause()
				break

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
				break

#TODO: why doesnt this pint in polybar
			elif argv[1] == "saved":
				try:
					id = track.item.uri.split(':')[-1]
					print(saved if spotify.saved_tracks_contains([id])[0] else notsaved)
				except:
					print(notsaved)
	
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
				break
	
			elif argv[1] == "random_queue":
				all_uris = []
				for i in range(0, (spotify.saved_tracks()).total, 50):
					page = (spotify.saved_tracks(limit=50, offset=i)).items
					for j in range(0, len(page)):
						all_uris.append(page[j].track.uri)
				random.shuffle(all_uris)
				for i in range(0, len(all_uris)):
					spotify.playback_queue_add(all_uris[i])
				break

			elif argv[1] == "previous_dry":
				print(previous)
				break
		
			elif argv[1] == "next_dry":
				print(next)
				break
	
			elif argv[1] == "previous":
				try:
					spotify.playback_previous()
				except:
					pass
				print(previous)
				break

			elif argv[1] == "next":
				try:
					spotify.playback_next()
				except:
					pass
				print(next)
				break
	
			else:
				print("Unknown argument")
				break

		else:
			break

		if not tail:
			break
		
		vibe = True
		sleep(tail_delay)

if __name__ == "__main__":
	run_program()

