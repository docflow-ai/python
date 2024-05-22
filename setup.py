import setuptools

setuptools.setup(
    name="docflow_api",
    version="0.1.1",
    author="Ing. Branislav Vaculciak",
    author_email="branislav@vaculciak.sk",
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires='>=3.9',
    install_requires=[
        'mpi4py>=2.0',
        'bson',
        'certifi',
        'chardet',
        'filetype',
        'idna',
        'PyPDF2',
        'python-dateutil',
        'pytz',
        'requests',
        'six',
        'urllib3'
    ]
)