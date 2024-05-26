#!/usr/bin/env python
from setuptools import setup, find_packages

with open("bpycanvas/__init__.py") as fin:
    for line in fin:
        if line.startswith("__version__ ="):
            version = eval(line[14:])
            break

setup(name='bpycanvas',
      version=version,
      description='A Blender modeling tool with a similar modeling method to SPLayout.',
      author='Zhenyu ZHAO',
      author_email='mailtozyzhao@163.com',
      install_requires=[],
      # long_description=long_description,
      url="https://github.com/Hideousmon/blender-layout-render",
      include_package_data=True,
      packages=find_packages()
      )