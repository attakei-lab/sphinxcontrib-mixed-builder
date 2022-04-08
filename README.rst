===========================
sphinxcontrib-mixed-builder
===========================

.. note:: This is experimental library.

Overview
========

This is Sphinx extension to generate mixied contents by multiple builders.

You can generate these contents by one builder:

- Main contents are regular HTML files.
- Under ``/slides/`` are Reveal.js presentations.

Installation
============

.. code-block:: console

   pip install --find-links=https://github.com/attakei-lab/sphinxcontrib-mixed-builder/releases sphinxcontrib-mixed-builder

Usage
=====

After configure, run ``make mixed``

.. code-block:: python

   extensions = [
       "sphinxcontrib.mixed_builder",
       "sphinx_revealjs",
   ]

   mixed_builders = ["html", "revealjs"]
   mixed_rules = [
       {
           "equal": "index",
           "builder": "html",
       },
       # TODO: Not implemented
       {
           "start": "slides/",
           "builder": "revaljs"
       },
   ]

Example
=======

See `doc <doc/>`_.
