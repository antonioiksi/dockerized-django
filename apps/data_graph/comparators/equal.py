from .icomparator import IComparator


class Equal(IComparator):

    title = "Равно"
    name = "equal"

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

        if first == second:
            return True
        else:
            return False
