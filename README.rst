Frustum
========

(Almost) out-of-the box logging. Frustum is a wrapper around the standard's
library logging, so you don't have to write the same boilerplate again.

Install::

    pip install frustum

Usage::

    from frustum import Frustum

    # Initialize with verbosity from 1 to 5 (critical to info)
    frustum = Frustum(verbosity=5)

    # Register all the events that you want within frustum
    frustum.register_event('setup', 'info', 'Frustum has been setup in {}')

    # Now you can use the registered events in this way
    frustum.log('setup', 'readme')

    # The previous call would output:
    # INFO:frustum:Frustum has been setup in readme
    # into your stdout (as per standard loggin configuration)
