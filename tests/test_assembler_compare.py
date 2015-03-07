#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_assembler_compare
----------------------------------

Tests for `assembler_compare` module.
"""

import unittest
import os
from assembler_compare import assembler_compare


class TestAssembler_compare(unittest.TestCase):

    def setUp(self):
        self.conf = "tests/ac.txt"
        # need this for later functions
        self.k, self.data, self.outprefix, self.assemblers, self.other = assembler_compare.read_conf(self.conf)

    def test_read_conf(self):
        self.k, self.data, self.outprefix, self.assemblers, self.other = assembler_compare.read_conf(self.conf)
        self.assertEqual(self.k, "23")
        self.assertEqual(self.data, "tests/test-data.fastq")
        self.assertEqual(self.outprefix, "test")
        self.assertEqual(self.assemblers, [("1", "velvet")])
        self.assertEqual(self.other, [("1", "echo")])

    def test_velvet_assembly(self):
    	assembler_compare.velvet(self.k, self.outprefix, self.data)
    	self.assertTrue(os.path.isfile("test.velvet/contigs.fa"))

    def test_abyss(self):
    	assembler_compare.abyss(self.k, self.outprefix, self.data)
    	self.assertTrue(os.path.isfile("test-contigs.fa"))

    def tearDown(self):
        del self.conf

if __name__ == '__main__':
    unittest.main()
