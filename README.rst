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

- |unstable-docs|: unstable
- |master-docs|: master


==============
 Build Status
==============

On Travis:

- |unstable-status|: unstable
- |master-status|: master

==============
 Contributing
==============

1. Fork.
2. Add yourself to ``CONTRIBUTORS.md``.
3. Make a pull-request against the ``unstable`` branch.


=========
 License
=========

See `LICENSE <https://github.com/cloudmesh/workflow/blob/main/LICENSE>`_


.. |unstable-docs| image:: http://readthedocs.org/projects/cloudmesh-workflow/badge/?version=unstable
   :target: http://cloudmesh-workflow.readthedocs.org/en/unstable
   :alt: Documentation for unstable branch

.. |master-docs| image:: http://readthedocs.org/projects/cloudmesh-workflow/badge/?version=main
   :target: http://cloudmesh-workflow.readthedocs.org/en/main/
   :alt: Documentation for main branch

.. |master-status| image:: https://travis-ci.org/cloudmesh/workflow.svg?branch=main
    :target: https://travis-ci.org/cloudmesh/workflow

.. |unstable-status| image:: https://travis-ci.org/cloudmesh/workflow.svg?branch=unstable
    :target: https://travis-ci.org/cloudmesh/workflow
