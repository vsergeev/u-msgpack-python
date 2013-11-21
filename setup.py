from distutils.core import setup

setup(
    name='u-msgpack-python',
    version='1.4',
    description='A lightweight msgpack serializer and deserializer written in pure Python.',
    author='vsergeev',
    author_email='vsergeev at gmail',
    url='https://github.com/vsergeev/u-msgpack-python',
    py_modules=['umsgpack'],
    long_description="""u-msgpack-python is a lightweight `MessagePack <https://github.com/msgpack/msgpack>`_ serializer and deserializer module, compatible with both Python 2 and Python 3. u-msgpack-python is fully compliant with the latest `MessagePack specification <https://github.com/msgpack/msgpack/blob/master/spec.md>`_, as of September 29, 2013. In particular, it supports the new binary, UTF-8 string, and application ext types. See https://github.com/vsergeev/u-msgpack-python for more information.""",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    license='MIT',
    keywords='msgpack serialization deserialization',
    )

