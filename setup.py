from setuptools import setup

setup(
    name='braubuddy',
    version='0.2.0',
    author='James Stewart',
    author_email='jstewart101@gmail.com',
    packages=['braubuddy'],
    scripts=[],
    url='http://pypi.python.org/pypi/Braubuddy/',
    license='LICENSE.txt',
    description='An extensile thermostat framework',
    long_description=open('README.rst').read(),
    entry_points = {
        'console_scripts': [
            'braubuddy = braubuddy.runserver:main',
        ]
    },
    install_requires=[
        'pyserial>=2.0',
        'tosr0x>=0.2.0',
        'temperusb>=1.2.0',
        'ds18b20>=0.01.03',
        'cherrypy>=3.2.2',
        'pyxdg>=0.25',
        'jinja2>=2.7.0',
    ],
)
