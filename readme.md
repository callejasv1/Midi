# MIDI Transformation and Generation Scripts

This project contains a collection of Python scripts to programmatically create and manipulate MIDI files. You can generate a base chromatic sequence, apply complex transformations to it, and then create rhythmic variations from the result.

## Scripts Overview

There are three main scripts in this project:

1.  **`create_chromatic_midi.py`**: Generates a MIDI file containing a random sequence of the 12 chromatic notes from C1 to B1.
2.  **`midi_transform.py`**: Takes an input MIDI file and applies a series of transformations (reversal, intervallic inversion) to create a new, longer sequence.
3.  **`create_melody.py`**: Takes an input MIDI file and generates three unique melodic variations by applying randomized rhythms and rests. It outputs MIDI, MusicXML, and CSV files for each variation.

## Installation

These scripts require Python 3 and a few external libraries.

1.  **Clone the repository or download the scripts.**

2.  **Install the required Python libraries:**

    ```bash
    pip install mido music21
    ```

## Workflow and Usage

The scripts are designed to be used in a chain to produce complex musical outputs from a simple, generated source.

### Step 1: Create the Base Chromatic MIDI

Run `create_chromatic_midi.py` to generate a MIDI file with 12 random chromatic notes.

**Usage:**
```bash
python create_chromatic_midi.py
```

**Output:**
- `chromatic_random.mid`: A MIDI file containing the 12-note sequence.

---

### Step 2: Transform the Sequence

Use `midi_transform.py` with the file generated in the previous step. This script will perform a 4-part transformation:

1.  **Part 1**: The original 12 notes.
2.  **Part 2**: The 12 notes in reverse order.
3.  **Part 3**: An intervallic inversion of the original sequence.
4.  **Part 4**: A reversed version of the intervallic inversion.

These four parts are combined into a single 48-note sequence.

**Usage:**
```bash
python midi_transform.py chromatic_random.mid
```

**Output:**
- `chromatic_random_transformed.mid`: A MIDI file containing the full 48-note transformed sequence.

---

### Step 3: Create Melodic Variations

Finally, use `create_melody.py` to generate rhythmic variations from the 48-note sequence. This script will produce three different versions, each with unique, randomly assigned note durations, dotted notes, and rests.

**Usage:**
```bash
python create_melody.py chromatic_random_transformed.mid
```

**Outputs:**
For each of the 3 variations (e.g., `v1`, `v2`, `v3`), the script generates:
- **`.mid` file**: A MIDI file that can be played in any DAW or MIDI player.
  - `chromatic_random_transformed_melody_v1.mid`
  - `chromatic_random_transformed_melody_v2.mid`
  - `chromatic_random_transformed_melody_v3.mid`
- **`.musicxml` file**: A MusicXML file that can be opened in notation software like MuseScore or Sibelius to see the sheet music.
  - `chromatic_random_transformed_melody_v1.musicxml`
  - `chromatic_random_transformed_melody_v2.musicxml`
  - `chromatic_random_transformed_melody_v3.musicxml`
- **`.csv` file**: A CSV file detailing each musical event (note or rest), its duration in ticks, and its name in English and Spanish.
  - `chromatic_random_transformed_melody_v1.csv`
  - `chromatic_random_transformed_melody_v2.csv`
  - `chromatic_random_transformed_melody_v3.csv`

## Script Details

### `create_chromatic_midi.py`
- **Function**: Creates a MIDI file with the 12 chromatic notes from C1 (MIDI note 24) to B1 (MIDI note 35) in a random, non-repeating order.
- **Notes**: Each note has a fixed velocity and duration (quarter note).

### `midi_transform.py`
- **Function**: Reads the first 12 notes from a MIDI file and applies a series of structural transformations to generate a 48-note sequence.

### `create_melody.py`
- **Function**: Reads all notes from a MIDI file and generates melodic variations by randomizing rhythms.
- **Random Durations**: 1/32, 1/16, 1/8, 1/4, 1/2, and whole note.
- **Random Modifiers**:
  - **Normal**: The note is played with its assigned duration.
  - **Dotted**: The note duration is extended by 50%.
  - **Silence**: A rest is inserted, and the current note is "held" to be used in the next musical event.

