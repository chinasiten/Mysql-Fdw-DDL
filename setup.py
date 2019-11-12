from setuptools import find_packages, setup

setup(
    name='mysql_fdw_ddl',
    version='0.0.0',
    author='SitenSong',
    author_email='chinasiten@live.cn',
    license='BSD',
    install_requires=['sqlalchemy>=1.3.0','pymysql>=0.9.0'],
    packages=find_packages(),
)