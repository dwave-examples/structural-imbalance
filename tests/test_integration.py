#    Copyright 2020 D-Wave Systems Inc.

#    Licensed under the Apache License, Version 2.0 (the "License")
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http: // www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import subprocess
import unittest
import time
import os

class IntegrationTests(unittest.TestCase):

    def setUp(self):
        self.verificationErrors = []
        self.output=None

    def VerifyErrors(self,output):

        try: 
            self.assertNotIn("ERROR",output.upper() )
        except AssertionError as e:
            print("Verify if error string contains in output failed \n")
            self.verificationErrors.append(str(e))

        try: 
            self.assertNotIn("WARNING",output.upper() )
        except AssertionError as e:
            print("Verify if warning string contains in output failed \n")
            self.verificationErrors.append(str(e))

    def runDemo(self,hardware):
        cwd=os.getcwd()
        self.output=subprocess.check_output(["python", cwd+"/demo.py", hardware])
        self.output=str(self.output)

    def test_structural_imbalance_cpu(self):
        self.runDemo("cpu")

        print("Example output \n"+self.output)
        try: 
            self.assertIn("Running demo on cpu",self.output )
        except AssertionError as e:
            print("Test structural_imbalance example verification failed \n")
            self.verificationErrors.append(str(e))

        try: 
            self.assertIn("Created CSV file: Results/Global/Structural Imbalance.csv",self.output )
        except AssertionError as e:
            print("Test structural_imbalance example verification failed \n")
            self.verificationErrors.append(str(e))

        self.VerifyErrors(self.output)

    def test_structural_imbalance_qpu(self):
        self.runDemo("qpu")
        print("Example output \n"+self.output)
        try: 
            self.assertIn("Running demo on qpu",self.output )
        except AssertionError as e:
            print("Test structural_imbalance example verification failed \n")
            self.verificationErrors.append(str(e))

        try: 
            self.assertIn("Created CSV file: Results/Global/Structural Imbalance.csv",self.output )
        except AssertionError as e:
            print("Test structural_imbalance example verification failed \n")
            self.verificationErrors.append(str(e))

        self.VerifyErrors(self.output)

    def tearDown(self):
        self.assertEqual([], self.verificationErrors)

if __name__ == '__main__':
    unittest.main()