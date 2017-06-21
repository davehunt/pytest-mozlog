pytest-mozlog
=============

pytest-mozlog is a plugin for pytest_ that provides an additional logging
specialized for the Mozilla universe by integrating with mozlog_.

Note that the source code for pytest-mozlog can now be found at
https://dxr.mozilla.org/mozilla-central/source/testing/mozbase/mozlog/mozlog/pytest_mozlog/plugin.py

The plugin is included with mozlog_ and will be enabled by default when the
package is installed. To disable it you can run pytest with ``-p no:mozlog``.

.. _pytest: http://www.python.org/
.. _mozlog: http://mozbase.readthedocs.io/en/latest/mozlog.html
