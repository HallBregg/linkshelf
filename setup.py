import setuptools


with open('requirements.txt', 'r') as req:
    required_packages = req.read().splitlines()


setuptools.setup(
    name='linkshelf',
    author='HallBregg',
    author_email='hallbregg0@gmail.com',

    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    scripts=['src/manage.py'],

    include_package_data=True,
    install_requires=required_packages,
    python_requires='>=3.10',
)
