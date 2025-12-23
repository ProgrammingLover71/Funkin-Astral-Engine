# Friday Night Funkin' Astral Engine

### Conductor
# The Conductor allows for precise music and beat handling for any and all states.

import arcade as arc
from StateManager import State
from AssetManager import *
import librosa
import pyglet
import numpy as np
from dataclasses import dataclass

# A measure is		 4 beats
# A measure is also 16 steps
# `beat_hit()` runs  4 times a measure
# `step_hit()` runs 16 times a measure


@dataclass
class BPMData:
	bpm: float
	measure_length_ms: 	float
	beat_length_ms:		float
	step_length_ms: 	float


class Conductor:
	song_position: float				# Where we are in the song
	bpm_data: BPMData					# The current song's BPM
	music_player: pyglet.media.Player	# The music player for this song
	current_song: arc.Sound				# The current sound

	measure_length_ms: float	# How many milliseconds a measure lasts
	beat_length_ms: float		# How many milliseconds a beat lasts
	step_length_ms: float		# How many milliseconds a step lasts

	current_beat: int = -1
	current_step: int = -1

	bpm_cache: dict[str, BPMData] = {}	# The BPM cache for all loaded songs

	def __init__(self) -> None:
		self.reset()
	
	
	def reset(self) -> None:
		self.song_position = 0.0
		self.bpm_data = None
		self.measure_length_ms	= 0.0
		self.beat_length_ms		= 0.0
		self.step_length_ms		= 0.0
		self.current_beat 		= -1
		self.current_step		= -1
	
	def load_audio(self, audio: SoundAsset, bpm_override: float | None = None) -> None:
		# Prep the conductor for playing the song
		self.song_position	= 0.0
		self.current_beat	= 0
		self.current_step	= 0

		if bpm_override == None:
			self.bpm_data = self.getBPMData(audio)
			target_bpm = self.bpm_data.bpm
		else:
			# Make the data ourselves instead of computing it like morons
			self.bpm_cache[audio.sound_path] = BPMData(bpm_override, 0, 0, 0)
			self.bpm_data = self.bpm_cache[audio.sound_path]
			target_bpm = bpm_override
		self.computeMeasureTimes(audio, target_bpm)
		# Load the step/beat/measure times
		self.measure_length_ms 	= self.bpm_cache[audio.sound_path].measure_length_ms
		self.beat_length_ms 		= self.bpm_cache[audio.sound_path].beat_length_ms
		self.step_length_ms 		= self.bpm_cache[audio.sound_path].step_length_ms
	
	
	def play_audio(self, audio: SoundAsset, bpm_override: float | None = None) -> None:
		# Load the step/beat/measure times and play the audio
		self.load_audio(audio, bpm_override = bpm_override)
		self.current_song = audio.sound
		self.music_player = arc.sound.play_sound(audio.sound)

	
	def getBPMData(self, audio: SoundAsset) -> BPMData:
		# Load the sound using librosa and estimate the BPM (if we didn't already)
		if self.bpm_cache.get(audio.sound_path) == None:
			# Downsample and cut the song so we can quickly get its BPM faster
			y, sr = librosa.load(audio.sound_path, sr=11025, mono=True)
			y, _ = librosa.effects.trim(y, top_db=20)

			onset_env = librosa.onset.onset_strength(y=y, sr=sr)
			_, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
			beat_times = librosa.frames_to_time(beats, sr=sr)
			intervals = np.diff(beat_times)
			# Calculate the average BPM for the song and cache it
			bpms = 60 / intervals
			self.bpm_cache[audio.sound_path] = BPMData(np.median(bpms), 0, 0, 0)

		return self.bpm_cache[audio.sound_path]
	

	
	def computeMeasureTimes(self, audio: SoundAsset, bpm_override: float | None = None) -> None:
		if bpm_override == None:
			bpm_data = self.getBPMData(audio)
			beat_time_s = 60 / bpm_data.bpm
		else:
			beat_time_s = 60 / bpm_override
		measure_time_s	= beat_time_s * 4
		step_time_s		= beat_time_s / 4
		# Store the values in the BPM cache
		self.bpm_cache[audio.sound_path].measure_length_ms 	= 1000.0 * measure_time_s
		self.bpm_cache[audio.sound_path].beat_length_ms 	= 1000.0 * beat_time_s
		self.bpm_cache[audio.sound_path].step_length_ms		= 1000.0 * step_time_s
		
	
	def update(self) -> tuple[bool, bool]:
		self.song_position = self.current_song.get_stream_position(self.music_player)

		# Compute the current beat and step positions
		new_beat = int(self.song_position / (self.beat_length_ms / 1000.0))
		new_step = int(self.song_position / (self.step_length_ms / 1000.0))

		beat_just_hit = (new_beat != self.current_beat)
		step_just_hit = (new_step != self.current_step)

		self.current_beat = new_beat
		self.current_step = new_step
		
		return beat_just_hit, step_just_hit

