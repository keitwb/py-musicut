import pytest

from musicut import Key, Chord, Note
from musicut.formatters import KeyedFormatter

valid_notations = (
    (Chord(1), 'C', 'C'),
    (Chord(7, modifier=Note.FLAT), 'E', 'D'),
    (Chord(4), 'F', 'Bb'),
    (Chord(7), 'F', 'E'),
    (Chord(5, bass=7), 'G', 'D/F#'),
    (Chord(7, modifier=Note.FLAT, bass=2), 'Eb', 'Db/F'),
    (Chord(2, bass=4, bass_modifier=Note.SHARP), 'G', 'A/C#'),
    (Chord(3), 'C#', 'E#'),
    (Chord(4, addition=2), 'C', 'Fadd2'),
    (Chord(6, chord_type=Chord.MINOR), 'A', 'F#m'),
    (Chord(5, sustained=True), 'C#', 'G#sus4'),
    (Chord(5, extension=7, extension_type=Chord.DOMINANT), 'D', 'A7'),
    (Chord(2, chord_type=Chord.MINOR, extension=7, extension_type=Chord.MINOR),
        'A', 'Bm7')
)
@pytest.mark.parametrize("chord,key_name,expected", valid_notations)
def test_keyed_formatter(chord, key_name, expected):
    key = Key.from_key_name(key_name)
    assert KeyedFormatter(key).notation_for_chord(chord) == expected

