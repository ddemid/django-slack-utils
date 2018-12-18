import codecs
import re
from os import path
from setuptools import setup, find_packages


def read(*parts):
    filename = path.join(path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='django-slack-utils',
    version=find_version("slack_utils", "__init__.py"),
    description="A Django app for handling Slack webhooks",
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='slack, django',
    author='Dmitry Demidenko',
    author_email='dmitry.demidenko@startmatter.com',
    maintainer='Dmitry Demidenko',
    maintainer_email='dmitry.demidenko@startmatter.com',
    url='https://github.com/startmatter/django-slack-utils',
    license='BSD',
    packages=find_packages(exclude=['tests']),
    install_requires=[
    ],
    zip_safe=False,
)