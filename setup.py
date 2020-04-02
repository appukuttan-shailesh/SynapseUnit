try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

json_files = package_files('synapseunit/tests/stimuli')

setup(
    name='synapseunit',
    version='0.0.2',
    author='Justinas Dainauskas, Shailesh Appukuttan',
    author_email='shailesh.appukuttan@unic.cnrs-gif.fr',
    packages=['synapseunit', 'synapseunit.tests', 'synapseunit.capabilities', 'synapseunit.scores'],
    package_data={'synapseunit': json_files},
    url='https://github.com/appukuttan-shailesh/SynapseUnit',
    license='BSD-3-Clause',
    description='A SciUnit library for data-driven validation testing of synaptic models.',
    long_description="",
    install_requires=['sciunit>=0.2.1']
)
