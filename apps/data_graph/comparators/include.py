from .icomparator import IComparator


class Include(IComparator):

    title = "Содержит"
    name = "include"

    @staticmethod
    def compare(first, second) -> bool:
        if isinstance(first, list):
            first = ' '.join(first)
        else:
            first = str(first)
        if isinstance(second, list):
            second = ' '.join(second)
        else:
            second = str(second)

        if first in second or second in first:
            return True
        else:
            return False
