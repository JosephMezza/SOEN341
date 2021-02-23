import pytest
from calc import add


class Test_Add:

    def test_add(self):
        addTest = add('Travis')
        assert addTest == 'Hello Travis'