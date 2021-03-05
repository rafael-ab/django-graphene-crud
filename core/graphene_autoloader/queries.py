import os
import importlib
import inspect
from pathlib import Path
from graphene import ObjectType

BASE_DIR = Path(__file__).resolve().parent.parent.parent
subdirectories = [
    subdir
    for subdir in os.listdir(BASE_DIR)
    if os.path.isdir(os.path.join(BASE_DIR, subdir)) and
    subdir != '__pycache__' and subdir[0] != '.'
]
queries_base_classes = []

for directory in subdirectories:
    try:
        module = importlib.import_module(f'{directory}.queries')
        if module:
            classes = [cls for cls in inspect.getmembers(module, inspect.isclass)]
            queries = [c[1] for c in classes if 'Query' in c[0]]
            queries_base_classes += queries
    except ModuleNotFoundError:
        pass

properties = {}
for base_class in queries_base_classes:
    for prop in base_class.__dict__.keys():
        if prop not in ['__module__', '__dict__', '__weakref__', '__doc__']:
            properties.update({ prop: base_class.__dict__[prop] })

Query = type(
    'Query',
    tuple([ObjectType]),
    properties
)
