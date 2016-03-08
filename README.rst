|master-status| |master-docs|


==========
Status
==========

Please use for now the dev branch if you work with Cloudmesh.

==================
Cloudmesh workflow
==================


Cloudmesh workflow provides a tiny Domain Specific Language (two operators:
``|`` and ``&``) for parallel and sequential (respectively) evaluation
of Python functions.

==============
 Installation
==============

::

  pip install -r requirements.txt
  pip install .


===============
 Documentation
===============

See ReadTheDocs:

- |dev-docs|: dev
- |master-docs|: master
- http://cloudmesh.github.io/workflow

==============
 Build Status
==============

On Travis:

- |dev-status|: dev
- |master-status|: master

==============
 Contributing
==============

1. Fork.
2. Add yourself to ``CONTRIBUTORS.md``.
3. Make a pull-request against the ``dev`` branch.


=========
 License
=========

See `LICENSE <https://github.com/cloudmesh/workflow/blob/master/LICENSE>`_


.. |dev-docs| image:: http://readthedocs.org/projects/cloudmesh-workflow/badge/?version=dev
   :target: http://cloudmesh-workflow.readthedocs.org/en/dev
   :alt: Documentation for dev branch

.. |master-docs| image:: http://readthedocs.org/projects/cloudmesh-workflow/badge/?version=master
   :target: http://cloudmesh-workflow.readthedocs.org/en/master/
   :alt: Documentation for master branch

.. |master-status| image:: https://travis-ci.org/cloudmesh/workflow.svg?branch=master
    :target: https://travis-ci.org/cloudmesh/workflow

.. |dev-status| image:: https://travis-ci.org/cloudmesh/workflow.svg?branch=dev
    :target: https://travis-ci.org/cloudmesh/workflow
