# coding: utf-8

from collections import namedtuple

__all__ = ['Note', 'Chord']

class Note(namedtuple('Note', ['letter', 'modifier'])):
    """
    Represents an octave-independent note, e.g. A, C, G#, etc...
    """
    FLAT = 'b'
    SHARP = '#'

    def __new__(_cls, letter, modifier=None):
        return super(Note, _cls).__new__(_cls, letter, modifier)

    def __unicode__(self):
        return u'%s%s' % (self.letter, self.modifier or '')

    def __repr__(self):
        return self.__unicode__()


class Chord(object):
    """
    Represents a key-independent chord
    """
    MAJOR = 'M'
    MINOR = 'min'
    DOMINANT = 'dom'
    AUGMENTED = 'aug'
    DIMINISHED = 'dim'
    HALF_DIMINISHED = 'dim5'
    FIVE = '5'
    FLAT = 'b'

    CHORD_TYPES = [
        MAJOR,
        MINOR,
        AUGMENTED,
        DIMINISHED,
        FIVE,
    ]

    EXTENSION_TYPES = [
        MAJOR,
        MINOR,
        DOMINANT,
        DIMINISHED,
        HALF_DIMINISHED
    ]

    def __init__(self, degree, modifier=None, chord_type=MAJOR, sustained=False,
                 bass=None, bass_modifier=None, addition=None, extension=None,
                 extension_type=None):
        """
        :param int degree: The integer degree of the chord, 1-7.  To signify a
        flat chord, set the `flat` param to True.
        :param modifier: A modifier to the degree.  E.g. a flat 7 chord would
        have degree = 7 and modifier = :const:`Note.FLAT`.
        :param str chord_type: Whether the chord is major, minor, augmented,
         diminished, or a five chord.  Use the constants defined in
         :const:`CHORD_TYPES`.
        :param bool sustained: Set as True if the chord is a sustained 4th
        :param int bass: The degree of an alternate bass for this chord
        :param bass_modifier: Whether the degree specified in the *bass* param
         is sharp, flat, or neither.  Use :const:`Note.SHARP`,
         :const:`Note.FLAT` or None.
        :param addition: A degrees to add to the chord, e.g. 2 to signify the
         addition of the 2nd degree note (i.e. an add2 chord)
        :param int extension: The degree of any extensions (e.g. 7, 9, 11, etc..)
        :param str extension_type: An extension type defined on this class in
         :const:`EXTENSION_TYPES`
        """
        self.degree = degree
        self.modifier = modifier
        self.chord_type = chord_type
        self.sustained = sustained
        self.bass = bass
        self.bass_modifier = bass_modifier
        self.addition = addition
        self.extension = extension
        self.extension_type = extension_type

        if extension_type is None != extension is None:
            raise ValueError("Must set extension type and extension together")

    @property
    def degree(self):
        return self._degree

    @degree.setter
    def degree(self, value):
        if not 1 <= value <= 7:
            raise ValueError("Degree must be between 1 and 7")

        self._degree = value

    @property
    def chord_type(self):
        return self._chord_type

    @chord_type.setter
    def chord_type(self, value):
        if value is None or value not in self.CHORD_TYPES:
            raise ValueError("Invalid chord type received: %s" % value)

        self._chord_type = value

    @property
    def extension_type(self):
        return self._extension_type

    @extension_type.setter
    def extension_type(self, value):
        if value is not None and value not in self.EXTENSION_TYPES:
            raise ValueError("Invalid extension type received!")

        self._extension_type = value

    def __unicode__(self):
        return 'Chord: ' + str({
            'degree': self.degree,
            'modifier': self.modifier,
            'chord_type': self.chord_type,
            'extension_type': self.extension_type,
            'extension': self.extension,
            'addition': self.addition,
            'bass': self.bass,
            'bass_modifier': self.bass_modifier,
            'sustained': self.sustained})

    def __repr__(self):
        return self.__unicode__()
