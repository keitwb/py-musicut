from musicut import Chord

class ParserMixin(object):
    """
    This is a place to share parser code that is common to multiple parsers
    """
    def get_extension(self, groups, chord_type):
        ext = groups['extension']
        if ext is None or ext == '5':
            return None, None
        else:
            extension = int(ext)

        et = groups['extension_type']
        if et == 'M':
            etype = Chord.MAJOR
        elif et == 'dim':
            etype = Chord.DIMINISHED
        elif et == 'm' or chord_type == Chord.MINOR:
            etype = Chord.MINOR
        else:
            etype = Chord.DOMINANT

        return extension, etype

    def get_addition(self, groups):
        if groups['addition'] is not None:
            return int(groups['addition'])
        elif groups['extension'] == '2':
            return 2
        else:
            return None
