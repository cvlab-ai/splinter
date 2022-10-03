from setuptools import setup, find_packages

setup(
    name='Splinter',
    version='0.1',
    description='Exam Checker',
    url='https://github.com/cvlab-ai/splinter',
    packages=find_packages(where='inference_engine/src'),
    package_dir={"": 'inference_engine/src'},
)
