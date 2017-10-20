# -*- coding: utf-8 -*-
from itertools import groupby
from sqlalchemy import create_engine

from .db_graph import Table, DBGraph

class PgDbInspector:
    query_table = '''
SELECT               
      pg_class.relname as table_name,
      pg_attribute.attname as column_name,
	  (pg_attribute.attnum = any(pg_index.indkey) AND indisprimary) as primary_key,
      CASE 
	    WHEN  pg_attribute.atttypid = 1043 AND pg_attribute.atttypmod > 4
        THEN 
            'varchar(' || (pg_attribute.atttypmod - 4)::text || ')'
        ELSE
            format_type(pg_attribute.atttypid, pg_attribute.atttypmod)     
      END as data_type,
      pg_attribute.attnum as ordinal_position
  FROM pg_index, pg_class, pg_attribute, pg_namespace 
  WHERE 
      indrelid = pg_class.oid AND 
      nspname = 'public' AND 
      pg_class.relnamespace = pg_namespace.oid AND 
      pg_attribute.attrelid = pg_class.oid AND 
      pg_attribute.attnum > 0 
      AND indisprimary
ORDER BY 
     table_name 
   , ordinal_position
    '''

    query_foreign_key = '''
SELECT 
	conname AS constraint_name, 
	conrelid::regclass::text AS table_name, 
	ta.attname AS column_name,
    confrelid::regclass::text AS foreign_table_name, 
	fa.attname AS foreign_column_name
FROM (
	SELECT 
		conname, 
		conrelid, 
		confrelid,
        unnest(conkey) AS conkey, 
		unnest(confkey) AS confkey
    FROM pg_constraint
    WHERE contype = 'f'
	-- AND conname = 'comment_name_fkey'
) sub
JOIN pg_attribute AS ta ON ta.attrelid = conrelid AND ta.attnum = conkey
JOIN pg_attribute AS fa ON fa.attrelid = confrelid AND fa.attnum = confkey
;
    '''

    def __init__(self, db_url):
        self._db_ulr = db_url
        self.__engine = create_engine(db_url)
        print(db_url)
        pass

    def inspect(self):
        connect = self.__engine.connect()
        dbg = DBGraph(self._db_ulr)
        rows = connect.execute(PgDbInspector.query_table).fetchall()

        for table, columns in groupby(rows, lambda x:x[0]):
            tab = Table(table)
            for c in columns:
                tab.add_column( (c[1], c[3], c[2]) )
            dbg.add_table(tab)
        relationship = connect.execute(PgDbInspector.query_foreign_key).fetchall()
        for r in relationship:
            dbg.add_relationship( (r[1],r[2]), (r[3],r[4]) )
        return dbg
        pass


