# -*- coding: utf-8 -*-
"""
Tests

Usage:
pytest tests/

Coverage:
coverage run -m pytest . -x -v
coverage report --include=howard/* -m
"""

import logging as log
import os
import sys
import duckdb
import re
import Bio.bgzf as bgzf
import gzip
import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from unittest.mock import patch

from howard.objects.variants import Variants
from howard.commons import *
from howard.tools.tools import *


tests_folder = os.path.dirname(__file__)


def test_process():

    # Init files
    input_vcf = tests_folder + "/data/example.vcf.gz"
    output_vcf = "/tmp/output_file.tsv"
    config = {}
    param = "{}"
    annotations = tests_folder + "/data/annotations/nci60.parquet"
    calculations = "VARTYPE"
    prioritizations = tests_folder + "/data/prioritization_profiles.json"
    input_query = None

    # prepare arguments for the query function
    args = argparse.Namespace(
        input = input_vcf,
        output = output_vcf,
        config = config,
        param = param,
        annotations = annotations,
        calculations = calculations,
        prioritizations = prioritizations,
        query = input_query,
    )

    # Remove if output file exists
    remove_if_exists([output_vcf])

    # Query
    process(args)

    # read the contents of the actual output file
    with open(output_vcf, 'r') as f:
        result_output_nb_lines = 0
        result_output_nb_variants = 0
        for line in f:
            result_output_nb_lines += 1
            if not line.startswith("#"):
                result_output_nb_variants += 1

    # Expected result
    expected_result_nb_lines = 68
    expected_result_nb_variants = 7

    # Compare
    assert result_output_nb_lines == expected_result_nb_lines
    assert result_output_nb_variants == expected_result_nb_variants


def test_process_with_param_file():

    # Init files
    input_vcf = tests_folder + "/data/example.vcf.gz"
    output_vcf = "/tmp/output_file.tsv"
    config = {}
    param = tests_folder +  "/data/param.snpeff_hgvs.json"
    annotations = tests_folder + "/data/annotations/nci60.parquet"
    calculations = "VARTYPE"
    prioritizations = tests_folder + "/data/prioritization_profiles.json"
    input_query = None

    # prepare arguments for the query function
    args = argparse.Namespace(
        input = input_vcf,
        output = output_vcf,
        config = config,
        param = param,
        annotations = annotations,
        calculations = calculations,
        prioritizations = prioritizations,
        query = input_query,
    )

    # Remove if output file exists
    remove_if_exists([output_vcf])

    # Query
    process(args)

    # read the contents of the actual output file
    with open(output_vcf, 'r') as f:
        result_output_nb_lines = 0
        result_output_nb_variants = 0
        for line in f:
            result_output_nb_lines += 1
            if not line.startswith("#"):
                result_output_nb_variants += 1

    # Expected result
    expected_result_nb_lines = 78
    expected_result_nb_variants = 7

    # Compare
    assert result_output_nb_lines == expected_result_nb_lines
    assert result_output_nb_variants == expected_result_nb_variants


def test_process_with_query():

    # Init files
    input_vcf = tests_folder + "/data/example.vcf.gz"
    output_vcf = "/tmp/output_file.tsv"
    config = {}
    param = "{}"
    annotations = tests_folder + "/data/annotations/nci60.parquet"
    calculations = "VARTYPE"
    prioritizations = tests_folder + "/data/prioritization_profiles.json"
    input_query = "SELECT count(*) AS '#count' FROM variants WHERE INFO LIKE '%VARTYPE%' AND INFO LIKE '%PZScore%'"

    # prepare arguments for the query function
    args = argparse.Namespace(
        input = input_vcf,
        output = output_vcf,
        config = config,
        param = param,
        annotations = annotations,
        calculations = calculations,
        prioritizations = prioritizations,
        query = input_query,
    )

    # Remove if output file exists
    remove_if_exists([output_vcf])

    # Query
    process(args)

    # read the contents of the actual output file
    with open(output_vcf, 'r') as f:
        result_output_nb_lines = 0
        result_output_nb_variants = 0
        result_lines = []
        for line in f:
            result_output_nb_lines += 1
            if not line.startswith("#"):
                result_output_nb_variants += 1
                result_lines.append(line.strip())

    # Expected result
    expected_result_nb_lines = 62
    expected_result_nb_variants = 1
    expected_result_lines = ["7"]

    # Compare
    assert result_output_nb_lines == expected_result_nb_lines
    assert result_output_nb_variants == expected_result_nb_variants
    assert result_lines == expected_result_lines


