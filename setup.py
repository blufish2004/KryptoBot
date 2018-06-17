import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kryptobot",
    packages=[
        'kryptobot',
        'kryptobot.bots',
        'kryptobot.catalyst_shim',
        'kryptobot.ccxt_shim',
        'kryptobot.db',
        'kryptobot.harvesters',
        'kryptobot.listeners',
        'kryptobot.markets',
        'kryptobot.notifiers',
        'kryptobot.portfolio',
        'kryptobot.publishers',
        'kryptobot.server',
        'kryptobot.signals',
        'kryptobot.strategies',
        'kryptobot.strategies.catalyst',
        'kryptobot.strategies.mixins',
        'kryptobot.ta',
        'kryptobot.workers',
        'kryptobot.workers.catalyst',
        'kryptobot.workers.harvester',
        'kryptobot.workers.market',
        'kryptobot.workers.strategy',
    ],
    version="0.0.3",
    author="Stephan Miller",
    author_email="stephanmil@gmail.com",
    description="Cryptocurrency trading bot framework",
    long_description=long_description,
    url="https://github.com/eristoddle/KryptoBot",
    zip_safe=False,
    include_package_data=True,
    install_requires=[
          'pypubsub',
          'requests',
          'SQLAlchemy',
          'psycopg2-binary',
          'pyti',
          'ccxt',
          'redis',
          'celery',
          'flower',
          'kombu-encrypted-serializer',
          'celery-redbeat',
          'flask',
          'enigma-catalyst',
          'pandas',
          # This breaks, pymarketcap requires cython to be installed first
          'cython',
          'pymarketcap',
          'pandas',
          'ta-lib'
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ),
)
