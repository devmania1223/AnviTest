import sys
import os
base_directory = os.sep.join(os.path.abspath(os.path.dirname(__file__)).split(os.sep))
if base_directory not in sys.path:
    sys.path.append(base_directory)
