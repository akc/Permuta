import unittest
from permuta import MeshPattern, Permutation, Permutations
import random

class TestPermutation(unittest.TestCase):

    def test_init(self):
        with self.assertRaises(AssertionError): Permutation([1,2,2], check=True)
        with self.assertRaises(AssertionError): Permutation([2,1,2], check=True)
        with self.assertRaises(AssertionError): Permutation([1,1], check=True)
        with self.assertRaises(AssertionError): Permutation([2], check=True)
        with self.assertRaises(AssertionError): Permutation(set([1,2,3]), check=True)
        with self.assertRaises(AssertionError): Permutation(5, check=True)
        with self.assertRaises(AssertionError): Permutation(None, check=True)
        Permutation([], check=True)
        Permutation([1], check=True)
        Permutation([4,1,3,2], check=True)

    def test_contained_in(self):
        def generate_contained(n,perm):
            for i in range(len(perm),n):
                r = random.randint(1,len(perm)+1)
                for i in range(len(perm)):
                    if perm[i] >= r:
                        perm[i] += 1
                x = random.randint(0,len(perm))
                perm = perm[:x] + [r] + perm[x:]
            return Permutation(perm)

        self.assertTrue(Permutation([4,8,1,9,2,7,6,3,5]).contained_in(Permutation([4,8,1,9,2,7,6,3,5])))
        self.assertTrue(Permutation([]).contained_in(Permutation([])))
        self.assertTrue(Permutation([]).contained_in(Permutation([4,8,1,9,2,7,6,3,5])))
        self.assertTrue(Permutation([1]).contained_in(Permutation([1])))
        self.assertFalse(Permutation([8,4,1,9,2,7,6,3,5]).contained_in(Permutation([4,8,1,9,2,7,6,3,5])))

        for i in range(100):
            n = random.randint(0, 4)
            patt = Permutations(n).random_element()
            self.assertTrue(patt.contained_in(generate_contained(random.randint(n, 8), patt.perm)))

        self.assertFalse(Permutation([1]).contained_in(Permutation([])))
        self.assertFalse(Permutation([1,2]).contained_in(Permutation([])))
        self.assertFalse(Permutation([1,2]).contained_in(Permutation([1])))
        self.assertFalse(Permutation([2, 1]).contained_in(Permutation([1, 2])))
        self.assertFalse(Permutation([1,2,3]).contained_in(Permutation([1,2])))
        self.assertFalse(Permutation([2, 1, 3]).contained_in(Permutation([1, 2, 4, 5, 3])))
        self.assertFalse(Permutation([1, 2, 3]).contained_in(Permutation([3, 2, 4, 1])))
        self.assertFalse(Permutation([3, 2, 4, 1]).contained_in(Permutation([3, 1, 4, 2])))
        self.assertFalse(Permutation([1, 3, 2]).contained_in(Permutation([3, 1, 2, 4])))
        self.assertFalse(Permutation([3, 1, 2, 4]).contained_in(Permutation([6, 4, 3, 8, 2, 1, 7, 5])))
        self.assertFalse(Permutation([1, 2, 3, 4]).contained_in(Permutation([5, 8, 6, 2, 7, 3, 4, 1])))

    def test_inverse(self):
        for i in range(10):
            self.assertEqual(Permutation(range(1,i)), Permutation(range(1,i)).inverse())
        self.assertEqual(Permutation([3,2,4,1]), Permutation([4,2,1,3]).inverse())
        self.assertEqual(Permutation([5,4,2,7,6,8,9,1,3]), Permutation([8,3,9,2,1,5,4,6,7]).inverse())

    def test_rotate_right(self):
        for i in range(10):
            self.assertEqual(Permutation(range(i-1,0,-1)), Permutation(range(1,i)).rotate_right())
        self.assertEqual(Permutation([3,2,4,5,1,6,7]), Permutation([7,6,4,3,1,2,5]).rotate_right())
        self.assertEqual(Permutation([5,6,4,2,8,1,3,7]), Permutation([5,8,2,1,3,7,4,6]).rotate_right())

    def test_reverse(self):
        self.assertEqual(Permutation([6,3,4,1,5,7,2]), Permutation([2,7,5,1,4,3,6]).reverse())
        self.assertEqual(Permutation([8,2,1,3,5,7,4,6]), Permutation([6,4,7,5,3,1,2,8]).reverse())

    def test_complement(self):
        self.assertEqual(Permutation([7,5,3,4,2,1,6]), Permutation([1,3,5,4,6,7,2]).complement())
        self.assertEqual(Permutation([3,6,7,4,8,5,1,2]), Permutation([6,3,2,5,1,4,8,7]).complement())

    def test_flip_antidiagonal(self):
        for i in range(100):
            perm = Permutations(random.randint(0,20)).random_element()
            self.assertEqual(perm.reverse().complement().inverse(), perm.flip_antidiagonal())

    def test_to_standard(self):
        def gen(perm):
            res = list(perm.perm)
            add = 0
            for i in perm.inverse():
                add += random.randint(0,10)
                res[i-1] += add
            return Permutation(res)

        for i in range(100):
            perm = Permutations(random.randint(0,20)).random_element()
            self.assertEqual(perm, Permutation.to_standard(perm))
            self.assertEqual(perm, Permutation.to_standard(gen(perm)))

    def test_call(self):
        for i in range(100):
            n = random.randint(0,20)
            lst = [ random.randint(0,10000) for i in range(n) ]
            perm = Permutations(n).random_element()
            res = perm(lst)
            for j,k in enumerate(perm.inverse()):
                self.assertEqual(lst[j], res[k-1])

    def test_eq(self):
        self.assertTrue(Permutation([]) == Permutation([]))
        self.assertTrue(Permutation([1]) == Permutation([1]))
        self.assertTrue(Permutation([]) != Permutation([1]))
        self.assertTrue(Permutation([1]) != Permutation([]))
        self.assertFalse(Permutation([]) != Permutation([]))
        self.assertFalse(Permutation([1]) != Permutation([1]))
        self.assertFalse(Permutation([]) == Permutation([1]))
        self.assertFalse(Permutation([1]) == Permutation([]))
        for i in range(100):
            a = Permutations(random.randint(0,10)).random_element()
            b = Permutation(list(a.perm))
            c = Permutations(random.randint(0,10)).random_element()
            if a.perm == c.perm:
                continue
            self.assertTrue(a == b)
            self.assertTrue(a != c)
            self.assertTrue(b == a)
            self.assertTrue(c != a)
