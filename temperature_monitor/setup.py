from setuptools import setup, find_packages
from sphinx.setup_command import BuildDoc

cmdclass = {'build_sphinx': BuildDoc}
name='stem'
version='0.0.1'
setup(
    name='stem',
    version='0.0.1',
    cmdclass=cmdclass,
    packages=find_packages(include=['stem', 'stem.*']),
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version)}}
)
