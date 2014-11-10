from setuptools import setup, find_packages

setup(
    name='braubuddy',
    version='0.4.0',
    author='James Stewart',
    author_email='jstewart101@gmail.com',
    description='An extensile temperature management framework.',
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
        'tosr0x>=0.2.0',
        'pyserial>=2.0',                # required for tosr0x
        'temperusb>=1.2.0',
        'ds18b20>=0.01.03',
        'cherrypy>=3.2.2',
        'pyxdg>=0.25',
        'jinja2>=2.7.0',
        'mock>=1.0,<2.0',
        'alabaster>=0.6.0',
        'graphitesend>=0.3.4,<0.4',
        'librato-metrics>=0.4.12,<0.5',
        'twitter>=1.15,<2',
        'pygal>=1.5.1,<2',
        'cairosvg>=1.0.9,<2',           # required for pygal png
        'tinycss>=0.3,<0.4',            # required for pygal png
        'cssselect>=0.9.1,<0.10',       # required for pygal png
        'lxml>=3.4,<4',                 # required for pygal png
        'dweepy>=0.0.1,<0.0.2',
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
