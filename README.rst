=======================================
``libgiza`` -- Build Automation Toolkit
=======================================

.. image:: https://travis-ci.org/tychoish/libgiza.svg?branch=master
    :target: https://travis-ci.org/tychoish/libgiza

``libgiza`` is a Python package that provides a collection of base
classes used in the construction of `giza
<https://pypi.python.org/pypi/giza>`_, which is a documentation build
automation tool. ``libgiza`` provides several of functionality:

1. Tools for defining and running build tasks in parallel builds. See
   ``libgiza.app`` for the primary interface, along with the
   components ``libgiza.task`` and ``libgiza.pool``. Think of this as
   a worker pool on steroids.

2. Tools for content generation. See ``libgiza.inheritance`` for these
   classes. This is the underlying toolkit for the defining feature of
   giza, which makes it possible to describe semi-structured content
   and generate content from base templates or using existing
   content as a basis for related content. 

3. A Python interface for common git operations. The ``GitRepo()``
   class in ``libgiza.git`` wraps the ``git`` command internally, but
   provides methods for many common operations and more reasonable 
   output/error handling

4. A base class for defining classes for "configuration" data. See the
   ``ConfigurationBase`` and ``RecursiveConfigurationBase`` in
   ``libgiza.config``. These provide support for serialization and
   de-serialization, easy ingestion from either files or
   dictionaries, and using default python ``@property`` defined
   getters and setters for more strict input validation and type
   checking.
   
