import os
import sys

# Get the current working directory
current_dir = os.getcwd()

# Add it to PYTHONPATH (runtime effect)
sys.path.insert(0, current_dir)

# Optional: also modify environment variable PYTHONPATH (for subprocesses)
os.environ["PYTHONPATH"] = current_dir + os.pathsep + os.environ.get("PYTHONPATH", "")


from mangum import Mangum  # noqa
from app.framework import App  # noqa

handler = Mangum(App)
