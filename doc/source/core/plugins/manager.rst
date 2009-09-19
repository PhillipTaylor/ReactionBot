:mod:`manager`
==============

.. index:: module: core.plugins.manager

.. module:: manager


Plugin manager object.

Managing plugins
----------------

Because with txIRCbot it is possible to have as many plugin objects as we
want, global registration object is requred. That's what
:attr:`plugin_manager` is doing for us.


.. class:: PluginManager(object)

    Plugin manager singleton class. Instead of calling it's constructor, it's
    good to use :attr:`plugin_manager` instance.

    .. method:: register(self, plugin)

        Register any plugin class instance that provide at least one interface
        from :mod:`core.plugins.interface`

    .. method:: filter(self, action, channel, interface, name)

        Returns filtered list of registered plugins. You can filter by
        `action` type, `channel` name, provided `interface` class or simply
        plugin uniqe `name`

.. data:: plugin_manager 

    :class:`PluginManager` class instance. 


`plugin_manager` usage example
------------------------------

Example of plugin intance registration with :attr:`plugin_manager`::

    from zope.interface import implements
    from core.plugins.interface import IPlugin
    from core.plugins.manager import plugin_manager

    class MyPlugin(object):
        implements(IPlugin)
        name = 'simple.plugin'

    my_plugin = MyPlugin()
    plugin_manager.register(my_plugin)



Managing protocols
------------------


.. TODO
