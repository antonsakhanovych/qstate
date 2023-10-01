from qiskit import *
import operator
from qiskit.tools.visualization import plot_histogram
from music21.chord import Chord
from music21.duration import Duration
from music21.instrument import Instrument
from music21.note import Note, Rest
from music21.stream import Stream
from music21.tempo import MetronomeMark
from music21.volume import Volume
import pygame

def binaryToDecimal(binary):
    binary = int(binary)
    decimal, i = 0, 0
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return decimal
backend = BasicAer.get_backend('qasm_simulator')

def create_pattern(n_qubits):
    circuit = QuantumCircuit(n_qubits, n_qubits)
    for i in range(0, n_qubits):
        circuit.h(i)
    for i in range(0, n_qubits):
        circuit.measure(i, i)
    job = execute(circuit, backend=backend)
    result = job.result()
    value = result.get_counts()
    play_pattern = str(max(value.items(), key=operator.itemgetter(1))[0])
    return play_pattern

def choose_octave():
    bin_val = create_pattern(2)
    dec_val = binaryToDecimal(bin_val) + 2
    return str(dec_val)

def create_song():
    song = ''
    for _ in range(0, 10):
        song += create_pattern(7)
    print(song)
    return song

def create_melody(play_pattern, file_path):
    notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    stream1 = Stream()
    for i in range(0, len(play_pattern)):
        octave = choose_octave()
        if play_pattern[i] == '1':
            stream1.append(Note(notes[i % len(notes)] + octave, quarterLength=1))
    stream1.write('midi', fp=file_path)

def play_midi(midi_file):
    pygame.init()
    pygame.mixer.init()

    try:
        pygame.mixer.music.load(midi_file)
        print(f"Playing {midi_file}")
        pygame.mixer.music.play()

        # Wait for the MIDI to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(30)

    except pygame.error as e:
        print(e)
        print("Could not load or play the MIDI file.")

####################
play_seq = create_song()
input_path = 'input.mid'
create_melody(play_seq, input_path)
####################

play_midi(input_path)
