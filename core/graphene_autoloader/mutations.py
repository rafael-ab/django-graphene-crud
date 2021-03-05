import os
import re
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
mutations_base_classes = []

for directory in subdirectories:
    try:
        module = importlib.import_module(f'{directory}.mutations')
        if module:
            classes = [cls for cls in inspect.getmembers(module, inspect.isclass)]
            mutations = [c[1] for c in classes if 'Mutation' in c[0]]
            mutations_base_classes += mutations
    except ModuleNotFoundError:
        pass

properties = {}
for cls in mutations_base_classes:
    # transform ClassNameMutation to class_name
    prop_name = '_'.join(re.findall('[A-Z][^A-Z]*', cls.__name__)[:-1]).lower()
    properties.update({ prop_name: cls.Field() })

Mutation = type(
    'Mutation',
    tuple([ObjectType]),
    properties
)
