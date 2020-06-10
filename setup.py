import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='unsilence',
    version='1.0.2',
    install_requires=requirements,
    license='MIT License',
    author='Tim-Luca Lagmöller',
    author_email='mail@lagmoellertim.de',
    description='Remove Silence from Media Files',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/lagmoellertim/unsilence',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": ["unsilence=unsilence.command_line.EntryPoint:main"]
    }
)
