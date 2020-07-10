import os
import codecs
from setuptools import find_packages, setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-nna',
    version='0.1.0',
    author='Marcelo Duarte Trevisani',
    author_email='marcelo.trevisani@imgtec.com',
    maintainer='Marcelo Duarte Trevisani',
    maintainer_email='marcelo.trevisani@imgtec.com',
    license='Apache Software License 2.0',
    url='https://github.com/marcelotrevisani/pytest-nna',
    description='Pytest plugin to be used with the components',
    long_description=read('README.rst'),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires='>=3.6',
    install_requires=[
        'pytest>=5.3.2',
        "pytest-reportlog",
        "pytest-timeout",
        "pytest-json-report",
        "requests",
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
    ],
    entry_points={
        'pytest11': [
            'pytest_nna = pytest_nna.plugin',
        ],
    },
)
