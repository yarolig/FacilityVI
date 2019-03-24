import os

data_py = os.path.abspath(os.path.dirname(__file__))
run_dir = os.path.normpath(os.path.join(data_py, '..'))

def get_run_dir():
    return run_dir
