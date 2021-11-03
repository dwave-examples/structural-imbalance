# Copyright 2020 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess
import unittest
import os
import sys

from tests import qpu_available

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class IntegrationTests(unittest.TestCase):

    def runDemo(self, hardware):
        demo_file = os.path.join(project_dir, 'structural_imbalance.py')
        output = subprocess.check_output([sys.executable, demo_file, hardware])
        return output.decode("utf-8")

    @unittest.skipIf(os.getenv('SKIP_INT_TESTS'), "Skipping integration test.")
    def test_structural_imbalance_cpu(self):
        output = self.runDemo("--cpu")
        output = output.upper()
        if os.getenv('DEBUG_OUTPUT'):
            print("Example output \n" + output)

        # Simple check to make sure a "FOUND X VIOLATIONS OUT OF Y EDEGES" message was printed
        self.assertIn("VIOLATIONS OUT OF", output)

    @unittest.skipIf(os.getenv('SKIP_INT_TESTS'), "Skipping integration test.")
    @unittest.skipUnless(qpu_available(), "requires QPU")
    def test_structural_imbalance_qpu(self):
        output = self.runDemo("--qpu")
        output = output.upper()
        if os.getenv('DEBUG_OUTPUT'):
            print("Example output \n" + output)

        # Simple check to make sure a "FOUND X VIOLATIONS OUT OF Y EDEGES" message was printed
        self.assertIn("VIOLATIONS OUT OF", output)


if __name__ == '__main__':
    unittest.main()
