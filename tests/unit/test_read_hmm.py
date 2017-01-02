#!/usr/bin/env python
# coding: utf-8


"""
Unit tests read_hmm function of integron_finder
"""

import integron_finder
import pandas as pd
import unittest
import os
import pandas.util.testing as pdt
import argparse

class TestFunctions(unittest.TestCase):

    def setUp(self):
        """
        Define variables common to all tests
        """
        self.rep_name = "acba.007.p01.13"
        # Simulate argparse to get argument
        parser = argparse.ArgumentParser(description='Process some integers.')
        parser.add_argument("--gembase", help="gembase format", action="store_true")
        args = parser.parse_args([])
        integron_finder.args = args

    def test_read_empty(self):
        """
        Test that when there are no hits in the hmm result file, it returns an empty
        dataframe, without error.
        """
        infile = os.path.join("tests", "data", "fictive_results",
                              self.rep_name + "_intI-empty.res")
        df = integron_finder.read_hmm(self.rep_name, infile)
        exp = pd.DataFrame(columns=["Accession_number", "query_name", "ID_query", "ID_prot",
                                    "strand", "pos_beg", "pos_end", "evalue"])

        intcols = ["pos_beg", "pos_end", "strand"]
        floatcol = ["evalue"]
        exp[intcols] = exp[intcols].astype(int)
        exp[floatcol] = exp[floatcol].astype(float)
        pdt.assert_frame_equal(df, exp)

    def test_read_hmm(self):
        """
        Test that the hmm hits are well read
        """
        infile = os.path.join("tests", "data", "Results_Integron_Finder_" + self.rep_name,
                                 "other", self.rep_name + "_intI.res")
        df = integron_finder.read_hmm(self.rep_name, infile)
        exp = pd.DataFrame(data={"Accession_number": self.rep_name, "query_name": "intI_Cterm",
                                 "ID_query": "-", "ID_prot": "ACBA.007.P01_13_1", "strand": 1,
                                 "pos_beg": 55, "pos_end": 1014, "evalue": 1.9e-25},
                           index=[0])
        exp = exp[["Accession_number", "query_name", "ID_query", "ID_prot",
                   "strand", "pos_beg", "pos_end", "evalue"]]
        pdt.assert_frame_equal(df, exp)

    def test_read_hmm_gembase(self):
        """
        Test that the hmm hits are well read, when the gembase format is used (.prt file is
        provided, prodigal is not used to find the proteins).
        """
        parser = argparse.ArgumentParser(description='Process some integers.')
        parser.add_argument("--gembase", help="gembase format", action="store_true")
        args = parser.parse_args(["--gembase"])
        integron_finder.args = args
        infile = os.path.join("tests", "data", "fictive_results", self.rep_name +
                                 "_intI-gembase.res")
        df = integron_finder.read_hmm(self.rep_name, infile)
        exp = pd.DataFrame(data={"Accession_number": self.rep_name, "query_name": "intI_Cterm",
                                 "ID_query": "-", "ID_prot": "ACBA007p01a_000009", "strand": 1,
                                 "pos_beg": 55, "pos_end": 1014, "evalue": 1.9e-25},
                           index=[0])
        exp = exp[["Accession_number", "query_name", "ID_query", "ID_prot",
                   "strand", "pos_beg", "pos_end", "evalue"]]
        pdt.assert_frame_equal(df, exp)

    def test_read_hmm_evalue(self):
        """
        Test that the hmm hits are well read, and returned only if evalue is < to the
        given threshold.
        """
        infile = os.path.join("tests", "data", "Results_Integron_Finder_" + self.rep_name,
                                 "other", self.rep_name + "_intI.res")
        df1 = integron_finder.read_hmm(self.rep_name, infile, evalue=1.95e-25)
        exp1 = pd.DataFrame(data={"Accession_number": self.rep_name, "query_name": "intI_Cterm",
                                  "ID_query": "-", "ID_prot": "ACBA.007.P01_13_1", "strand": 1,
                                  "pos_beg": 55, "pos_end": 1014, "evalue": 1.9e-25},
                            index=[0])
        exp1 = exp1[["Accession_number", "query_name", "ID_query", "ID_prot",
                     "strand", "pos_beg", "pos_end", "evalue"]]
        pdt.assert_frame_equal(df1, exp1)
        df2 = integron_finder.read_hmm(self.rep_name, infile, evalue=1.9e-25)
        exp2 = pd.DataFrame(columns=["Accession_number", "query_name", "ID_query", "ID_prot",
                                     "strand", "pos_beg", "pos_end", "evalue"])

        intcols = ["pos_beg", "pos_end", "strand"]
        floatcol = ["evalue"]
        exp2[intcols] = exp2[intcols].astype(int)
        exp2[floatcol] = exp2[floatcol].astype(float)
        pdt.assert_frame_equal(df2, exp2)

    def test_read_hmm_cov(self):
        """
        Test that the hmm hits are well read, and returned only if coverage is > to the
        given threshold.
        """
        infile = os.path.join("tests", "data", "Results_Integron_Finder_" + self.rep_name,
                                 "other", self.rep_name + "_intI.res")
        df1 = integron_finder.read_hmm(self.rep_name, infile, coverage=0.945)
        exp1 = pd.DataFrame(data={"Accession_number": self.rep_name, "query_name": "intI_Cterm",
                                  "ID_query": "-", "ID_prot": "ACBA.007.P01_13_1", "strand": 1,
                                  "pos_beg": 55, "pos_end": 1014, "evalue": 1.9e-25},
                            index=[0])
        exp1 = exp1[["Accession_number", "query_name", "ID_query", "ID_prot",
                     "strand", "pos_beg", "pos_end", "evalue"]]
        pdt.assert_frame_equal(df1, exp1)
        df2 = integron_finder.read_hmm(self.rep_name, infile, coverage=0.95)
        exp2 = pd.DataFrame(columns=["Accession_number", "query_name", "ID_query", "ID_prot",
                                     "strand", "pos_beg", "pos_end", "evalue"])
        intcols = ["pos_beg", "pos_end", "strand"]
        floatcol = ["evalue"]
        exp2[intcols] = exp2[intcols].astype(int)
        exp2[floatcol] = exp2[floatcol].astype(float)
        pdt.assert_frame_equal(df2, exp2)

    # test various hits for same protein: keep best evalue

