import pytest

from musicut import Note, Key

valid_key_mapping = (
    ('C', Key(Note('C'), Key.MAJOR)),
    ('Em', Key(Note('E'), Key.MINOR)),
    ('F#m', Key(Note('F', Note.SHARP), Key.MINOR)),
    ('C#', Key(Note('C', Note.SHARP), Key.MAJOR)),
)
@pytest.mark.parametrize("key_name,expected", valid_key_mapping)
def test_key_from_name(key_name, expected):
    assert Key.from_key_name(key_name).__dict__ == expected.__dict__

valid_degrees_for_keys = (
    (Note('C'), Key.MAJOR, Note('D'), 2, None),
    (Note('C'), Key.MAJOR, Note('G'), 5, None),
    (Note('C'), Key.MAJOR, Note('B', Note.FLAT), 7, Note.FLAT),
    (Note('B', Note.FLAT), Key.MAJOR, Note('B', Note.FLAT), 1, None),
    (Note('B', Note.FLAT), Key.MAJOR, Note('E', Note.FLAT), 4, None),
    (Note('F'), Key.MAJOR, Note('B', Note.FLAT), 4, None),
    (Note('F'), Key.MAJOR, Note('B'), 5, Note.FLAT),
    (Note('A'), Key.MINOR, Note('B', Note.FLAT), 2, Note.FLAT),
    (Note('E'), Key.MINOR, Note('G'), 3, None),
    (Note('E'), Key.MINOR, Note('D'), 7, None),
    (Note('C'), Key.MAJOR, Note('D', Note.SHARP), 2, Note.SHARP),
    (Note('C'), Key.MAJOR, Note('E', Note.FLAT), 3, Note.FLAT),
)
@pytest.mark.parametrize("tonic,key_type,note,degree,modifier", valid_degrees_for_keys)
def test_key_note_to_degree(tonic, key_type, note, degree, modifier):
    assert Key(tonic, key_type).degree_for_note(note) == (degree, modifier)

valid_notes_for_degree = (
    (1, None, 'C', Note('C')),
    (2, None, 'C', Note('D')),
    (7, None, 'C', Note('B')),
    (4, None, 'F', Note('B', Note.FLAT)),
    (7, None, 'F', Note('E')),
    (2, None, 'E', Note('F', Note.SHARP)),
    (7, Note.FLAT, 'F', Note('E', Note.FLAT)),
    (5, Note.SHARP, 'E', Note('B', Note.SHARP)),
    (6, Note.FLAT, 'E', Note('C')),
    (3, None, 'Am', Note('C')),
    (4, None, 'Am', Note('D')),
    (4, Note.SHARP, 'Am', Note('D', Note.SHARP)),
)
@pytest.mark.parametrize("degree,modifier,key_name,expected", valid_notes_for_degree)
def test_key_note_for_degree(degree, modifier, key_name, expected):
    key = Key.from_key_name(key_name)
    assert key.note_for_degree(degree, modifier) == expected
