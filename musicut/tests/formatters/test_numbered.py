import pytest

from musicut import Key, Chord, Note
from musicut.formatters import NumberedFormatter

valid_notations = (
    (Chord(1), '1'),
    (Chord(7, modifier=Note.FLAT), 'b7'),
    (Chord(4), '4'),
    (Chord(7), '7'),
    (Chord(5, bass=7), '5/7'),
    (Chord(7, modifier=Note.FLAT, bass=2), 'b7/2'),
    (Chord(2, bass=4, bass_modifier=Note.SHARP), '2/#4'),
    (Chord(3, chord_type=Chord.MINOR), '-3'),
    (Chord(4, addition=2), '4add2'),
    (Chord(2, chord_type=Chord.MINOR, extension=7, extension_type=Chord.MINOR), '-27'),
    (Chord(5, extension=7, extension_type=Chord.DOMINANT), '57'),
    (Chord(5, extension=7, extension_type=Chord.DOMINANT, bass=7), '57/7'),
)
@pytest.mark.parametrize("chord,expected", valid_notations)
def test_keyed_formatter(chord, expected):
    assert NumberedFormatter().notation_for_chord(chord) == expected

