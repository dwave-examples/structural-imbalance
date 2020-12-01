from functools import lru_cache

from dwave.cloud import Client
from dwave.cloud.exceptions import ConfigFileError

@lru_cache(maxsize=None)
def qpu_available():
    """Check whether QPU solver is available"""
    try:
        with Client.from_config() as client:
            solver = client.get_solver(qpu=True)
    except (ConfigFileError, ValueError) as e:
        return False
    else:
        return True
        
