# -*- coding: utf-8 -*-

from functools import reduce

from context import dbinspector
from context import db_graph

def merge_simple_value_test():
    base = {"color": "white", "bgColor": "darkblue"}
    extend = {"bgColor": "yellow"}
    c = db_graph.merge(base, extend)

    assert base["color"] == "white"
    assert c["color"] == base["color"]
    assert base["bgColor"] == "darkblue"
    assert extend["bgColor"] == "yellow"
    assert c["bgColor"] == extend["bgColor"]


def merge_list_test():
    base = {"color": ["yellow", "green"]}
    extend = {"color": ["blue"]}

    c = db_graph.merge(base, extend)
    assert c["color"] == ["yellow", "green", "blue"]
    assert base["color"] == ["yellow", "green"]
    assert extend["color"] == ["blue"]

def merge_dict_test():
    base = {'font':{'family':'Sans', 'size': 12}}
    extend = {'font':{'family':'Mono', 'size': 11}}
    c = db_graph.merge(base, extend)
    assert c["font"]['family'] == 'Mono'
    assert base["font"]['family'] == 'Sans'
    assert extend["font"]["family"] == 'Mono'



