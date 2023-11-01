from setuptools import setup, find_packages

setup(
    name='rtl-sim',
    version='0.1.0',
    description='RTL-like Simulation and Evaluation in Python',
    author='Teddy van Jerry (Wuqiong Zhao)',
    author_email='me@teddy-van-jerry.org',
    url='https://github.com/Teddy-van-Jerry/rtl-sim',
    packages=find_packages(),
    install_requires=[
        'torch>=1.0.0',
        'numpy>=1.0.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
