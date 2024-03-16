from setuptools import setup, find_packages

setup(
    name='gyl',
    version='0.1',
    description='General Youtube animation Library',
    author='Robby-Blue',
    license='GPL-3.0-only',
    packages=find_packages(),
    install_requires=[
        'fast-diff-match-patch',
        'Pillow',
        'cairosvg'
    ],
    data_files=[('gyl/fonts', ['gyl/fonts/Roboto-Black.ttf'])],
)