import re

from musicut import Chord, Note

from .base import ParserMixin


class KeyedParser(ParserMixin):
    """
    Handles chord notation that is already in a key (e.g. Csus4, Am7)
    """
    REGEX = re.compile(
        r"(?:(?P<note>[A-G])(?P<note_modifier>[b#])?)"
        r"(?P<chord_type>dim|m|min|\+)?"
        r"((?P<extension_type>M|dim|m)?(?P<extension>2|5|6|7|9|11))?"
        r"(?P<sustained>sus4?)?"
        r"(?:add(?P<addition>[246]))?"
        r"(?:/(?P<bass>[A-G])(?P<bass_modifier>[b#])?)?$")

    def __init__(self, key):
        self.key = key

    def chord_from_notation(self, notation):
        match = self.REGEX.match(notation)
        if match is None:
            raise ValueError("Notation was not understood: %s" % notation)

        groups = match.groupdict()

        degree, modifier = self.get_degree(groups)
        chord_type = self.get_chord_type(groups)
        sustained = groups['sustained'] is not None
        bass, bass_modifier = self.get_bass(groups)
        addition = self.get_addition(groups)
        extension, extension_type = self.get_extension(groups, chord_type)

        return Chord(
            degree=degree,
            modifier=modifier,
            chord_type=chord_type,
            sustained=sustained,
            bass=bass,
            bass_modifier=bass_modifier,
            addition=addition,
            extension=extension,
            extension_type=extension_type)

    def get_degree(self, groups):
        if groups['note_modifier'] == 'b':
            modifier = Note.FLAT
        elif groups['note_modifier'] == '#':
            modifier = Note.SHARP
        else:
            modifier = None

        note = Note(groups['note'], modifier)
        return self.key.degree_for_note(note)

    def get_chord_type(self, groups):
        ct = groups['chord_type']
        if groups['extension'] == '5':
            return Chord.FIVE
        elif ct is None:
            return Chord.MAJOR
        elif ct in ['m', 'min']:
            return Chord.MINOR
        elif ct == 'dim':
            return Chord.DIMINISHED
        elif ct == '+':
            return Chord.AUGMENTED

    def get_bass(self, groups):
        if groups['bass'] is None:
            return None, None

        mod = None
        if groups['bass_modifier'] == 'b':
            mod = Note.FLAT
        elif groups['bass_modifier'] == '#':
            mod = Note.SHARP

        note = Note(groups['bass'], mod)
        return self.key.degree_for_note(note)
