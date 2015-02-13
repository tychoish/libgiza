=======================================
``libgiza`` -- Build Automation Toolkit
=======================================

.. image:: https://travis-ci.org/tychoish/libgiza.svg?branch=master
    :target: https://travis-ci.org/tychoish/libgiza

``libgiza`` is a Python package that provides a collection of base
classes used in the construction of `giza
<https://pypi.python.org/pypi/giza>`_, which is a documentation build
automation tool. ``libgiza`` provides two groups of functionality:

1. Tools for defining and executing parallel builds. See
   ``libgiza.app`` for the primary interface, along with the
   components ``libgiza.task`` and ``libgiza.pool``.

2. Tools for content generation. See ``libgiza.inheritance`` for these
   classes.
