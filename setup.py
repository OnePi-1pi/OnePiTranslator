from setuptools import setup, find_packages
import os
import sys

def read_readme(filename):
    with open(filename, encoding='utf-8') as f:
        return f.read()

long_description = read_readme('README.md')
long_description_zh = read_readme('README_zh.md')

def data_files():
    if sys.platform == 'win32':
        return [('share/onepitranslator', ['scripts/run.exe'])]
    else:
        return [('share/onepitranslator', ['scripts/run.sh'])]

setup(
    name='OnePiTranslator',
    version='1.0.0',
    author='One Pi',
    author_email='q_o_ql@163.com',
    description='A simple GUI tool for translating text or documents and renaming files or folder names using both online and offline methods.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/OnePi-1pi/OnePiTranslator',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'setuptools',
        'ttkbootstrap',
        'pillow',
        'qrcode',
        'deep_translator',
        'regex',
        'deep_translator[ai]',
        'deep_translator[docx]',
        'deep_translator[pdf]',
    ],
    extras_require={
        'complete': [
            'argostranslate',
            'spacy',
            'spacy[xx_sent_ud_sm]',
            # Add other optional dependencies here
        ],
    },
    entry_points={
        'console_scripts': [
            'onepitranslator=onepitranslator:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',  # 假设你也支持Python 3.14
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    package_data={
        'onepitranslator': [
            'resources/images/*',
            'scripts/*',
        ],
    },
    data_files=data_files(),
)
