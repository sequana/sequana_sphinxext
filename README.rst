Sequana Sphinxext
##################


.. image:: https://badge.fury.io/py/sequana-sphinxext.svg
    :target: https://pypi.python.org/pypi/sequana-sphinxext

.. image:: https://github.com/sequana/sequana_sphinxext/actions/workflows/main.yml/badge.svg?branch=master
    :target: https://github.com/sequana/sequana_sphinext/actions/workflows/main.yml

.. image:: https://coveralls.io/repos/github/sequana/sequana_sphinxext/badge.svg?branch=master
    :target: https://coveralls.io/github/sequana/sequana_sphinxext?branch=master 

.. image:: http://joss.theoj.org/papers/10.21105/joss.00352/status.svg
   :target: http://joss.theoj.org/papers/10.21105/joss.00352
   :alt: JOSS (journal of open source software) DOI


:Python version:  3.7.3, 3.8 ,3.9
:Status: Production
:Issues: Please fill issues `On github <https://github.com/sequana/sequana/issues>`_
:How to cite: Citations are important for us to carry on developments.
    For Sequana library (including the pipelines), please use

    Cokelaer et al, (2017), 'Sequana': a Set of Snakemake NGS pipelines, Journal of
    Open Source Software, 2(16), 352, `JOSS DOI doi:10.21105/joss.00352 <https://joss.theoj.org/papers/10.21105/joss.00352>`_
 

The sequana_sphinxext  package is used exclusively to provide Sphinx extensions for the Sequana
project. **Sequana** includes a set of pipelines related to NGS (new generation sequencing) including quality control, variant calling, coverage, taxonomy, transcriptomics. **Please see the** `documentation <http://sequana.readthedocs.org>`_ for an up-to-date status.

We have three sphinx extension to be added in your Sphinx configuration files in the extensions list::

    extensions += [
        "sequana_sphinxext.snakemakerule",
        "sequana_sphinxext.pipeline",
        "sequana_sphinxext.wrapper"]

You can then include a wrapper from  `sequana wrappers <https://github.com/sequana/sequana-wrappers>`_ using e.g.::

    .. sequana_wrapper:: fastqc

or a rule from Sequana::

    .. snakemakerule:: fastq_sampling

or a pipeline from sequana::

    .. sequana_pipeline:: demultiplex





