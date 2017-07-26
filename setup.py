from setuptools import setup

setup(name='FlaskApp',
      version='1.0',
      description='A Flask App to send SF reports using mechanize',
      author='Enrique Valenzuela',
      author_email='em@enriquemanuel.me',
      url='http://www.python.org/sigs/distutils-sig/',
     install_requires=['Flask>=0.10.1','mechanize','requests', 'boto3','dropbox'],
     )
