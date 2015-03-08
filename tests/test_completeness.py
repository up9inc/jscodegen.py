import unittest as unittest
from syntax import Syntax
from jscodegen import CodeGenerator


def add_tests(generator):
    def class_decorator(cls):
        """Add tests to `cls` generated by `generator()`."""
        for f, token in generator():
            test = lambda self, i=token, f=f: f(self, i)
            test.__name__ = "test %s" % token.name
            setattr(cls, test.__name__, test)
        return cls
    return class_decorator


def _test_tokens():

    def t(self, to):
        c = CodeGenerator({})
        func_name = to.name.lower()
        try:
            getattr(c, func_name)
            self.assertTrue(True, func_name)
        except AttributeError:
            self.fail("Not implemented: %s" % func_name)

    for token in Syntax:
        yield t, token


class TestCase(unittest.TestCase):
    pass
TestCase = add_tests(_test_tokens)(TestCase)

if __name__=="__main__":
    unittest.main()