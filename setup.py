from setuptools import setup, find_packages

setup(name='simple_test',
      version='0.5',
      url='',
      license='',
      author='melt',
      author_email='ycwfmelt@live.cn',
      description='Simple Test FrameWork',
      packages=find_packages(exclude=['test', 'local', '.vscode']),
      long_description=open('README.md').read(),
      zip_safe=False,
      setup_requires=['pytest>="4.6"',
                      'requests>="2.0"',
                      'mysql-connector-python>="8.0.0"',
                      'pyyaml>="5.0"'],)
