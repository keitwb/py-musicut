import pytest

from musicut import Chord, Note
from musicut.parsers import numbered_parser

valid_chords = [
    ('1', Chord(degree=1, chord_type=Chord.MAJOR)),
    ('-6', Chord(degree=6, chord_type=Chord.MINOR)),
    ('-27', Chord(degree=2, chord_type=Chord.MINOR, extension=7,
                  extension_type=Chord.MINOR)),
    ('5sus4', Chord(degree=5, chord_type=Chord.MAJOR, sustained=True)),
    ('3sus', Chord(degree=3, chord_type=Chord.MAJOR, sustained=True)),
    ('4M7', Chord(degree=4, chord_type=Chord.MAJOR, extension_type=Chord.MAJOR,
                  extension=7)),
    ('1add4', Chord(degree=1, chord_type=Chord.MAJOR, addition=4)),
    ('15', Chord(degree=1, chord_type=Chord.FIVE)),
    ('17', Chord(degree=1, chord_type=Chord.MAJOR, extension=7,
                 extension_type=Chord.DOMINANT)),
    ('1/3', Chord(degree=1, chord_type=Chord.MAJOR, bass=3)),
    ('5/7', Chord(degree=5, chord_type=Chord.MAJOR, bass=7)),
    ('2/#4', Chord(degree=2, chord_type=Chord.MAJOR, bass=4,
                   bass_modifier=Note.SHARP)),
    ('5/b7', Chord(degree=5, chord_type=Chord.MAJOR, bass=7,
                   bass_modifier=Chord.FLAT)),
    ('b7', Chord(degree=7, modifier=Note.FLAT)),
    ('b6/1', Chord(degree=6, modifier=Note.FLAT, bass=1)),
    ('b7/b2', Chord(degree=7, modifier=Note.FLAT, bass=2, bass_modifier=Chord.FLAT)),
    ('1m7', Chord(degree=1, chord_type=Chord.MINOR, extension=7,
                  extension_type=Chord.MINOR)),
    pytest.mark.xfail(('1+', Chord(degree=1, chord_type=Chord.AUGMENTED))),
    pytest.mark.xfail(('1dim', Chord(degree=1, chord_type=Chord.DIMINISHED))),
]

@pytest.mark.parametrize("notation,expected", valid_chords)
def test_valid_chords(notation, expected):
    chord = numbered_parser.chord_from_notation(notation)

    assert chord.degree == expected.degree
    assert chord.modifier == expected.modifier
    assert chord.chord_type == expected.chord_type
    assert chord.addition == expected.addition
    assert chord.sustained == expected.sustained
    assert chord.extension == expected.extension
    assert chord.extension_type == expected.extension_type
    assert chord.bass == expected.bass
    assert chord.bass_modifier == expected.bass_modifier


invalid_chords = [
    '8',
    '0',
    'minor4',
    'n5',
    '5n',
    '1/9',
    '18',
]

@pytest.mark.parametrize("notation", invalid_chords)
def test_invalid_chords(notation):
    with pytest.raises(ValueError):
        numbered_parser.chord_from_notation(notation)
