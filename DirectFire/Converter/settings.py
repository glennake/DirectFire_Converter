"""
Settings for DirectFire Converter
"""


import os
from traceback_with_variables import Format

# Base directory, build paths like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Logging directory
LOG_DIR = BASE_DIR + "logs"

# Logging level
LOG_LEVEL = 2  # 1:DEBUG, 2:INFO, 3:WARNING, 4:ERROR, 5:CRITICAL

# Output directory
OUTPUT_DIR = BASE_DIR + "output"

# Traceback with variables formatting
TBWV_FMT = Format(
    before=10,
    after=5,
    max_value_str_len=9999999,
    max_exc_str_len=9999999,
)