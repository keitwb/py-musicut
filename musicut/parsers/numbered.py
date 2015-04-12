import re

from musicut import Chord, Note

from .base import ParserMixin

class NumberedParser(ParserMixin):
    """
    Handles the standard numbered notation (e.g. 1sus4, -67)
    """
    REGEX = re.compile(
        r"^(?P<minor>-)?"
        r"(?P<degree_modifier>[b#])?"
        r"(?P<degree>[1-7])"
        r"((?P<extension_type>M|dim|m)?(?P<extension>2|5|6|7|9|11))?"
        r"(?P<sustained>sus4?)?"
        r"(?:add(?P<addition>[246]))?"
        r"(?:/(?P<bass_modifier>[b#])?(?P<bass>[1-7]))?$")

    def chord_from_notation(self, notation):
        """
        :param str notation: The chord notation, e.g. '1M7', '-67', etc...
        """
        match = self.REGEX.match(notation)
        if match is None:
            raise ValueError("Notation was not understood: %s" % notation)

        groups = match.groupdict()

        chord_type = self.get_chord_type(groups)
        modifier = self.get_degree_modifier(groups)
        sustained = groups['sustained'] is not None
        bass, bass_modifier = self.get_bass(groups)
        addition = self.get_addition(groups)
        extension, extension_type = self.get_extension(groups, chord_type)

        return Chord(
            int(groups['degree']),
            modifier=modifier,
            chord_type=chord_type,
            sustained=sustained,
            bass=bass,
            bass_modifier=bass_modifier,
            addition=addition,
            extension=extension,
            extension_type=extension_type)

    def get_chord_type(self, groups):
        if groups['extension'] == '5':
            return Chord.FIVE
        elif groups['minor'] is not None:
            return Chord.MINOR
        elif groups['extension_type'] == 'm':
            return Chord.MINOR
        else:
            return Chord.MAJOR

    def get_degree_modifier(self, groups):
        if groups['degree_modifier'] == 'b':
            return Note.FLAT
        elif groups['degree_modifier'] == '#':
            return Note.SHARP
        else:
            return None

    def get_bass(self, groups):
        if groups['bass'] is not None:
            bass = int(groups['bass'])
        else:
            bass = None

        if groups['bass_modifier'] == 'b':
            modifier = Note.FLAT
        elif groups['bass_modifier'] == '#':
            modifier = Note.SHARP
        else:
            modifier = None

        return bass, modifier

numbered_parser = NumberedParser()
