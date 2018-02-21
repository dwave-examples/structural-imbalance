Demo for the Structural Imbalance Project
=========================================

Running the Demo
----------------

You can run the demo on classical hardware (a CPU) or on a D-Wave QPU, with the selection made by the pip requirements
file used.

.. code-block:: bash

  pip install -r requirements_cpu.txt   # to run on CPU
  pip install -r requirements_qpu.txt   # to run on QPU

Running on a CPU
~~~~~~~~~~~~~~~~

.. code-block:: bash

  pip install -r requirements_cpu.txt
  python demo.py

Running on a QPU
~~~~~~~~~~~~~~~~

Access to a D-Wave system must be configured. This requires setting up a `.dwrc`_ configuration file as
described in the `dwave_micro_client`_ documentation. A default solver is required. For example:

.. code-block::

  cloud | https://cloud.dwavesys.com/sapi, token,  , DW_2000Q

where :code:`token` is a valid token for a system with server URL https://cloud.dwavesys.com/sapi corresponding to the
solver with name DW_2000Q. In this example, no proxy URL is required, so the field is left blank.

.. code-block:: bash

  pip install -r requirements_qpu.txt
  python demo.py

License
-------

Released under the Apache License 2.0. See LICENSE file.

Further Reading
---------------

Data is from the Stanford Militants Mapping Project.

Mapping Militant Organizations, Stanford University, last modified February 28, 2016,
http://web.stanford.edu/group/mappingmilitants/cgi-bin/.

.. _`.dwrc`: http://dwave-micro-client.readthedocs.io/en/latest/#configuration
.. _`dwave_micro_client`: http://dwave-micro-client.readthedocs.io/en/latest/#
