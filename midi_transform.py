#!/usr/bin/env python3
"""
MIDI Transformation Script
Takes a MIDI file, extracts first 12 notes, reverses them,
applies intervallic inversion, and inverts the result.
"""

import mido
from mido import MidiFile, MidiTrack, Message
import sys


def extract_first_12_notes(midi_file_path):
    """
    Extract the first 12 note-on events from a MIDI file.
    Returns a list of (note, velocity, time) tuples.
    """
    midi = MidiFile(midi_file_path)
    notes = []
    
    for track in midi.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.velocity > 0:
                notes.append({
                    'note': msg.note,
                    'velocity': msg.velocity,
                    'time': msg.time
                })
                if len(notes) == 12:
                    return notes
    
    return notes


def reverse_notes(notes):
    """
    Reverse the order of notes.
    """
    return list(reversed(notes))


def intervallic_inversion(notes):
    """
    Apply intervallic inversion to a sequence of notes.
    If the interval was +2 semitones, it becomes -2 semitones, and vice versa.
    The first note stays the same.
    """
    if not notes:
        return []
    
    inverted = [notes[0].copy()]  # First note stays the same
    
    for i in range(1, len(notes)):
        # Calculate the interval from previous note
        interval = notes[i]['note'] - notes[i-1]['note']
        
        # Invert the interval (negate it)
        inverted_interval = -interval
        
        # Apply inverted interval to the previous inverted note
        new_note = inverted[i-1]['note'] + inverted_interval
        
        # Ensure the note is within valid MIDI range (0-127)
        new_note = max(0, min(127, new_note))
        
        inverted.append({
            'note': new_note,
            'velocity': notes[i]['velocity'],
            'time': notes[i]['time']
        })
    
    return inverted


def invert_notes(notes, axis=None):
    """
    Invert notes around an axis.
    If no axis is provided, use the middle of the range of the notes.
    """
    if not notes:
        return []
    
    if axis is None:
        # Use the average of min and max notes as the axis
        min_note = min(n['note'] for n in notes)
        max_note = max(n['note'] for n in notes)
        axis = (min_note + max_note) / 2
    
    inverted = []
    for note in notes:
        # Invert around the axis
        new_note = int(2 * axis - note['note'])
        
        # Ensure the note is within valid MIDI range (0-127)
        new_note = max(0, min(127, new_note))
        
        inverted.append({
            'note': new_note,
            'velocity': note['velocity'],
            'time': note['time']
        })
    
    return inverted


def create_midi_file(notes, output_path, tempo=500000):
    """
    Create a MIDI file from a list of notes.
    """
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)
    
    # Add tempo
    track.append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))
    
    # Add note events
    for i, note_data in enumerate(notes):
        # Note on
        track.append(Message('note_on', 
                           note=note_data['note'], 
                           velocity=note_data['velocity'], 
                           time=note_data['time'] if i == 0 else 0))
        
        # Note off (after a duration, e.g., 480 ticks = quarter note at 480 ticks per beat)
        track.append(Message('note_off', 
                           note=note_data['note'], 
                           velocity=0, 
                           time=480))
    
    midi.save(output_path)
    print(f"MIDI file saved to: {output_path}")


def print_notes(notes, title="Notes"):
    """
    Print notes in a readable format.
    """
    print(f"\n{title}:")
    for i, note in enumerate(notes, 1):
        print(f"  {i}. Note: {note['note']} (velocity: {note['velocity']})")


def main(input_file):
    """
    Main processing function.
    """
    print(f"Processing MIDI file: {input_file}")
    
    # Step 1: Extract first 12 notes (same notes)
    step1_notes = extract_first_12_notes(input_file)
    print(f"\nExtracted {len(step1_notes)} notes")
    print_notes(step1_notes, "Step 1: Same Notes (Original)")
    
    # Step 2: Reversed notes
    step2_notes = reverse_notes(step1_notes)
    print_notes(step2_notes, "Step 2: Reversed Notes")
    
    # Step 3: Intervallic inversion of Step 1
    step3_notes = intervallic_inversion(step1_notes)
    print_notes(step3_notes, "Step 3: Intervallic Inversion of Step 1")
    
    # Step 4: Reversed notes of Step 3
    step4_notes = reverse_notes(step3_notes)
    print_notes(step4_notes, "Step 4: Reversed Notes of Step 3")
    
    # Combine all steps into one sequence (48 notes total)
    all_notes = step1_notes + step2_notes + step3_notes + step4_notes
    print(f"\n{'='*60}")
    print(f"COMBINED SEQUENCE ({len(all_notes)} notes total)")
    print(f"{'='*60}")
    
    # Save the result with all 48 notes
    output_file = input_file.rsplit('.', 1)[0] + '_transformed.mid'
    create_midi_file(all_notes, output_file)
    
    return all_notes


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python midi_transform.py <input_midi_file>")
        print("\nExample: python midi_transform.py input.mid")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        main(input_file)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
