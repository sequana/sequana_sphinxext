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
:class:`sequana.snaketools.Module` class

"""
from docutils.nodes import Body, Element
import requests

from sphinx.util.docutils import SphinxDirective


def get_rule_doc(name):
    """Decode and return the docstring(s) of a sequana/snakemake rule."""
    try:
        from sequana_pipetools import Module
        rule = Module(name)
        filename = rule.path + "/%s.rules" % name
        data = open(filename, "r").read()
    except ImportError:
        url = "https://raw.githubusercontent.com/sequana/sequana/master/sequana/rules/"
        if name.count("/") == 0:
            url = f"{url}/{name}/{name}.rules"
        elif name.count("/") == 1:
            # this is a rule with a version name/version/name.rules
            # and users provided name/version
            name, version = name.split("/")
            url = f"{url}/{name}/{version}/{name}.rules"
        r = requests.get(url)
        data = r.content.decode()
        if "404: Not Found" in data:
            print(f"URL not found: {url}")
            return (
                  f"**docstring for {name} not found**"
             )

    # Try to identify the rule and therefore possible docstring
    # It may be a standard rule or a dynamic rule !
    # standard one
    if name.endswith("_dynamic"):
        name = name[:-8]
    rulename_tag = "rule %s" % name
    if rulename_tag in data:
        data = data.split(rulename_tag, 1)[1]
    else:
        return "no docstring found for %s " % name

    # Find first """ or ''' after the rule definition
    single = data.find("'''")
    double = data.find('"""')
    if single > 0 and double > 0:
        if single > double:
            quotes = '"""'
        else:
            quotes = "'''"
    elif single > 0:
        quotes = "'''"
    elif double > 0:
        quotes = '"""'
    else:
        return "no docstring found for %s " % name

    start = data.find(quotes)
    end = data[start + 3 :].find(quotes) + start + 3

    if end == -1 or end < start:
        return "no end of docstring found for %s " % name

    docstring = data[start + 3 : end]
    return docstring


class snakemake_base(Body, Element):
    def dont_traverse(self, *args, **kwargs):
        return []


class snakemake_rule(snakemake_base):
    pass


def run(content, node_class, state, content_offset):
    node = node_class("")  # shall we add something here ?
    name = content[0]
    try:
        node.rule_docstring = get_rule_doc(name)
    except Exception:
        node.rule_docstring = f"Could not read or interpret documentation for {name}"
    state.nested_parse(content, content_offset, node)
    return [node]


class SnakemakeDirective(SphinxDirective):

    has_content = True

    def run(self):
        return run(self.content, snakemake_rule, self.state, self.content_offset)


def setup(app):

    setup.app = app
    setup.config = app.config
    setup.confdir = app.confdir
    app.add_directive("snakemakerule", SnakemakeDirective)

    # Add visit/depart methods to HTML-Translator:
    def visit_perform(self, node):
        # Ideally, we should use sphinx but this is a simple temporary solution
        from docutils import core
        from docutils.writers.html4css1 import Writer

        w = Writer()
        try:
            res = core.publish_parts(node.rule_docstring, writer=w)["html_body"]
            self.body.append('<div class="snakemake">' + res + "</div>")
            node.children = []
        except Exception as err:
            print(err)
            self.body.append('<div class="snakemake"> no docstring </div>')

    def depart_perform(self, node):
        node.children = []

    def depart_ignore(self, node):
        node.children = []

    def visit_ignore(self, node):
        node.children = []

    app.add_node(
        snakemake_rule,
        html=(visit_perform, depart_perform),
        latex=(visit_ignore, depart_ignore),
    )

    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
