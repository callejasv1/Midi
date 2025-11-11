#!/usr/bin/env python3
"""
Create a MIDI file with chromatic notes in random order.
12 notes from C1 to B1 (C1, C#1, D1, D#1, E1, F1, F#1, G1, G#1, A1, A#1, B1)
No repeats, using sharps (#).
"""

import mido
from mido import MidiFile, MidiTrack, Message
import random


def create_chromatic_midi(output_file='chromatic_random.mid'):
    """
    Create a MIDI file with 12 chromatic notes in random order.
    C1 = MIDI note 24
    """
    # C1 starts at MIDI note 24
    # The 12 chromatic notes from C1 to B1
    chromatic_notes = list(range(24, 36))  # 24-35: C1, C#1, D1, D#1, E1, F1, F#1, G1, G#1, A1, A#1, B1
    
    # Randomize the order
    random.shuffle(chromatic_notes)
    
    # Note names for display
    note_names = ['C1', 'C#1', 'D1', 'D#1', 'E1', 'F1', 'F#1', 'G1', 'G#1', 'A1', 'A#1', 'B1']
    
    # Print the random order
    print("Random chromatic sequence:")
    for i, note in enumerate(chromatic_notes, 1):
        note_name = note_names[note - 24]
        print(f"  {i}. {note_name} (MIDI note {note})")
    
    # Create MIDI file
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)
    
    # Add tempo (120 BPM)
    track.append(mido.MetaMessage('set_tempo', tempo=500000, time=0))
    
    # Add notes
    for i, note in enumerate(chromatic_notes):
        # Note on (first note starts immediately, others after previous note off)
        track.append(Message('note_on', note=note, velocity=80, time=0))
        
        # Note off after 480 ticks (quarter note at 480 ticks per beat)
        track.append(Message('note_off', note=note, velocity=0, time=480))
    
    # Save the file
    midi.save(output_file)
    print(f"\nMIDI file created: {output_file}")


if __name__ == "__main__":
    create_chromatic_midi()
