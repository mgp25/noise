# -*- coding: utf-8 -*-
import noise
from setuptools import find_packages, setup

setup(
    name='noise',
    version=noise.__version__,
    packages=find_packages(exclude=['tests', 'examples']),
    install_requires=['cryptography>=2.5'],
    extras_require={
        'GuardedHandshakeState': ['transitions']
    },
    test_requires=['pytest'],
    license='MIT',
    platforms='any',
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Natural Language :: English',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Operating System :: MacOS :: MacOS X',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX :: Linux',
                 'Topic :: Security :: Cryptography',
                 'Topic :: Software Development :: Libraries :: Python Modules']
)
