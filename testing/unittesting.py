#!/usr/bin/env python
# coding=utf-8

import functest
import unittest

class TestAdd(unittest.TestCase):
    """
    Test the add function from the functest library
    """

    def test_add_integers(self):
        """
        Test that the addition of two integers
        """
        result = functest.add(1, 2)
        self.assertEqual(result, 3)

    def test_add_strings(self):
        """
        Test the addition of two strings return the two string as one
        concatenated string
        """
        result = functest.add('abc', 'def')
        self.assertEqual(result, 'abcdef')
    
    @unittest.skip('Skip this test')
    # skip, skipUnless, skipIf
    def test_add_floats(self):
        """
        Test the addition of two floats
        """
        result = functest.add(1.5, 3.1)    
        self.assertEqual(result, 4.6)         

def my_suite():
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    suite.addTest(unittest.makeSuite(TestAdd))
    # suite.run(result)
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

if __name__ == '__main__':
    # unittest.main()
    my_suite()


