# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='nutcracker',
    version='0.1.0',
    description='Run several Pecan or WSGI applications in a single bundle, declaratively.',
    author='Jonathan LaCour',
    author_email='jonathan@cleverdevil.org',
    install_requires=[
        "pecan",
        "six"
    ],
    test_suite='nutcracker',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=['ez_setup'])
)
