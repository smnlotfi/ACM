from setuptools import setup
from setuptools import setup, find_packages

setup(
    name='Techsiro_commons',
    version='0.1.0',
    description='Commons for techsiro_project',
    author='Thechsiro Team',
    author_email='info@techsiro.com',
    packages=find_packages(include=['commons.*']),
    install_requires=[
        'Django==4.2.7',
        'djangorestframework==3.14.0',
        'drf-spectacular==0.26.5'
    ],

)