from musicut import Chord

from .base import FormatterMixin

class KeyedFormatter(FormatterMixin):
    """
    Formats :class:`Chord`s into their string notation.

    This is essentially the inverse of :class:`KeyedParser`.
    """
    def __init__(self, key):
        self.key = key

    def notation_for_chord(self, chord):
        note = self.key.note_for_degree(chord.degree, chord.modifier)

        return "{letter}{mod}{chord_type}{extension}{sustained}{addition}{bass}".format(
            letter=note.letter,
            mod=self.MODIFIER_NOTATION.get(note.modifier, ''),
            chord_type=self.CHORD_TYPE_NOTATION.get(chord.chord_type, ''),
            extension=self.get_extension_notation(chord),
            sustained='sus4' if chord.sustained else '',
            addition='add%s' % chord.addition if chord.addition else '',
            bass=self.get_bass_notation(chord)
        )

    def get_bass_notation(self, chord):
        if chord.bass:
            note = self.key.note_for_degree(chord.bass, chord.bass_modifier)
            return '/{letter}{modifier}'.format(
                letter=note.letter,
                modifier=self.MODIFIER_NOTATION.get(note.modifier, ''))
        else:
            return ''

