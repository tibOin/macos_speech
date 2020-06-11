#!/usr/bin/env python
#~*~ coding: utf-8 ~*~

from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='macos_speech',
      version='1.0b1',
      description='Leverage the macOS `say` command into you scripts',
      long_description=readme(),
      long_description_content_type="text/markdown",
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: System :: Operating System',
        'Topic :: Utilities'

      ],
      keywords='macos, say, speech synthesis',
      url='https://github.com/tibOin/macos_speech/',
      author='tibOin',
      author_email='tiboin@protonmail.com',
      license='MIT',
      packages=['macos_speech'],
      include_package_data=True,
      zip_safe=False)
