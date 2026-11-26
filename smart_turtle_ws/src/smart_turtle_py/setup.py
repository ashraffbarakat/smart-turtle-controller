from setuptools import find_packages, setup

package_name = 'smart_turtle_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Ashraf Barakat',
    maintainer_email='ashrafbarakat@yahoo.com',
    description='Logic and Control Package for Smart Turtle Controller',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'command_publisher = smart_turtle_py.command_publisher:main',
            'turtle_controller = smart_turtle_py.turtle_controller:main',
            'reset_node = smart_turtle_py.reset_node:main',
        ],
    },
)
