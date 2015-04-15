# coding: utf-8

from musicut import Note

__all__ = ['Key', 'CIRCLE_OF_FIFTHS']

ALL_NOTES = (
    (Note('A'), None),
    (Note('A', Note.SHARP), Note('B', Note.FLAT)),
    (Note('B'), Note('C', Note.FLAT)),
    (Note('C'), Note('B', Note.SHARP)),
    (Note('C', Note.SHARP), Note('D', Note.FLAT)),
    (Note('D'), None),
    (Note('D', Note.SHARP), Note('E', Note.FLAT)),
    (Note('E'), Note('F', Note.FLAT)),
    (Note('F'), Note('E', Note.SHARP)),
    (Note('F', Note.SHARP), Note('G', Note.FLAT)),
    (Note('G'), None),
    (Note('G', Note.SHARP), Note('A', Note.FLAT)),
)

# These are all of the keys that don't require double sharps/flats, which we
# don't support
CIRCLE_OF_FIFTHS = (
    Note('G', Note.FLAT),
    Note('D', Note.FLAT),
    Note('A', Note.FLAT),
    Note('E', Note.FLAT),
    Note('B', Note.FLAT),
    Note('F'),
    Note('C'),
    Note('G'),
    Note('D'),
    Note('A'),
    Note('E'),
    Note('B'),
    Note('F', Note.SHARP),
    Note('C', Note.SHARP),
)

# Map from a note to the index in the ALL_NOTES tuple
ALL_NOTES_INDEX = {}
for i, (l, r) in enumerate(ALL_NOTES):
    ALL_NOTES_INDEX[l] = ALL_NOTES_INDEX[r] = i

MAJOR = 'maj'
MINOR = 'min'

# Maps a major interval to the degree.  There are two entries for each
# interval, one for each key disposition (sharp or flat).
INTERVALS_TO_DEGREE = {
    MAJOR: {
        0: { k: (1, None) for k in [Note.SHARP, Note.FLAT] },
        1: { Note.FLAT: (2, Note.FLAT), Note.SHARP: (1, Note.SHARP) },
        2: { k: (2, None) for k in [Note.SHARP, Note.FLAT] },
        3: { Note.FLAT: (3, Note.FLAT), Note.SHARP: (2, Note.SHARP) },
        4: { k: (3, None) for k in [Note.SHARP, Note.FLAT] },
        5: { k: (4, None) for k in [Note.SHARP, Note.FLAT] },
        6: { Note.FLAT: (5, Note.FLAT), Note.SHARP: (4, Note.SHARP) },
        7: { k: (5, None) for k in [Note.SHARP, Note.FLAT] },
        8: { Note.FLAT: (6, Note.FLAT), Note.SHARP: (5, Note.SHARP) },
        9: { k: (6, None) for k in [Note.SHARP, Note.FLAT] },
        10: { Note.FLAT: (7, Note.FLAT), Note.SHARP: (6, Note.SHARP) },
        11: { k: (7, None) for k in [Note.SHARP, Note.FLAT] },
    },
}
INTERVALS_TO_DEGREE[MINOR] = { i: { k: ((((d+2) % 7) or 7), v)
                                   for k, (d,v) in INTERVALS_TO_DEGREE[MAJOR][(i-3) % 12].items() }
                              for i in range(0, 12) }

DEGREES_TO_INTERVAL = { key_type: { d: i for i,m in itd.items() for (k, d) in m.items() }
                        for key_type, itd in INTERVALS_TO_DEGREE.items() }

NOTE_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

class Key(object):
    MAJOR = MAJOR
    MINOR = MINOR

    def __init__(self, tonic, key_type=MAJOR):
        if tonic not in CIRCLE_OF_FIFTHS:
            raise ValueError("Key not supported: %s" % (tonic,))

        self.tonic = tonic
        self.key_type = key_type
        self._tonic_index = ALL_NOTES_INDEX[self.tonic]

        if CIRCLE_OF_FIFTHS.index(tonic) < CIRCLE_OF_FIFTHS.index(Note('C')):
            self._disposition = Note.FLAT
        else:
            self._disposition = Note.SHARP

    @classmethod
    def from_key_name(cls, key_name):
        """
        Creates a Key class corresponding to the given string name.  E.g. 'C'
        returns the key of C, 'Eb' returns the key of Eb, 'F#m' returns the
        key of F# minor.
        """
        tonic_mod = None
        key_type = cls.MAJOR
        if key_name[-1] == 'm':
            key_type = cls.MINOR
            key_name = key_name[:-1]
        if key_name[-1] == 'b':
            tonic_mod = Note.FLAT
        elif key_name[-1] == '#':
            tonic_mod = Note.SHARP

        return cls(Note(key_name[0], tonic_mod), key_type)

    def letter_for_degree(self, degree):
        letter_idx = (NOTE_LETTERS.index(self.tonic.letter) + degree -1) % len(NOTE_LETTERS)
        return NOTE_LETTERS[letter_idx]

    def note_for_interval(self, interval):
        itd = INTERVALS_TO_DEGREE[self.key_type][interval]
        degree, modifier = itd[self._disposition]
        return self.note_for_degree(degree, modifier)

    def _valid_notes_for_interval(self, interval):
        start_idx = ALL_NOTES_INDEX[self.tonic]
        notes_index = (start_idx + interval) % len(ALL_NOTES)
        return ALL_NOTES[notes_index]

    def note_for_degree(self, degree, modifier=None):
        dmap = DEGREES_TO_INTERVAL[self.key_type]
        interval = dmap[(degree, modifier)]
        notes = self._valid_notes_for_interval(interval)
        letter = self.letter_for_degree(degree)

        if notes[1] is None or notes[1].letter != letter:
            return notes[0]
        else:
            return notes[1]

    def interval_for_note(self, note):
        return (ALL_NOTES_INDEX[note] - self._tonic_index) % len(ALL_NOTES)

    def degree_for_note(self, note):
        itd = INTERVALS_TO_DEGREE[self.key_type]
        interval = self.interval_for_note(note)
        return itd[interval][note.modifier or Note.FLAT]

    def __repr__(self):
        return 'Key: %s' % (unicode(self.tonic),)


#class Transposer(object):
    #def 
