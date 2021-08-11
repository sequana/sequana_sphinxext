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
a sequana wrappers Snakefile .

::

    .. sequana_wrapper: multiqc

The name must be a valid sequana wrappers

"""
import requests
from docutils.nodes import Body, Element


# from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective


def get_rule_doc(name):
    """Decode and return the docstring(s) of a sequana wrapper."""

    url = "https://raw.githubusercontent.com/sequana/sequana-wrappers/main/wrappers"
    url = f"{url}/{name}/example.smk"
    r = requests.get(url)

    title = f"**{name}**\n\n"
    data = r.content.decode()
    # Try to identify the rule and therefore possible docstring
    # It may be a standard rule or a dynamic rule !
    # standard one
    rulename_tag = "rule %s" % name
    if "404: Not Found" in data:
        print(f"URL not found: {url}")
        return (
            title
            + f"**docstring for {name} wrapper not yet available (no example.smk found)**"
        )
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
    code = data[end + 3 :]
    code = "\n".join(["    " + line for line in code.split("\n")])
    rst = title + docstring + f"\nExample:: \n\n    rule {name}:" + code
    return rst


class snakemake_base(Body, Element):
    def dont_traverse(self, *args, **kwargs):
        return []


class sequana_wrapper(snakemake_base):
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
        return run(self.content, sequana_wrapper, self.state, self.content_offset)


def setup(app):

    setup.app = app
    setup.config = app.config
    setup.confdir = app.confdir
    app.add_directive("sequana_wrapper", SnakemakeDirective)

    # Add visit/depart methods to HTML-Translator:
    def visit_perform(self, node):
        # Ideally, we should use sphinx but this is a simple temporary solution
        from docutils import core
        from docutils.writers.html4css1 import Writer

        w = Writer()
        try:
            res = core.publish_parts(node.rule_docstring, writer=w)["html_body"]
            self.body.append('<div class="sequana_wrapper">' + res + "</div><br>")
            node.children = []
        except Exception as err:
            print(err)
            self.body.append('<div class="sequana_wrapper"> no docstring </div>')

    def depart_perform(self, node):
        node.children = []

    def depart_ignore(self, node):
        node.children = []

    def visit_ignore(self, node):
        node.children = []

    app.add_node(
        sequana_wrapper,
        html=(visit_perform, depart_perform),
        latex=(visit_ignore, depart_ignore),
    )

    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
