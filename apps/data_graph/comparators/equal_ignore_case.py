from .icomparator import IComparator


class EqualIgnoreCase(IComparator):

    title = "Равно без учета регистра"
    name = "equal_ignore_case"

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

        if first.lower() == second.lower():
            return True
        else:
            return False
