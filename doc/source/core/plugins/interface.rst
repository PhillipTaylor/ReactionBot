:mod:`interface` --- Plugin interfaces
======================================

.. index:: module: core.plugins.interface

.. module:: interface


This module contains plugin interfaces that allow to implements basic
functionality. Each plugin class has to implement at least :class:`IPlugin`.

To implement interface, use `zope.interface.implements <http://www.zope.org/Products/ZopeInterface>`_ 
function.


Basic interfaces
----------------

.. class:: IPlugin

    Base class for every plugin interface.

    .. attribute:: name 

        Unique plugin instance name.


Custom functionality interfaces
-------------------------------

.. class:: IStorable(IPlugin)

    Easy plugin data storage.

    .. method:: dump(self)
        
        Dump data stored by plugin instance. It is good choise to return
        simple type data. You may also want to use :mod:`pickle` module to
        dump Python objects into string.

    .. method:: load(self, data)

        Load dumped data. It is the same object that :meth:`dump` method
        returned.


.. class:: IInitialize(IPlugin)

    Plugin load initialization.

    .. method:: initialize(self)

        Method called just after plugin load.


.. class:: IFinalize(IPlugin)

    Plugin unload finalization.

    .. method:: finalize(self)

        Method called just after plugin unload.


.. class:: ICustomChannelsHandler(IPlugin)

    Allows each plugin instance to work only for custom channels.

    .. method:: accepts_channel(self, channel)

        Return `True` if plugin should recive messages from `channel`,
        else `False`.

.. class:: IPeriodic(IPlugin)

    Periodic metod call.

    .. attribute:: sleep_time

        Sleep time between each call.

    .. method:: periodic_handler(self, protocols)

        Handle periodic call. `protocols` is list of avaliable for that plugin
        IRC protocols instances.

.. class:: IActionHandler(IPlugin)

    Handle IRC actions.

    .. method:: accepts_action(self, action)

        Return `True` if plugin should revice `action` messages, else `False`.

    .. method:: handle_action(self, protocol, action, user, message)

        Handle IRC `message`. 


.. class:: ILineReceiver(IPlugin)


    .. method:: handle_line(self, protocol, line)

        Handle each single IRC `protocol` `line` of data.


Example plugin
--------------

Plugin class that will print last dump time::

    import time

    from zope.interface import implements
    from core.plugins.interface import IStorable
    

    class MyStoreTimePlugin(object):

        implements(IStorable)

        def __init__(self, name):
            self.name = '%s.%s' % (type(self).__name__, name)

        def dump(self):
            return time.time()

        def load(self, data):
            print 'last dump time:', data


