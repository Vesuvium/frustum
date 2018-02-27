Frustum
========

(Almost) out-of-the box logging. Frustum is a wrapper around the standard's
library logging, so you don't have to write the same boilerplate again.

Install::

    pip install frustum

Usage::

    from frustum import Frustum

    # Initialize with logger name and level
    frustum = Frustum('logger_name', 'debug')

    # Register all the events that you want within frustum
    frustum.register_event('setup', 'info', 'Frustum has been setup in {}')

    # Start the logger
    frustum.start_logger()

    # Now you can use the registered events in this way
    frustum.log('setup', 'readme')

    # The previous call would output:
    # INFO:app:Frustum has been setup in readme
    # into your stdout (as per standard logging configuration)
