from setuptools import setup, find_packages

setup(
    name='braubuddy',
    version='0.3.0',
    author='James Stewart',
    author_email='jstewart101@gmail.com',
    description='An extensile thermostat framework',
    long_description=open('README.rst').read(),
    license='LICENSE.txt',
    packages=find_packages(),
    url='http://braubuddy.org/',
    include_package_data=True,
    entry_points={
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
        'mock>=1.0,<2.0',
        'alabaster>=0.6.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
