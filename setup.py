from setuptools import setup

setup(name='cbpi4_SerialPortPowerRegulator',
      version='0.0.1',
      description='CraftBeerPi Plugin',
      author='',
      author_email='',
      url='',
      include_package_data=True,
      package_data={
        # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.rst', '*.yaml'],
      'cbpi4_SerialPortPowerRegulator': ['*','*.txt', '*.rst', '*.yaml']},
      packages=['cbpi4_SerialPortPowerRegulator'],
     )