import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import dbinspector
from dbinspector import db_graph
from dbinspector.db_inspector import PgDbInspector
from dbinspector.main import  parse_arg
from dbinspector.main import  visual_db
