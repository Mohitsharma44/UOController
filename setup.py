
from setuptools import setup, find_packages
import sys, os

setup(name='uocontroller',
    version='0.1',
    description="Command line tool for controlling UO equipments",
    long_description="Command line tool for controlling UO equipments",
    classifiers=[],
    keywords='',
    author='[Mohit Sharma]',
    author_email='[Mohitsharma44@gmail.com]',
    url='https://github.com/mohitsharma44/UOController',
    license='[MIT]',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=[
        ### Required to build documentation
        # "Sphinx >= 1.0",
        ### Required for testing
        # "nose",
        # "coverage",
        ### Required to function
        'cement',
        ],
    setup_requires=[],
    entry_points="""
        [console_scripts]
        uocontroller = uocontroller.cli.main:main
    """,
    namespace_packages=[],
    )
