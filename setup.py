import setuptools

setuptools.setup(
    name='pytimer',
    version='0.0.2',
    description='pytimer is an easy to use timer',
    long_description='context based timer to easily time your code',
    url='https://veltzer.github.io/pytimer',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    license='GPL3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='python timing time context manager utility',
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
)
