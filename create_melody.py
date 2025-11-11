#!/usr/bin/env python3
"""
Create a melody from a MIDI file by applying random durations.
Takes all notes from the input file and applies:
1. Random duration: 1/32, 1/16, 1/8, 1/4, 1/2, 1 (whole note)
2. Random modifier: no change, dotted, or silence (hold note for next cycle)
"""

import mido
from mido import MidiFile, MidiTrack, Message
import random
import sys
import csv
from music21 import stream, note, tempo, meter, key, instrument


def extract_all_notes(midi_file_path):
    """
    Extract all note-on events from a MIDI file.
    Returns a list of (note, velocity) tuples.
    """
    midi = MidiFile(midi_file_path)
    notes = []
    
    for track in midi.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.velocity > 0:
                notes.append({
                    'note': msg.note,
                    'velocity': msg.velocity
                })
    
    return notes


def create_melody_with_random_durations(notes, ticks_per_beat=480):
    """
    Apply random durations to notes.
    
    Duration options (based on whole note = 1920 ticks at 480 tpb):
    1: 1/32 = 60 ticks
    2: 1/16 = 120 ticks
    3: 1/8 = 240 ticks
    4: 1/4 = 480 ticks
    5: 1/2 = 960 ticks
    6: 1 (whole) = 1920 ticks
    
    Modifier options:
    1: no changes
    2: dotted note (1.5x duration)
    3: silence (rest - hold note for next cycle)
    """
    # Duration mapping (in ticks)
    duration_map = {
        1: ticks_per_beat // 8,   # 1/32 note = 60 ticks
        2: ticks_per_beat // 4,   # 1/16 note = 120 ticks
        3: ticks_per_beat // 2,   # 1/8 note = 240 ticks
        4: ticks_per_beat,        # 1/4 note = 480 ticks
        5: ticks_per_beat * 2,    # 1/2 note = 960 ticks
        6: ticks_per_beat * 4     # whole note = 1920 ticks
    }
    
    duration_names = {
        1: "1/32",
        2: "1/16",
        3: "1/8",
        4: "1/4",
        5: "1/2",
        6: "1 (whole)"
    }
    
    melody_events = []
    note_index = 0
    held_note = None
    event_number = 1
    
    print("\nGenerating melody with random durations:\n")
    
    while note_index < len(notes):
        # Get the note to use (either held from previous or new from the sequence)
        if held_note is not None:
            current_note = held_note
            held_note = None
            print(f"Event {event_number}: Using held note {current_note['note']} (from note #{note_index})")
        else:
            current_note = notes[note_index]
            print(f"Event {event_number}: Using note #{note_index + 1}: {current_note['note']}")
            note_index += 1
        
        # Step 1: Random duration (1-6)
        duration_choice = random.randint(1, 6)
        base_duration = duration_map[duration_choice]
        duration_name = duration_names[duration_choice]
        
        # Step 2: Random modifier (1-3)
        modifier_choice = random.randint(1, 3)
        
        if modifier_choice == 1:
            # No changes
            final_duration = base_duration
            modifier_name = "normal"
            melody_events.append({
                'type': 'note',
                'note': current_note['note'],
                'velocity': current_note['velocity'],
                'duration': final_duration
            })
            print(f"  Event {event_number}: Note {current_note['note']}, {duration_name} ({modifier_name}), {final_duration} ticks")
            
        elif modifier_choice == 2:
            # Dotted note (1.5x duration)
            final_duration = int(base_duration * 1.5)
            modifier_name = "dotted"
            melody_events.append({
                'type': 'note',
                'note': current_note['note'],
                'velocity': current_note['velocity'],
                'duration': final_duration
            })
            print(f"  Event {event_number}: Note {current_note['note']}, {duration_name} ({modifier_name}), {final_duration} ticks")
            
        else:  # modifier_choice == 3
            # Silence (rest) - hold note for next cycle
            modifier_name = "silence (rest)"
            melody_events.append({
                'type': 'rest',
                'duration': base_duration
            })
            held_note = current_note
            # Note: we already incremented note_index or we're using a held note,
            # so we don't need to adjust it here
            print(f"  Rest, {duration_name}, {base_duration} ticks (note {current_note['note']} held for next cycle)")
        
        event_number += 1
    
    print(f"\nTotal notes in input: {len(notes)}")
    print(f"Total musical events created: {len(melody_events)}")
    
    return melody_events


def midi_note_to_name(midi_note):
    """
    Convert MIDI note number to note name (e.g., 60 -> C4).
    """
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (midi_note // 12) - 1
    note = note_names[midi_note % 12]
    return f"{note}{octave}"


def get_duration_name(duration_ticks, ticks_per_beat=480):
    """
    Convert duration in ticks to a readable name.
    """
    duration_map = {
        60: "1/32",
        90: "1/32 dotted",
        120: "1/16",
        180: "1/16 dotted",
        240: "1/8",
        360: "1/8 dotted",
        480: "1/4",
        720: "1/4 dotted",
        960: "1/2",
        1440: "1/2 dotted",
        1920: "whole",
        2880: "whole dotted"
    }
    
    return duration_map.get(duration_ticks, f"{duration_ticks} ticks")


def get_duration_name_spanish(duration_ticks, ticks_per_beat=480):
    """
    Convert duration in ticks to Spanish name.
    """
    duration_map_spanish = {
        60: "fusa",
        90: "fusa con puntillo",
        120: "semicorchea",
        180: "semicorchea con puntillo",
        240: "corchea",
        360: "corchea con puntillo",
        480: "negra",
        720: "negra con puntillo",
        960: "blanca",
        1440: "blanca con puntillo",
        1920: "redonda",
        2880: "redonda con puntillo"
    }
    
    return duration_map_spanish.get(duration_ticks, f"{duration_ticks} ticks")


def save_melody_to_csv(melody_events, output_path):
    """
    Save melody events to a CSV file.
    """
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Event_Number', 'Type', 'Note_Number', 'Note_Name', 'Velocity', 'Duration_Ticks', 'Duration_Name', 'Duration_Spanish']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for i, event in enumerate(melody_events, 1):
            if event['type'] == 'note':
                writer.writerow({
                    'Event_Number': i,
                    'Type': 'note',
                    'Note_Number': event['note'],
                    'Note_Name': midi_note_to_name(event['note']),
                    'Velocity': event['velocity'],
                    'Duration_Ticks': event['duration'],
                    'Duration_Name': get_duration_name(event['duration']),
                    'Duration_Spanish': get_duration_name_spanish(event['duration'])
                })
            else:  # rest
                writer.writerow({
                    'Event_Number': i,
                    'Type': 'rest',
                    'Note_Number': '',
                    'Note_Name': '',
                    'Velocity': '',
                    'Duration_Ticks': event['duration'],
                    'Duration_Name': get_duration_name(event['duration']),
                    'Duration_Spanish': get_duration_name_spanish(event['duration'])
                })
    
    print(f"CSV file saved to: {output_path}")


def create_midi_from_melody(melody_events, output_path, tempo=500000):
    """
    Create a MIDI file from melody events compatible with MuseScore.
    Forces 4/4 time signature with proper measure tracking.
    """
    # Create MIDI file with Type 1 format (multiple tracks)
    midi = MidiFile(type=1, ticks_per_beat=480)
    
    # Create track
    track = MidiTrack()
    midi.tracks.append(track)
    
    # Add track name
    track.append(mido.MetaMessage('track_name', name='Melody', time=0))
    
    # Add tempo (120 BPM = 500000 microseconds per beat)
    track.append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))
    
    # Add time signature (4/4) - 4 beats per measure, quarter note gets the beat
    # In 4/4: one measure = 4 quarter notes = 1920 ticks (4 * 480)
    track.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, 
                                  clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
    
    # Add key signature (C major)
    track.append(mido.MetaMessage('key_signature', key='C', time=0))
    
    # Set instrument (Program Change to Acoustic Grand Piano = 0)
    track.append(Message('program_change', program=0, time=0, channel=0))
    
    # Add melody events with measure tracking
    accumulated_time = 0
    current_measure_ticks = 0
    measure_length = 1920  # 4/4 time: 4 beats * 480 ticks = 1920 ticks per measure
    
    for i, event in enumerate(melody_events):
        if event['type'] == 'note':
            # Note on with accumulated time (from previous rests)
            track.append(Message('note_on', 
                                note=event['note'], 
                                velocity=event['velocity'], 
                                time=accumulated_time,
                                channel=0))
            
            # Update measure position
            current_measure_ticks += accumulated_time
            
            # Note off after duration
            track.append(Message('note_off', 
                                note=event['note'], 
                                velocity=0, 
                                time=event['duration'],
                                channel=0))
            
            # Update measure position
            current_measure_ticks += event['duration']
            
            # Reset accumulated time after playing a note
            accumulated_time = 0
        else:  # rest
            # Accumulate rest time for the next note
            accumulated_time += event['duration']
    
    # Add end of track marker
    track.append(mido.MetaMessage('end_of_track', time=0))
    
    midi.save(output_path)
    print(f"\nMIDI file saved to: {output_path}")
    print("Time signature: 4/4")
    print(f"Total duration: {current_measure_ticks} ticks ({current_measure_ticks / measure_length:.2f} measures)")


def create_musicxml_from_melody(melody_events, output_path):
    """
    Create a MusicXML file from melody events for MuseScore.
    This provides exact notation control without ambiguity.
    """
    from music21 import stream, note, tempo, meter, key, instrument
    
    # Create a score
    score = stream.Score()
    part = stream.Part()
    
    # Add metadata
    part.insert(0, instrument.Piano())
    part.insert(0, key.Key('C'))
    part.insert(0, meter.TimeSignature('4/4'))
    part.insert(0, tempo.MetronomeMark(number=120))
    
    # Duration mapping (in quarter note lengths)
    # 480 ticks = 1 quarter note
    ticks_per_quarter = 480
    
    for event in melody_events:
        if event['type'] == 'note':
            # Convert ticks to quarter note duration
            duration_quarters = event['duration'] / ticks_per_quarter
            
            # Create note with MIDI pitch
            n = note.Note(event['note'])
            n.quarterLength = duration_quarters
            n.volume.velocity = event['velocity']
            
            part.append(n)
        else:  # rest
            # Convert ticks to quarter note duration
            duration_quarters = event['duration'] / ticks_per_quarter
            
            # Create rest
            r = note.Rest()
            r.quarterLength = duration_quarters
            
            part.append(r)
    
    score.append(part)
    
    # Write to MusicXML
    score.write('musicxml', fp=output_path)
    print(f"MusicXML file saved to: {output_path}")


def main(input_file):
    """
    Main processing function.
    """
    print(f"Processing MIDI file: {input_file}")
    
    # Extract all notes
    notes = extract_all_notes(input_file)
    print(f"Extracted {len(notes)} notes")
    
    # Get base filename without extension
    base_filename = input_file.rsplit('.', 1)[0]
    
    # Generate 3 different variations
    for variation_num in range(1, 4):
        print(f"\n{'='*60}")
        print(f"GENERATING VARIATION {variation_num}")
        print(f"{'='*60}")
        
        # Create melody with random durations
        melody_events = create_melody_with_random_durations(notes)
        
        # Create output filenames with variation number
        midi_output_file = f"{base_filename}_melody_v{variation_num}.mid"
        musicxml_output_file = f"{base_filename}_melody_v{variation_num}.musicxml"
        csv_output_file = f"{base_filename}_melody_v{variation_num}.csv"
        
        # Save the MIDI result
        create_midi_from_melody(melody_events, midi_output_file)
        
        # Save the MusicXML result
        create_musicxml_from_melody(melody_events, musicxml_output_file)
        
        # Save the CSV result
        save_melody_to_csv(melody_events, csv_output_file)
    
    print(f"\n{'='*60}")
    print(f"COMPLETED: 3 variations generated successfully!")
    print(f"{'='*60}")
    
    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_melody.py <input_midi_file>")
        print("\nExample: python create_melody.py chromatic_random_transformed.mid")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        main(input_file)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
