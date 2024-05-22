import setuptools

setuptools.setup(
    name="docflow_api",
    version="0.1",
    author="Ing. Branislav Vaculciak",
    author_email="branislav@vaculciak.sk",
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires='>=3.9',
    install_requires=['mpi4py>=2.0',
                      'numpy',
                      'unidecode',
                      'shapely',
                      'requests',
                      'Pillow',
                      'validators',
                      'pyOpenSSL',
                      'pymongo',
                      'geotext',
                      'google-auth',
                      'google-cloud-vision',
                      'google-cloud-storage',
                      'bpemb',
                      'attrdict',
                      'lxml',
                      'dateparser'
                      ]
)