# -*- coding: utf-8 -*-
import sys
import imp


class StringImporter(object):
    """
    Use custom meta hook to import modules available as strings.
    Cp. PEP 302 http://www.python.org/dev/peps/pep-0302/#specification-part-2-registering-hooks
    """

    def __init__(self, fullname, contents):
        self.fullname = fullname
        self.contents = contents

    def load_module(self, fullname=""):
        if not fullname:
            fullname = self.fullname
        if fullname in sys.modules:
            return sys.modules[fullname]

        mod = sys.modules.setdefault(fullname, imp.new_module(fullname))
        mod.__file__ = "<%s>" % fullname
        mod.__loader__ = self
        code = compile(self.contents, mod.__file__, "exec")
        exec code in mod.__dict__
        return mod