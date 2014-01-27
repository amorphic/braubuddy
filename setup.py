from distutils.core import setup

setup(
    name='Braubuddy',
    version='0.1.0',
    author='James Stewart',
    author_email='jstewart101@gmail.com',
    packages=['braubuddy, braubuddy.test'],
    scripts=[],
    url='http://pypi.python.org/pypi/Braubuddy/',
    license='LICENSE.txt',
    description='An extensile thermostat framework',
    long_description=open('README.txt').read(),
    install_requires=[
    ],
)
