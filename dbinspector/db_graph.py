# -*- coding: utf-8 -*-
from functools import reduce

import copy

default_style = {
'baseStyle':{
    'font': {
        "family": "Luxi Sans",
        "size": 12,
        "shape": "regular"
    },
},'tableStyle': {
    "color": "white",
    "bgColor": "#00649d",
    "keyIcon": "&#x1f511;",
    "nonKeyIcon": "&ensp;"
}, 'columnStyle': {
    "color": "black",
    "bgColor": "#82d1f5"
}, 'keyColumnStyle': {
    "color": "black",
    "bgColor": "#88ff88"
}}

def merge(a, b):
    """merges b into a"""
    c = copy.deepcopy(a)
    for key in b:
        if key in a:
            if isinstance(b[key], dict):
                c[key] = merge(a[key], b[key])
            elif isinstance(b[key], list):
                c[key] = a[key] + copy.deepcopy(b[key])
            else:
                c[key] = b[key]  # Override
        else:
            c[key] = b[key]
    return c

class Table:
    def __init__(self, name):
        self.name = name  # table name
        self.column = []  # a triple of column name, datatype, and primary key,
        # for example: ("user_name", "varchar(64)", True)
        self.style = reduce(merge, {}, default_style)

    def add_column(self, column_tuple):
        self.column.append(column_tuple)
        return self

    def to_dot(self):
        """return dot-string representing this table"""
        return '''"{}" [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#ffffff">
    <TR><TD COLSPAN="3" BGCOLOR="{}" ALIGN="CENTER"><FONT COLOR="{}">{}</FONT></TD></TR>\n    '''.format(
            self.name, self.style["tableStyle"]["bgColor"], self.style["tableStyle"]["color"], self.name) \
            + '\n    '.join(map(self.__col_to_dot, self.column)) \
            + '\n    </TABLE>> tooltip="{}"];'.format(self.name)
        pass

    def __col_to_dot(self, column):
        key = self.style["tableStyle"]["nonKeyIcon"]
        color = {
            "bgColor": self.style["columnStyle"]["bgColor"],
            "color":  self.style["columnStyle"]["color"]
        }
        if column[2]: # key column
            key = self.style["tableStyle"]["keyIcon"]
            color = {
                "bgColor": self.style["keyColumnStyle"]["bgColor"],
                "color": self.style["keyColumnStyle"]["color"]
            }
        return \
'''<TR><TD PORT= "{name}$left"  SIDES="lb" BGCOLOR="{color}" ALIGN="LEFT">{key}</TD>
	    <TD PORT="{name}$middle" SIDES="b"  BGCOLOR="{color}" ALIGN="LEFT">{name}</TD>  
		<TD PORT="{name}$right" SIDES="rb" BGCOLOR="{color}" ALIGN="RIGHT">::{type}</TD>
	</TR>'''.format(name=column[0], color=color["bgColor"], type=column[1], key=key)
        pass

    def apply_style(self, style):
        self.style = reduce(merge, [self.style, style])

    def __str__(self):
        return self.name


class DBGraph:
    def __init__(self, name):
        """
        Init a DB Graph
        :param name:
        """
        self.name = name  # name of the graph
        self.label = name
        self.tables = {}  # a db graph has a list of table, saved as map table Name -> table definition
        self.relationship = []  # a db graph has a list of relationship, which denotes the foreign key of tables in graph.
        self.style = reduce(merge,{}, default_style) # copy the default style
        self.table_style = {}
        self.apply_style(default_style)
        pass

    def set_label(self, label):
        self.label = label
        return self

    def add_table(self, table):
        self.tables[table.name] = table
        return self

    def apply_style(self, style):
        self.style = reduce(merge, [{}, style])
        self.table_style = reduce(merge, [{}, self.style['baseStyle'], self.style['tableStyle'] ])
        for tb_name, table in self.tables.items():
            table.apply_style(self.style)
        return self
        pass

    def add_relationship(self, tab_tuple, foreign_tab_tuple):
        # TODO: check if table has column
        self.relationship.append( (tab_tuple, foreign_tab_tuple) )
        return self
        pass

    def to_dot(self):
        return \
'''digraph "{name}" {{
    graph [ label="{label}"
            labeljust="l" rankdir="RL"
            bgcolor="#f0f0f0" nodesep="0.5" ranksep="1.0"
            fontname="{0[font][family]}"
            fontsize="{0[font][size]}"
            margin="0" ];
  node [ fontname="{1[font][family]}" fontsize="{1[font][size]}" shape="plaintext" ];
  edge [ arrowsize="0.6" ];
'''.format(self.style['baseStyle'], self.table_style, name=self.name, label=self.label) \
        + '\n /*tables go here*/ \n' \
        + "\n".join( map(lambda t:t.to_dot(), list( self.tables.values()) ) ) \
        + '\n /*relationship goes here*/ \n' \
        + "\n".join( map(self.__relationship_to_dot, self.relationship ) ) \
        + "\n}"
        pass

    def __relationship_to_dot(self, r):
        return \
'''"{table1}":"{col1}$left":w -> "{table2}":"{col2}$right":e [arrowhead=none dir=back arrowtail=crowodot];'''.format(table1=r[0][0], col1=r[0][1], table2=r[1][0], col2=r[1][1])
        pass


    def __str__(self):
        """for debug only"""
        return self.name + "(" \
               +  ",".join(map(str,self.tables)) \
               + ")"