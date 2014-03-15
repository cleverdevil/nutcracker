import re

import six

if six.PY3:
    def native_to_unicode(n, encoding='ISO-8859-1'):
        """Return the given native string as a unicode string with the given encoding."""
        assert_native(n)
        # In Python 3, the native string type is unicode
        return n
else:
    def native_to_unicode(n, encoding='ISO-8859-1'):
        """Return the given native string as a unicode string with the given encoding."""
        assert_native(n)
        # In Python 2, the native string type is bytes.
        # First, check for the special encoding 'escape'. The test suite uses this
        # to signal that it wants to pass a string with embedded \uXXXX escapes,
        # but without having to prefix it with u'' for Python 2, but no prefix
        # for Python 3.
        if encoding == 'escape':
            return unicode(
                re.sub(r'\\u([0-9a-zA-Z]{4})',
                       lambda m: unichr(int(m.group(1), 16)),
                       n.decode('ISO-8859-1')))
        # Assume it's already in the given encoding, which for ISO-8859-1 is almost
        # always what was intended.
        return n.decode(encoding)


def assert_native(n):
    if not isinstance(n, six.binary_type):
        raise TypeError("n must be a native str (got %s)" % type(n).__name__)
