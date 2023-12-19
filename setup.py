from setuptools import setup, find_packages

VERSION = '0.0.9'
DESCRIPTION = 'A framework to build and run Nostr NIP90 Data Vending Machines'
LONG_DESCRIPTION = ('A framework to build and run Nostr NIP90 Data Vending Machines. '
                    'This is an early stage release. Interfaces might change/brick')

# Setting up
setup(
    name="nostr-dvm",
    version=VERSION,
    author="Believethehype",
    author_email="believethehypeonnostr@proton.me",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(include=['nostr_dvm', 'nostr_dvm.backends', 'nostr_dvm.interfaces', 'nostr_dvm.tasks',
                                    'nostr_dvm.utils', 'nostr_dvm.utils.scrapper']),
    install_requires=["nostr-sdk==0.0.5",
                      "bech32==1.2.0",
                      "pycryptodome==3.19.0",
                      "python-dotenv==1.0.0",
                      "emoji==2.8.0",
                      "eva-decord==0.6.1",
                      "ffmpegio==0.8.5",
                      "lnurl==0.4.1",
                      "pandas==2.1.3",
                      "Pillow==10.1.0",
                      "PyUpload==0.1.4",
                      "requests==2.31.0",
                      "instaloader==4.10.1",
                      "pytube==15.0.0",
                      "moviepy==2.0.0.dev2",
                      "zipp==3.17.0",
                      "urllib3==2.1.0",
                      "typing_extensions==4.8.0"
                      ],
    keywords=['nostr', 'nip90', 'dvm', 'data vending machine'],
    url="https://github.com/believethehype/nostrdvm",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
    ]
)