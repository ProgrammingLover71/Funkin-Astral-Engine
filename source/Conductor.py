# Friday Night Funkin' Astral Engine

### Conductor module
# The Conductor allows for precise music and beat handling for any and all states.

import arcade as arc
from StateManager import State
from AssetManager import *
import librosa
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
	song_position: float	# Where we are in the song
	bpm: float				# The current song's BPM

	measure_length_ms: float	# How many milliseconds a measure lasts
	beat_length_ms: float		# How many milliseconds a beat lasts
	step_length_mp: float		# How many milliseconds a step lasts

	listener_states: list[State] = []	# The states that are listening to the Conductor's events (if it's not all of them, that's bad)
	bpm_cache: dict[str, BPMData] = {}	# The BPM cache for all loaded songs


	@classmethod
	def play_audio(cls, audio: SoundAsset):
		cls.song_position = 0.0
		cls.bpm = cls.getStartingBPM(audio)
		cls.computeMeasureTimes(audio)
		# Play the sound and load the step/beat/measure times
		cls.measure_length_ms 	= cls.bpm_cache[audio.sound_path].measure_length_ms
		cls.beat_length_ms 		= cls.bpm_cache[audio.sound_path].beat_length_ms
		cls.step_length_ms 		= cls.bpm_cache[audio.sound_path].step_length_ms
		arc.sound.play_sound(audio.sound)

	
	@classmethod
	def getStartingBPM(cls, audio: SoundAsset):
		# Load the sound using librosa and estimate the BPM (if we didn't already)
		if cls.bpm_cache.get(audio.sound_path) == None:
			y, sr = librosa.load(audio.sound_path, sr=None, mono=False)
			onset_env = librosa.onset.onset_strength(y=y, sr=sr)
			_, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
			beat_times = librosa.frames_to_time(beats, sr=sr)
			intervals = np.diff(beat_times)
			# Calculate the average BPM for the song and cache it
			bpms = 60 / intervals
			cls.bpm_cache[audio.sound_path] = BPMData(np.median(bpms), 0, 0)
		return cls.bpm_cache[audio.sound_path]
	

	@classmethod
	def computeMeasureTimes(cls, audio: SoundAsset):
		if cls.bpm_cache.get(audio.sound_path) == None:
			# Compute the bpm of the song
			_ = cls.getStartingBPM(audio)

		measure_time_s = 60 / cls.bpm_cache[audio.sound_path].measure_length_ms
		beat_time_s = measure_time_s * 4
		step_time_s = measure_time_s * 16
		# Store the values in the BPM cache
		cls.bpm_cache[audio.sound_path].measure_length_ms 	= 1000.0 * measure_time_s
		cls.bpm_cache[audio.sound_path].beat_length_ms 		= 1000.0 * beat_time_s
		cls.bpm_cache[audio.sound_path].step_length_ms		= 1000.0 * step_time_s
