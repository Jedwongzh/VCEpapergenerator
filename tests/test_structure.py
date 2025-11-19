# tests/test_structure.py

import unittest
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestProjectStructure(unittest.TestCase):

    def test_data_preparation_import(self):
        """
        Tests that the data_preparation module and its components can be imported.
        """
        try:
            from vce_paper_generator.data_preparation import processing
            self.assertIsNotNone(processing)
        except ImportError as e:
            self.fail(f"Failed to import data_preparation module: {e}")

    def test_common_import(self):
        """
        Tests that the common module and its components can be imported.
        """
        try:
            from vce_paper_generator.common import vector_db
            self.assertIsNotNone(vector_db)
        except ImportError as e:
            self.fail(f"Failed to import common module: {e}")

    def test_paper_generator_import(self):
        """
        Tests that the paper_generator module and its components can be imported.
        """
        try:
            from vce_paper_generator.paper_generator import generator
            self.assertIsNotNone(generator)
        except ImportError as e:
            self.fail(f"Failed to import paper_generator module: {e}")

if __name__ == '__main__':
    unittest.main()
