#!/usr/bin/env python
import io
import os
import sys

from setuptools import find_packages, setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()


readme = io.open('README.rst', 'r', encoding='utf-8').read()

setup(
    name='frustum',
    description='(Almost) out-of-the box logging',
    long_description=readme,
    url='https://github.com/Vesuvium/frustum',
    author='Jacopo Cascioli',
    author_email='jacopocascioli@gmail.com',
    license='MIT',
    version='0.0.3',
    packages=find_packages(),
    tests_require=[
        'pytest',
        'pytest-mock'
    ],
    setup_requires=['pytest-runner'],
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ]
)
