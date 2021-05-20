import setuptools

setuptools.setup(
    name="graph_extractor",
    version="0.0.2",
    author="Ing. Branislav Vaculciak",
    author_email="branislav@vaculciak.sk",
    description="Python package for creating graph model for GCN",
    packages=setuptools.find_packages(),
    classifiers=[
        "AI :: Tensorflow :: Python",
        "Graph :: Graph convolution network :: GCN"
    ],
    include_package_data=True,
    python_requires='>=3.7',
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