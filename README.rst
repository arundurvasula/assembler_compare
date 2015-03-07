===============================
Assembler Compare
===============================

.. image:: https://img.shields.io/travis/arundurvasula/assembler_compare.svg
        :target: https://travis-ci.org/arundurvasula/assembler_compare

.. image:: https://img.shields.io/pypi/v/assembler_compare.svg
        :target: https://pypi.python.org/pypi/assembler_compare


Software to compare sequence assemblers automatically

* Free software: BSD license
* Documentation: https://assembler_compare.readthedocs.org.

Note: this program uses eval and call when running assemblers. DON'T run any config files that contains `rm` in it (you shouldn't have `rm` there anyways).

Features
--------

* TODO

Contributing
--------
In order to add an assembler to assember compare, you need to do two things

1. add a function to call the program. See the section `assemblers in assembler-compare.py for examples. The function should be the name of the assembler and the variables `k`, `data`, and `outprefix` must be supplied to it. 
2. add it to the dictionary of `known_assemblers` in the main function. It should be something like `"assembler-name":assembler-name(k, data, outprefix)`
