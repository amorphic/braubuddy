from setuptools import setup

setup(
    name='braubuddy',
    version='0.1.0',
    author='James Stewart',
    author_email='jstewart101@gmail.com',
    packages=['braubuddy', 'test'],
    scripts=[],
    url='http://pypi.python.org/pypi/Braubuddy/',
    license='LICENSE.txt',
    description='An extensile thermostat framework',
    long_description=open('README.md').read(),
    entry_points = {
        'console_scripts': [
            'braubuddy = braubuddy.runserver:main',
        ]
    },
    install_requires=[
        'tosr0x>=0.2.0',
        'temperusb>=1.1.2'
    ],
)
