import os

from pdh import adnod


def test_ns2path_builds_expected_windows_path() -> None:
    """test_ns2path_builds_expected_windows_path."""
    expected = os.path.join(r"C:\PDH\DATA", "L1K4", "L2K7")
    assert adnod.ns2path("2:4:7") == expected


def test_uns2path_builds_expected_windows_path() -> None:
    """test_uns2path_builds_expected_windows_path."""
    expected = os.path.join(r"C:\PDH\USER", "L1K9")
    assert adnod.uns2path("2:9") == expected
