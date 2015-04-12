import pytest

from musicut import Chord, Note, Key
from musicut.parsers import KeyedParser

valid_chords = {
    ('A', 'A', Chord(degree=1, chord_type=Chord.MAJOR)),
    ('Em', 'G', Chord(degree=6, chord_type=Chord.MINOR)),
    ('Gm7', 'F', Chord(degree=2, chord_type=Chord.MINOR, extension=7,
                  extension_type=Chord.MINOR)),
    ('Fsus4', 'Bb', Chord(degree=5, chord_type=Chord.MAJOR, sustained=True)),
    ('G#sus', 'E', Chord(degree=3, chord_type=Chord.MAJOR, sustained=True)),
    ('EM7', 'B', Chord(degree=4, chord_type=Chord.MAJOR, extension_type=Chord.MAJOR,
                  extension=7)),
    ('Abadd4', 'Ab', Chord(degree=1, chord_type=Chord.MAJOR, addition=4)),
    ('D5', 'D', Chord(degree=1, chord_type=Chord.FIVE)),
    ('A7', 'A', Chord(degree=1, chord_type=Chord.MAJOR, extension=7,
                 extension_type=Chord.DOMINANT)),
    ('Ab7', 'Ab', Chord(degree=1, chord_type=Chord.MAJOR, extension=7,
                 extension_type=Chord.DOMINANT)),
    ('Db/F', 'Db', Chord(degree=1, chord_type=Chord.MAJOR, bass=3)),
    ('D/F#', 'G', Chord(degree=5, chord_type=Chord.MAJOR, bass=7)),
    ('F#/A#', 'E', Chord(degree=2, chord_type=Chord.MAJOR, bass=4,
                   bass_modifier=Note.SHARP)),
    ('Eb/Gb', 'Ab', Chord(degree=5, chord_type=Chord.MAJOR, bass=7,
                   bass_modifier=Chord.FLAT)),
    ('Bb', 'C', Chord(degree=7, modifier=Note.FLAT)),
    ('Cb/Eb', 'Eb', Chord(degree=6, modifier=Note.FLAT, bass=1)),
    ('Db/E', 'Eb', Chord(degree=7, modifier=Note.FLAT, bass=2, bass_modifier=Chord.FLAT)),
    ('Am7', 'A', Chord(degree=1, chord_type=Chord.MINOR, extension=7,
                  extension_type=Chord.MINOR)),
    ('Cb', 'F', Chord(degree=5, chord_type=Chord.MAJOR, modifier=Note.FLAT)),
    ('Gm', 'C', Chord(degree=5, chord_type=Chord.MINOR)),
    ('Am', 'Am', Chord(degree=1, chord_type=Chord.MINOR)),
    ('C', 'Am', Chord(degree=3, chord_type=Chord.MAJOR)),
    ('G#', 'Am', Chord(degree=7, chord_type=Chord.MAJOR, modifier=Note.SHARP)),
    ('Ab', 'Am', Chord(degree=1, chord_type=Chord.MAJOR, modifier=Note.FLAT)),
}


@pytest.mark.parametrize("notation,key_name,expected", valid_chords)
def test_valid_chords(notation, key_name, expected):
    key = Key.from_key_name(key_name)

    parser = KeyedParser(key)
    chord = parser.chord_from_notation(notation)

    assert chord.degree == expected.degree
    assert chord.modifier == expected.modifier
    assert chord.chord_type == expected.chord_type
    assert chord.addition == expected.addition
    assert chord.sustained == expected.sustained
    assert chord.extension == expected.extension
    assert chord.extension_type == expected.extension_type
    assert chord.bass == expected.bass
    assert chord.bass_modifier == expected.bass_modifier


invalid_chords = (
    ('H', 'C'),
    ('C/H', 'D'),
    ('1', 'Eb'),
    ('Ebad7', 'A'),
    ('Eadd14', 'C'),
)

@pytest.mark.parametrize("notation,key_name", invalid_chords)
def test_invalid_chords(notation, key_name):
    parser = KeyedParser(Key.from_key_name(key_name))
    with pytest.raises(ValueError):
        parser.chord_from_notation(notation)
