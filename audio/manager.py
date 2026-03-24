import math
from array import array

import pygame

from settings import (
    AUDIO_BUFFER_SIZE,
    AUDIO_MUSIC_VOLUME,
    AUDIO_SFX_VOLUME,
    AUDIO_SAMPLE_RATE,
)


class AudioManager:
    def __init__(self):
        self.enabled = False
        self.current_track = None
        self.music_paused = False
        self.music_channel = None
        self.effect_channels = []
        self.sounds = {}
        self.music_tracks = {}

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=AUDIO_SAMPLE_RATE, size=-16, channels=1, buffer=AUDIO_BUFFER_SIZE)
            pygame.mixer.set_num_channels(12)
            self.music_channel = pygame.mixer.Channel(0)
            self.effect_channels = [pygame.mixer.Channel(index) for index in range(1, 12)]
            self.sounds = self.build_sound_bank()
            self.music_tracks = self.build_music_bank()
            self.enabled = True
        except pygame.error:
            self.enabled = False

    def build_sound_bank(self):
        return {
            "menu_select": self.create_sound(
                0.18,
                [
                    {"start": 0.00, "duration": 0.09, "frequency": 493.88, "glide_to": 659.25, "waveform": "triangle", "volume": 0.85},
                    {"start": 0.04, "duration": 0.12, "frequency": 739.99, "waveform": "sine", "volume": 0.40},
                ],
                master=0.34,
            ),
            "pause": self.create_sound(
                0.16,
                [
                    {"start": 0.00, "duration": 0.08, "frequency": 523.25, "glide_to": 392.00, "waveform": "triangle", "volume": 0.80},
                ],
                master=0.28,
            ),
            "jump": self.create_sound(
                0.20,
                [
                    {"start": 0.00, "duration": 0.12, "frequency": 349.23, "glide_to": 440.00, "waveform": "triangle", "volume": 0.85},
                ],
                master=0.28,
            ),
            "super_jump": self.create_sound(
                0.32,
                [
                    {"start": 0.00, "duration": 0.20, "frequency": 329.63, "glide_to": 659.25, "waveform": "triangle", "volume": 0.90},
                    {"start": 0.06, "duration": 0.24, "frequency": 493.88, "glide_to": 880.00, "waveform": "sine", "volume": 0.38},
                ],
                master=0.36,
            ),
            "fish_collect": self.create_sound(
                0.22,
                [
                    {"start": 0.00, "duration": 0.08, "frequency": 659.25, "waveform": "triangle", "volume": 0.70},
                    {"start": 0.05, "duration": 0.08, "frequency": 783.99, "waveform": "triangle", "volume": 0.72},
                    {"start": 0.10, "duration": 0.10, "frequency": 987.77, "waveform": "sine", "volume": 0.46},
                ],
                master=0.34,
            ),
            "exit_open": self.create_sound(
                0.40,
                [
                    {"start": 0.00, "duration": 0.16, "frequency": 392.00, "waveform": "triangle", "volume": 0.55},
                    {"start": 0.08, "duration": 0.16, "frequency": 523.25, "waveform": "triangle", "volume": 0.60},
                    {"start": 0.16, "duration": 0.20, "frequency": 659.25, "waveform": "sine", "volume": 0.42},
                ],
                master=0.34,
            ),
            "bubble_activate": self.create_sound(
                0.45,
                [
                    {"start": 0.00, "duration": 0.30, "frequency": 180.00, "glide_to": 420.00, "waveform": "sine", "volume": 0.55},
                    {"start": 0.10, "duration": 0.28, "frequency": 260.00, "glide_to": 520.00, "waveform": "triangle", "volume": 0.32},
                ],
                master=0.34,
            ),
            "bubble_hit": self.create_sound(
                0.30,
                [
                    {"start": 0.00, "duration": 0.08, "frequency": 860.00, "waveform": "sine", "volume": 0.35},
                    {"start": 0.05, "duration": 0.10, "frequency": 720.00, "waveform": "sine", "volume": 0.30},
                    {"start": 0.12, "duration": 0.08, "frequency": 960.00, "waveform": "triangle", "volume": 0.28},
                ],
                master=0.28,
            ),
            "lantern_dim": self.create_sound(
                0.24,
                [
                    {"start": 0.00, "duration": 0.18, "frequency": 622.25, "glide_to": 523.25, "waveform": "sine", "volume": 0.42},
                ],
                master=0.20,
            ),
            "damage": self.create_sound(
                0.34,
                [
                    {"start": 0.00, "duration": 0.26, "frequency": 196.00, "glide_to": 138.59, "waveform": "square", "volume": 0.48},
                    {"start": 0.02, "duration": 0.24, "frequency": 92.50, "waveform": "noise", "volume": 0.22},
                ],
                master=0.34,
            ),
            "level_complete": self.create_sound(
                0.64,
                [
                    {"start": 0.00, "duration": 0.16, "frequency": 523.25, "waveform": "triangle", "volume": 0.62},
                    {"start": 0.12, "duration": 0.16, "frequency": 659.25, "waveform": "triangle", "volume": 0.64},
                    {"start": 0.24, "duration": 0.20, "frequency": 783.99, "waveform": "triangle", "volume": 0.68},
                    {"start": 0.36, "duration": 0.24, "frequency": 1046.50, "waveform": "sine", "volume": 0.44},
                ],
                master=0.34,
            ),
            "restart": self.create_sound(
                0.18,
                [
                    {"start": 0.00, "duration": 0.10, "frequency": 329.63, "glide_to": 293.66, "waveform": "triangle", "volume": 0.58},
                ],
                master=0.22,
            ),
            "game_over": self.create_sound(
                0.70,
                [
                    {"start": 0.00, "duration": 0.20, "frequency": 392.00, "waveform": "square", "volume": 0.40},
                    {"start": 0.18, "duration": 0.22, "frequency": 311.13, "waveform": "square", "volume": 0.42},
                    {"start": 0.40, "duration": 0.26, "frequency": 233.08, "waveform": "triangle", "volume": 0.40},
                ],
                master=0.32,
            ),
            "victory": self.create_sound(
                0.86,
                [
                    {"start": 0.00, "duration": 0.16, "frequency": 523.25, "waveform": "triangle", "volume": 0.56},
                    {"start": 0.14, "duration": 0.16, "frequency": 659.25, "waveform": "triangle", "volume": 0.60},
                    {"start": 0.28, "duration": 0.18, "frequency": 783.99, "waveform": "triangle", "volume": 0.64},
                    {"start": 0.44, "duration": 0.18, "frequency": 1046.50, "waveform": "triangle", "volume": 0.68},
                    {"start": 0.58, "duration": 0.24, "frequency": 1318.51, "waveform": "sine", "volume": 0.38},
                ],
                master=0.36,
            ),
        }

    def build_music_bank(self):
        return {
            "menu": self.create_sound(
                8.0,
                self.build_menu_music_events(),
                master=0.26,
            ),
            "lagoon": self.create_sound(
                8.0,
                self.build_lagoon_music_events(),
                master=0.24,
            ),
        }

    def build_menu_music_events(self):
        beat = 0.5
        events = []
        pad_chords = (
            (0, (523.25, 659.25, 783.99)),
            (4, (493.88, 622.25, 739.99)),
            (8, (440.00, 554.37, 659.25)),
            (12, (493.88, 659.25, 783.99)),
        )
        for start_beat, chord in pad_chords:
            for frequency in chord:
                events.append(
                    {
                        "start": start_beat * beat,
                        "duration": 1.8,
                        "frequency": frequency,
                        "waveform": "sine",
                        "volume": 0.13,
                    }
                )

        melody = (659.25, 783.99, 880.00, 783.99, 739.99, 659.25, 587.33, 659.25)
        for index, frequency in enumerate(melody * 2):
            events.append(
                {
                    "start": index * 0.5,
                    "duration": 0.42,
                    "frequency": frequency,
                    "waveform": "triangle",
                    "volume": 0.22,
                }
            )

        return events

    def build_lagoon_music_events(self):
        events = []
        bass_pattern = (174.61, 196.00, 220.00, 196.00)
        for step in range(16):
            events.append(
                {
                    "start": step * 0.5,
                    "duration": 0.36,
                    "frequency": bass_pattern[step % len(bass_pattern)],
                    "waveform": "triangle",
                    "volume": 0.20,
                }
            )

        pulse_pattern = (392.00, 440.00, 493.88, 440.00, 392.00, 440.00, 523.25, 440.00)
        for step, frequency in enumerate(pulse_pattern * 2):
            events.append(
                {
                    "start": step * 0.5,
                    "duration": 0.26,
                    "frequency": frequency,
                    "waveform": "sine",
                    "volume": 0.16,
                }
            )

        shimmer_notes = (659.25, 587.33, 622.25, 659.25, 739.99, 659.25, 622.25, 587.33)
        for step, frequency in enumerate(shimmer_notes):
            events.append(
                {
                    "start": 0.25 + step,
                    "duration": 0.62,
                    "frequency": frequency,
                    "waveform": "sine",
                    "volume": 0.12,
                }
            )

        return events

    def waveform_value(self, waveform, phase):
        if waveform == "sine":
            return math.sin(math.tau * phase)
        if waveform == "triangle":
            return 1.0 - 4.0 * abs((phase % 1.0) - 0.5)
        if waveform == "square":
            return 1.0 if (phase % 1.0) < 0.5 else -1.0
        if waveform == "noise":
            return math.sin(phase * 14391.7) * 0.5 + math.sin(phase * 7311.3) * 0.5
        return math.sin(math.tau * phase)

    def add_event(self, samples, event):
        start_index = int(event["start"] * AUDIO_SAMPLE_RATE)
        duration_samples = max(1, int(event["duration"] * AUDIO_SAMPLE_RATE))
        attack_samples = max(1, int(duration_samples * 0.10))
        release_samples = max(1, int(duration_samples * 0.28))
        base_frequency = event.get("frequency", 220.0)
        glide_to = event.get("glide_to")
        waveform = event.get("waveform", "sine")
        volume = event.get("volume", 0.5)

        for index in range(duration_samples):
            sample_index = start_index + index
            if sample_index >= len(samples):
                break

            progress = index / duration_samples
            if glide_to is None:
                frequency = base_frequency
            else:
                frequency = base_frequency + (glide_to - base_frequency) * progress

            phase = (index / AUDIO_SAMPLE_RATE) * frequency
            value = self.waveform_value(waveform, phase)

            if index < attack_samples:
                envelope = index / attack_samples
            elif index >= duration_samples - release_samples:
                envelope = (duration_samples - index) / release_samples
            else:
                envelope = 1.0

            samples[sample_index] += value * envelope * volume

    def create_sound(self, length_seconds, events, master=0.3):
        sample_count = max(1, int(length_seconds * AUDIO_SAMPLE_RATE))
        samples = [0.0] * sample_count

        for event in events:
            self.add_event(samples, event)

        peak = max((abs(sample) for sample in samples), default=1.0) or 1.0
        scale = (32767 * master)
        pcm = array(
            "h",
            (
                max(-32767, min(32767, int((sample / peak) * scale)))
                for sample in samples
            ),
        )
        return pygame.mixer.Sound(buffer=pcm.tobytes())

    def play_sfx(self, sound_name):
        if not self.enabled:
            return
        sound = self.sounds.get(sound_name)
        if sound is None:
            return
        channel = next((channel for channel in self.effect_channels if not channel.get_busy()), None)
        if channel is None and self.effect_channels:
            channel = self.effect_channels[0]
        if channel is None:
            return
        channel.set_volume(AUDIO_SFX_VOLUME)
        channel.play(sound)

    def play_music(self, track_name):
        if not self.enabled:
            return
        if track_name == self.current_track and self.music_channel.get_busy():
            return

        if self.music_channel.get_busy():
            self.music_channel.fadeout(350)

        self.current_track = track_name
        self.music_paused = False

        if track_name is None:
            return

        track = self.music_tracks.get(track_name)
        if track is None:
            return

        self.music_channel.set_volume(AUDIO_MUSIC_VOLUME)
        self.music_channel.play(track, loops=-1, fade_ms=450)

    def pause_music(self):
        if not self.enabled or self.music_channel is None:
            return
        self.music_channel.pause()
        self.music_paused = True

    def resume_music(self):
        if not self.enabled or self.music_channel is None or not self.music_paused:
            return
        self.music_channel.unpause()
        self.music_paused = False
