from setuptools import setup, find_packages
import re

version = '0.1'

def parse_requirements(file_name):
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'\s*-f\s+', line):
            pass
        else:
            requirements.append(line)

    return requirements

def parse_dependency_links(file_name):
    dependency_links = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'\s*-[ef]\s+', line):
            dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))

    return dependency_links

setup(name='webpype-django',
      version=version,
      description="WebPype functionality for Django",
      long_description=open('README.md').read(),
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='django webpipe',
      author='AJ Bahnken',
      author_email='aj@ajvb.me',
      url='https://github.com/ajvb/webpype-django',
      license='GNU General Public License v2',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires = parse_requirements('requirements.txt'),
      dependency_links = parse_dependency_links('requirements.txt'),
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
