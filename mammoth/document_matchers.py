import collections

import cobble


def paragraph(style_id=None, style_name=None, numbering=None):
    return ParagraphMatcher(style_id, style_name, numbering)


ParagraphMatcher = collections.namedtuple("ParagraphMatcher", ["style_id", "style_name", "numbering"])
ParagraphMatcher.element_type = "paragraph"


def run(style_id=None, style_name=None):
    return RunMatcher(style_id, style_name)


RunMatcher = collections.namedtuple("RunMatcher", ["style_id", "style_name"])
RunMatcher.element_type = "run"


class bold(object):
    element_type = "bold"


class italic(object):
    element_type = "italic"


class underline(object):
    element_type = "underline"


class strikethrough(object):
    element_type = "strikethrough"


class small_caps(object):
    element_type = "small_caps"


class comment_reference(object):
    element_type = "comment_reference"


BreakMatcher = collections.namedtuple("BreakMatcher", ["break_type"])
BreakMatcher.element_type = "break"


line_break = BreakMatcher("line")
page_break = BreakMatcher("page")
column_break = BreakMatcher("column")


def safe_unicode(value, encoding='utf-8'):
    """ Converts a value to unicode, even if it is already a unicode string.
    """
    if isinstance(value, unicode):
        return value
    elif isinstance(value, basestring):
        try:
            value = unicode(value, encoding)
        except (UnicodeDecodeError):
            value = value.decode('utf-8', 'replace')
    return value


def equal_to(value):
    return StringMatcher(_operator_equal_to, value)


def _operator_equal_to(first, second):
    if isinstance(second, unicode):
        first = safe_unicode(first)
    return first.upper() == second.upper()


def starts_with(value):
    return StringMatcher(_operator_starts_with, value)


def _operator_starts_with(first, second):
    if isinstance(second, unicode):
        first = safe_unicode(first)
    return second.upper().startswith(first.upper())


@cobble.data
class StringMatcher(object):
    operator = cobble.field()
    value = cobble.field()

    def matches(self, other):
        return self.operator(self.value, other)
