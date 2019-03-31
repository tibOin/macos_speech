#!/usr/bin/env python
#~*~ coding: utf-8 ~*~

from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='macos_speech',
      version='0.1a',
      description='Leverage the macOS `say` command into you scripts',
      long_description=readme(),
      long_description_content_type="text/markdown",
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
      ],
      keywords='macos, say, speech synthesis',
      url='https://github.com/tibOin/macos_speech/',
      author='chalios',
      author_email='tiboin@protonmail.com',
      license='MIT',
      packages=['macos_speech'],
      include_package_data=True,
      zip_safe=False)
