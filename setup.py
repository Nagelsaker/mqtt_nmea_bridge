from setuptools import setup, find_packages

setup(
    name='mqtt_nmea_bridge',
    version='0.1.0',
    url='https://github.com/Nagelsaker/mqtt_nmea_bridge',
    author='Simon J. N. Lexau',
    author_email='simon.lexau@ntnu.no',
    description='A bridge for MQTT communication using custom NMEA messages.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'paho-mqtt',  # Add other dependencies here
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)