#!/bin/env python3
# -*- coding: utf-8 -*-
from z3 import *
from presmondec import congruent, monadic_decomposable, monadic_decomposable_without_bound
from mondec import mondec
from utils import get_formula_variables


def test(phi, *decomposable_on, fast_version=False) -> bool:
    test_pass = True
    phi_vars = [v.unwrap() for v in get_formula_variables(phi)]

    if len(decomposable_on) == 0:
        # the formula is not decomposable
        for v in phi_vars:
            if monadic_decomposable(phi, v):
                print("❌ A non-decomposable formula %s has been considered "
                      "decomposable by monadic_decomposable() when decomposing on variable %s" % (phi, v))
                test_pass = False
            else:
                print("✔ monadic_decomposable(phi, %s) = False" % v)

            if monadic_decomposable_without_bound(phi, v):
                print("❌ A non-decomposable formula %s has been considered "
                      "decomposable by monadic_decomposable_without_bound() "
                      "when decomposing on variable %s" % (phi, v))
                test_pass = False
            else:
                print("✔ monadic_decomposable_without_bound(phi, %s) = False" % v)

        return test_pass

    for v in decomposable_on:
        if not monadic_decomposable(phi, v):
            print("❌ A decomposable formula %s has been considered "
                  "non-decomposable by monadic_decomposable() when decomposing on variable %s" % (phi, v))
            test_pass = False
        else:
            print("✔ monadic_decomposable(phi, %s) = True" % v)

        if fast_version:
            continue

        if not monadic_decomposable_without_bound(phi, v):
            print("❌ A decomposable formula %s has been considered "
                  "non-decomposable by monadic_decomposable_without_bound() "
                  "when decomposing on variable %s" % (phi, v))
            test_pass = False
        else:
            print("✔ monadic_decomposable_without_bound(phi, %s) = True" % v)

    print("Running the general purpose monadic decomposability checker...")
    print("--> it should terminate if there is no error")

    mondec(lambda v: phi, phi_vars)

    print("General purpose monadic decomposability checker terminated.")
    print("=" * 30)

    return test_pass


def print_test_start(i: int):
    print("==================== [TEST %d] ====================" % i)


def test_1() -> bool:
    x, y = Ints("x y")
    phi = And(x >= 0, y >= 0, x == y)
    return test(phi)


def test_2() -> bool:
    x, y = Ints("x y")
    phi = And(x >= 0, y >= 0, x <= y)
    return test(phi)


def test_3() -> bool:
    x, y = Ints("x y")
    phi = And(x >= 0, y >= 0, x >= y)
    return test(phi)


def test_4() -> bool:
    x, y, z = Ints("x y z")

    phi = And([
        x >= 0,
        y >= 0,
        z >= 0,
        x + 2 * y >= 5,
        z < 5,
        congruent(x, y, 2)
    ])

    return test(phi, x, y, z, fast_version=True)


def run_tests():

    tp = True

    print_test_start(1)
    tp = tp and test_1()
    print_test_start(2)
    tp = tp and test_2()
    print_test_start(3)
    tp = tp and test_3()
    print_test_start(4)
    tp = tp and test_4()

    print("Test result: %s" % "PASS" if tp else "FAIL")


if __name__ == "__main__":
    if "--help" in sys.argv[1:]:
        print("Usage: %s file.smt2" % sys.argv[0])
    elif not sys.argv[1:]:
        print("Default run_tests")
        run_tests()
    else:
        x = Int('x')
        smt = parse_smt2_file(sys.argv[1])
        phi = And([f for f in smt])
        phi_vars = [v.unwrap() for v in get_formula_variables(phi)]
        test(phi, *phi_vars)
