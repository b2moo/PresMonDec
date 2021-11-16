from z3 import *
from presmondec import congruent, monadic_decomposable, monadic_decomposable_without_bound
from mondec import mondec
from utils import get_formula_variables


def test(phi, *decomposable_on):
    phi_vars = [v.unwrap() for v in get_formula_variables(phi)]

    if len(decomposable_on) == 0:
        # the formula is not decomposable
        for v in phi_vars:
            if monadic_decomposable(phi, v):
                print("❌ A non-decomposable formula %s has been considered "
                      "decomposable by monadic_decomposable() when decomposing on variable %s" % (phi, v))
            else:
                print("✔ monadic_decomposable(phi, %s) = False" % v)

            if monadic_decomposable_without_bound(phi, v):
                print("❌ A non-decomposable formula %s has been considered "
                      "decomposable by monadic_decomposable_without_bound() "
                      "when decomposing on variable %s" % (phi, v))
            else:
                print("✔ monadic_decomposable_without_bound(phi, %s) = False" % v)

        return

    for v in decomposable_on:
        if not monadic_decomposable(phi, v):
            print("A decomposable formula %s has been considered "
                  "non-decomposable by monadic_decomposable() when decomposing on variable %s" % (phi, v))
        else:
            print("✔ monadic_decomposable(phi, %s) = True" % v)

        if not monadic_decomposable_without_bound(phi, v):
            print("A decomposable formula %s has been considered "
                  "non-decomposable by monadic_decomposable_without_bound() "
                  "when decomposing on variable %s" % (phi, v))
        else:
            print("✔ monadic_decomposable_without_bound(phi, %s) = True" % v)

    print("Running the general purpose monadic decomposability checker...")
    print("--> it should terminate if there is no error")

    R = lambda v: phi

    mondec(R, phi_vars)

    print("General purpose monadic decomposability checker terminated.")
    print("=" * 30)


def print_test_start(i: int):
    print("==================== [TEST %d] ====================" % i)


def test_1():
    x, y = Ints("x y")
    phi = And(x >= 0, y >= 0, x == y)
    test(phi)


def test_2():
    x, y = Ints("x y")
    phi = And(x >= 0, y >= 0, x <= y)
    test(phi)


def test_3():
    x, y = Ints("x y")
    phi = And(x >= 0, y >= 0, x >= y)
    test(phi)


def test_4():
    x, y, z = Ints("x y z")

    phi = And([
        x >= 0,
        y >= 0,
        z >= 0,
        x + 2 * y >= 5,
        z < 5,
        congruent(x, y, 2)
    ])

    test(phi, x, y, z)


def run_tests():
    print_test_start(1)
    test_1()
    print_test_start(2)
    test_2()
    print_test_start(3)
    test_3()
    print_test_start(4)
    test_4()


if __name__ == "__main__":
    run_tests()
