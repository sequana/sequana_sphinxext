#
#  This file is part of Sequana software
#
#  Copyright (c) 2016-2021 - Sequana Dev Team (https://sequana.readthedocs.io)
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  Website:       https://github.com/sequana/sequana
#  Documentation: http://sequana.readthedocs.io
#  Contributors:  https://github.com/sequana/sequana/graphs/contributors
##############################################################################
"""sequana wrappers

Defines a docutils directive for inserting simple docstring extracting from
a snakemake rule (from sequana project).

::

    .. snakemakerule: dag

The name must be a valid sequana rule in the rules directory accesible via the
:class:`sequana_pipetools.snaketools.Module` class

"""
from docutils.nodes import Body, Element
import urllib
from urllib.error import HTTPError
from sphinx.util.docutils import SphinxDirective


def get_rule_doc(name):
    """Decode and return the docstring(s) of a sequana/snakemake rule."""

    url = "https://raw.githubusercontent.com/sequana/{}/master/README.rst".format(name)

    try:
        data = urllib.request.urlopen(url).read().decode("utf8")
    except HTTPError:
        return f"Could not access to {url}"

    try:
        from sequana_pipetools import Module
        m = Module(f"pipeline:{name}")
        version = m.version
    except ValueError:
        version = "Not installed locally."
    except ImportError:
        version = "?"

    docstring = "**current version**:{}\n\n{}".format(version, data)

    return docstring


class snakemake_base(Body, Element):
    def dont_traverse(self, *args, **kwargs):
        return []


class sequana_pipeline_rule(snakemake_base):
    pass


def run(content, node_class, state, content_offset):
    node = node_class("")  # shall we add something here ?
    node.rule_docstring = get_rule_doc(content[0])
    state.nested_parse(content, content_offset, node)
    return [node]


class PipelineDirective(SphinxDirective):
    has_content = True

    def run(self):
        return run(self.content, sequana_pipeline_rule, self.state, self.content_offset)


def setup(app):
    app.add_directive("sequana_pipeline", PipelineDirective)

    # Add visit/depart methods to HTML-Translator:
    def visit_perform(self, node):
        # Ideally, we should use sphinx but this is a simple temporary solution
        from docutils import core
        from docutils.writers.html4css1 import Writer

        w = Writer()
        try:
            res = core.publish_parts(node.rule_docstring, writer=w)["html_body"]
            self.body.append('<div class="">' + res + "</div>")
            node.children = []
        except Exception as err:
            print(err)
            self.body.append('<div class=""> no docstring </div>')

    def depart_perform(self, node):
        node.children = []

    def visit_ignore(self, node):
        node.children = []

    def depart_ignore(self, node):
        node.children = []

    app.add_node(
        sequana_pipeline_rule,
        html=(visit_perform, depart_perform),
        latex=(visit_ignore, depart_ignore),
    )
