from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r', encoding="utf-8") as f:
        return f.read()


setup(
    name='PyCharacterAI',
    version='2.1.0',
    author='XtraF',
    author_email='igoromarov15@gmail.com',
    description='An unofficial asynchronous api wrapper for Character AI.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/Xtr4F/PyCharacterAI',
    packages=find_packages(),
    install_requires=['curl-cffi'],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.8'
)

