from musicut import Note, Chord

class FormatterMixin(object):
    CHORD_TYPE_NOTATION = {
        Chord.MAJOR: '',
        Chord.MINOR: 'm',
        Chord.AUGMENTED: '+',
        Chord.DIMINISHED: 'dim',
        Chord.FIVE: '5',
    }

    MODIFIER_NOTATION = {
        Note.FLAT: 'b',
        Note.SHARP: '#',
    }

    EXTENSION_TYPE_NOTATION = {
        Chord.MAJOR: 'M',
    }

    def get_extension_notation(self, chord):
        if chord.extension:
            if chord.extension_type == Chord.MAJOR:
                extype_notation = 'M'
            else:
                extype_notation = ''

            return '{type}{ext}'.format(
                ext=chord.extension,
                type=self.EXTENSION_TYPE_NOTATION.get(chord.extension_type, ''))
        else:
            return ''
