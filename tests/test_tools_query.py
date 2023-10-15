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
from test_needed import *



def test_query():

    # Init files
    input_vcf = tests_data_folder + "/example.vcf.gz"
    output_vcf = "/tmp/output_file.tsv"
    config = {'threads': 4}

    query_list = {
        "SELECT count(*) AS '#count' FROM variants": {"nb_lines": 54, "nb_variants": 1},
        "SELECT * AS '#count' FROM variants": {"nb_lines": 60, "nb_variants": 7}
    }

    for explode_infos in [True, False]:

        for explode_infos_prefix in ["", "INFO/", "CUSTOM_"]:

            for explode_infos_fields in ['*', 'SIFT']:

                for input_query in query_list:

                    # Expected results
                    expected_results = query_list[input_query]

                    # prepare arguments for the query function
                    args = argparse.Namespace(
                        input = input_vcf,
                        output = output_vcf,
                        config = config,
                        query = input_query,
                        explode_infos = explode_infos,
                        explode_infos_prefix = explode_infos_prefix,
                        explode_infos_fields = explode_infos_fields,
                        include_header = True
                    )

                    # Remove if output file exists
                    remove_if_exists([output_vcf])

                    # Query
                    query(args)

                    # read the contents of the actual output file
                    with open(output_vcf, 'r') as f:
                        result_output_nb_lines = 0
                        result_output_nb_variants = 0
                        result_lines = []
                        for line in f:
                            if not result_output_nb_lines:
                                log.debug(line)
                            result_output_nb_lines += 1
                            if not line.startswith("#"):
                                result_output_nb_variants += 1
                                result_lines.append(line.strip())

                    # Expected result
                    expected_result_nb_lines = expected_results.get("nb_lines", None)
                    expected_result_nb_variants = expected_results.get("nb_variants", None)

                    # Compare
                    assert result_output_nb_lines == expected_result_nb_lines
                    assert result_output_nb_variants == expected_result_nb_variants
