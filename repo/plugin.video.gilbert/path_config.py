import sys
import os

# Dynamically add the `deps` folder to the Python path
def configure_paths():
    plugin_dir = os.path.dirname(os.path.abspath(__file__))
    deps_dir = os.path.join(plugin_dir, 'deps')
    if deps_dir not in sys.path:
        sys.path.insert(0, deps_dir)
