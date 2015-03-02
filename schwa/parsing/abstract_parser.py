import abc


class AbstractParser:
    __metaclass__ = abc.ABCMeta

    @abc.abstractstaticmethod
    def parse(source):
        """ Parses all the components till method"""

    @abc.abstractstaticmethod
    def diff(source_a, source_b):
        """ Parses all the components till method"""