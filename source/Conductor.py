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
	bpm_data: float			# The current song's BPM

	measure_length_ms: float	# How many milliseconds a measure lasts
	beat_length_ms: float		# How many milliseconds a beat lasts
	step_length_ms: float		# How many milliseconds a step lasts

	current_beat: int = -1
	current_step: int = -1

	bpm_cache: dict[str, BPMData] = {}	# The BPM cache for all loaded songs


	@classmethod
	def load_audio(cls, audio: SoundAsset, bpm_override: float | None = None):
		cls.song_position = 0.0
		cls.bpm_data = cls.getStartingBPM(audio)
		if bpm_override == None:
			target_bpm = cls.bpm_data
		else:
			target_bpm = bpm_override
		cls.computeMeasureTimes(audio, target_bpm)
		# Load the step/beat/measure times
		cls.measure_length_ms 	= cls.bpm_cache[audio.sound_path].measure_length_ms
		cls.beat_length_ms 		= cls.bpm_cache[audio.sound_path].beat_length_ms
		cls.step_length_ms 		= cls.bpm_cache[audio.sound_path].step_length_ms
	
	@classmethod
	def play_audio(cls, audio: SoundAsset, bpm_override: float | None = None):
		# Load the step/beat/measure times and play the audio
		cls.load_audio(audio, bpm_override = bpm_override)
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
	def computeMeasureTimes(cls, audio: SoundAsset, bpm_override: float | None = None):
		if bpm_override == None:
			bpm_data = cls.getStartingBPM(audio)
			measure_time_s = 60 / bpm_data.bpm
		else:
			measure_time_s = 60 / bpm_override
		beat_time_s = measure_time_s * 4
		step_time_s = measure_time_s * 16
		# Store the values in the BPM cache
		cls.bpm_cache[audio.sound_path].measure_length_ms 	= 1000.0 * measure_time_s
		cls.bpm_cache[audio.sound_path].beat_length_ms 		= 1000.0 * beat_time_s
		cls.bpm_cache[audio.sound_path].step_length_ms		= 1000.0 * step_time_s


	@classmethod
	def update(cls, dt: float):
		cls.song_position += dt

		# Compute the current beat and step positions
		new_beat = int(cls.song_position / (cls.beat_length_ms / 1000.0))
		new_step = int(cls.song_position / (cls.step_length_ms / 1000.0))

		beat_just_hit = (new_beat != cls.current_beat)
		step_just_hit = (new_step != cls.current_step)

		cls.current_beat = new_beat
		cls.current_step = new_step

		return beat_just_hit, step_just_hit

