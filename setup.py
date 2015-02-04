import libgiza

from setuptools import setup, find_packages

REQUIRES = [
    'jinja2',
    'pyyaml',
]

TEST_REQUIRES = [
    'giza'
]

setup(
    name='libgiza',
    maintainer='tychoish',
    maintainer_email='sam@tychoish.com',
    description='Build System Toolkit',
    version=libgiza.__version__,
    license='Apache 2.0',
    url='http://github.com/tychoish/libgiza/',
    packages=find_packages(),
    test_suite=None,
    tests_require=TEST_REQUIRES,
    install_requires=REQUIRES,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Build Tools',
    ],
)
