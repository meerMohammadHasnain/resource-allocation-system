import os

from codecs import open
from setuptools import setup, find_packages
from setuptools.command.install import install


requirements = []
if os.path.exists('requirements.txt'):
    with open('requirements.txt', encoding='utf-8') as f:
        req_str = f.read()
        requirements = filter(lambda req: bool(req), req_str.split('\n'))


setup(
    name='resource-allocation-system',
    version='0.0.1.dev0',
    description='Resource Allocation System',
    author='Mohd. Hasnain Meer',
    author_email='hasnainmeer307@gmail.com',
    install_requires=requirements,
    packages=find_packages(exclude=['build', 'dist']),
    package_data={'com': []},
    cmdclass={'install': install}
)
