import coverage
import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).absolute().parent.parent.joinpath("security-center")))
from .test_model import ModelTest
#coverage.process_startup()

def setUpModule():
    print("setUp test")


def tearDownModule():
    print("tearUp test")


if __name__ == '__main__':
    cov = coverage.Coverage(cover_pylib="model")
    cov.start()
    unittest.main()
    cov.stop()
    cov.save()
    cov.html_report()
