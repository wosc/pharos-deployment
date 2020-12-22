from setuptools import setup, find_packages


setup(
    name='batou_ext',
    version='0.1dev',
    author='Wolfgang Schnerring',
    author_email='wosc@wosc.de',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    license='GPL v2',
    install_requires=[
        'batou',
        'setuptools',
    ],
)
