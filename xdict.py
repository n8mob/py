#!/usr/local/bin/python3

import xml.etree.ElementTree as ET

def etree_to_dict(t):
    d = {c.tag: etree_to_dict(c) for c in t.getchildren()}
    if t.attrib is not None:
        d.update({'@' + k: v} for k, v in t.attrib)
        
    if t.text is not None:
        d['text'] = t.text
        
    return d
