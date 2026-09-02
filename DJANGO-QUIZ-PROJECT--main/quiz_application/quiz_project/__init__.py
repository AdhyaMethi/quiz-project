"""
Quiz Project Package Initialization.

This module initializes the Django project and ensures compatibility
with MySQL on Windows using PyMySQL (if installed).
"""

# Enable PyMySQL as MySQLdb driver fallback for seamless Windows compatibility
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
