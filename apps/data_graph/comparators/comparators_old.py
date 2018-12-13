import sys

from fuzzywuzzy import fuzz, process

EQUAL = 'equal'
EQUAL_IGNORE_CASE = 'equal_ignore_case'
INCLUDE = 'include'
PARTIAL_RATIO = 'partial_ratio'
# https://pypi.python.org/pypi/abydos
# TODO add TRANSLIT_SIMILAR = 'translit_similar'  # https://pypi.python.org/pypi/PyICU/

COMPARATOR_CHOICES = (
    (EQUAL, 'equal'),
    (EQUAL_IGNORE_CASE, 'equal_ignore_case'),

    (INCLUDE, 'include'),
    (PARTIAL_RATIO, 'partial_ratio'),
)




def equal(val1="", val2=""):
    if (val1 == val2):
        return True
    else:
        return False


class Comparator(object):
    def equal(val1, val2):
        if isinstance(val1, list):
            v1 = ' '.join(val1)
        else:
            v1 = str(val1)
        if isinstance(val2, list):
            v2 = ' '.join(val2)
        else:
            v2 = str(val2)

        if v1 == v2:
            return True
        else:
            return False

    def equalIgnoreCase(val1="", val2=""):
        if isinstance(val1, list):
            v1 = ' '.join(val1)
        else:
            v1 = str(val1)
        if isinstance(val2, list):
            v2 = ' '.join(val2)
        else:
            v2 = str(val2)

        if v1.lower() == v2.lower():
            return True
        else:
            return False

    def include(val1, val2):
        if isinstance(val1, list):
            v1 = ' '.join(val1)
        else:
            v1 = str(val1)
        if isinstance(val2, list):
            v2 = ' '.join(val2)
        else:
            v2 = str(val2)

        if v1 in v2 or v2 in v1:
            return True
        else:
            return False

    # tmp = fuzz.ratio(left, right)
    # print(tmp, "ratio")
    #
    # tmp = fuzz.partial_ratio(left, right)
    # print(tmp, "partial_ratio")
    #
    # tmp = fuzz.partial_token_set_ratio(left, right)
    # print(tmp, "partial_token_set_ratio")
    #
    # tmp = fuzz.partial_token_sort_ratio(left, right)
    # print(tmp, "partial_token_sort_ratio")
    #
    # tmp = fuzz.token_set_ratio(left, right)
    # print(tmp, "token_set_ratio")
    #
    # tmp = fuzz.token_sort_ratio(left, right)
    # print(tmp, "token_sort_ratio")

    def partial_ratio(val1, val2):
        if isinstance(val1, list):
            v1 = ' '.join(val1)
        else:
            v1 = str(val1)
        if isinstance(val2, list):
            v2 = ' '.join(val2)
        else:
            v2 = str(val2)

        tmp = fuzz.partial_ratio(v1, v2)
        if tmp > 90:
            return True
        else:
            return False


def main(argv):
    try:
        # os.system("python " +argv[1]+" "+argv[2]+" "+argv[3])
        # mycode = "print('ss')"
        # res = exec("Comparator.equal(%s, %s)" % (argv[1], argv[2]))
        res = exec("equal(%s, %s)" % (argv[1], argv[2]))
        print(res)


    except Exception as err:
        print(err)


if __name__ == "__main__":
    main(sys.argv)
