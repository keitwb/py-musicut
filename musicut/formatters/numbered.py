from musicut import Chord

from .base import FormatterMixin

class NumberedFormatter(FormatterMixin):
    """
    Formats :class:`Chord`s into the standard numbered notation.

    This is the inverse of :class:`NumberedParser`.
    """
    def notation_for_chord(self, chord):
        if chord.chord_type == Chord.MINOR:
            minor = '-'
            chord_type = ''
        else:
            chord_type = self.CHORD_TYPE_NOTATION.get(chord.chord_type, '')
            minor = ''

        return "{minor}{mod}{degree}{chord_type}{extension}{sustained}{addition}{bass}".format(
            minor=minor,
            mod=self.MODIFIER_NOTATION.get(chord.modifier, ''),
            degree=chord.degree,
            chord_type=chord_type,
            extension=self.get_extension_notation(chord),
            sustained='sus4' if chord.sustained else '',
            addition='add%s' % chord.addition if chord.addition else '',
            bass=self.get_bass_notation(chord),
        )

    def get_bass_notation(self, chord):
        if chord.bass:
            return '/{modifier}{degree}'.format(
                degree=chord.bass,
                modifier=self.MODIFIER_NOTATION.get(chord.bass_modifier, ''))
        else:
            return ''

