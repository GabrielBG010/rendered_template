#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `defaultproject` package."""

import os
import tempfile
from tempfile import TemporaryDirectory
from unittest import TestCase

from defaultproject.hash_str import hash_str
from defaultproject.io import atomic_write


class FakeFileFailure(IOError):
    pass


class AtomicWriteTests(TestCase):
    def test_atomic_write(self):
        """Ensure file exists after being written successfully"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")
            with atomic_write(fp, "w") as f:
                assert not os.path.exists(fp)
                tmpfile = f.name
                f.write("asdf")
            assert not os.path.exists(tmpfile)
            assert os.path.exists(fp)

            with open(fp) as f:
                self.assertEqual(f.read(), "asdf")

    def test_atomic_failure(self):
        """Ensure that file does not exist after failure during write"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            with self.assertRaises(FakeFileFailure):
                with atomic_write(fp, "w") as f:
                    tmpfile = f.name
                    assert os.path.exists(tmpfile)
                    raise FakeFileFailure()
            assert not os.path.exists(tmpfile)
            assert not os.path.exists(fp)

    def test_file_exists(self):
        """Ensure an error is raised when a file exists"""
        with self.assertRaises(FileExistsError):
            temporary_file = tempfile.NamedTemporaryFile(delete=False)
            temporary_file_name = temporary_file.name
            temporary_file.close()
            with atomic_write(temporary_file_name, "w") as f:
                pass
                if f:
                    pass
            os.unlink(temporary_file_name)
