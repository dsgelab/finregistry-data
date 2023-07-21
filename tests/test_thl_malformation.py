import pytest
from finregistry_data.thl_malformations import *


def test_join_multiline_rows():
    lines = """TNRO;DIAGNOSE;ICD9;ICD10
FR0000000;one line diagnosis;000000;Q00.0
FR0000000;three line
diagnosis
;000000;Q00.0
FR0000000;one line diagnosis;000000;Q00.0"""
    expected = [
        ("FR0000000", "one line diagnosis", "000000", "Q00.0"),
        ("FR0000000", "three line\ndiagnosis\n", "000000", "Q00.0"),
        ("FR0000000", "one line diagnosis", "000000", "Q00.0"),
    ]
    result = join_multiline_rows(lines)
    assert result == expected
