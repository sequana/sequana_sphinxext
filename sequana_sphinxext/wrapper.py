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

    url = f"{url}/{name}/README.md"
    r = requests.get(url)

    title = f"**{name}**\n\n"
    data = r.content.decode()
    rulename_tag = "rule %s" % name

    if "404: Not Found" in data:
        print(f"URL not found: {url}")
        return (
            title
            + f"**docstring for {name} wrapper not yet available (no README.md found)**"
        )

    def get_section(data, section):

        if section in ["Example", "Configuration"]:
            code = f"\n**{section}**\n::\n\n"
        else:
            code = ""

        found = False
        for line in data.split("\n"):
            # while requested section is not found, we parse the data
            if line.startswith(f"# {section}") and not found:
                found = True
                continue
            elif found and line.startswith("# "):
                # a new section is found so, we can stop here and return the
                # current code
                return code
            # the actual section is stored here
            if found:
                code += line + "\n"
        if found:
            return code
        else:
            return ""

    example_code = get_section(data, "Example")
    docstring = get_section(data, "Documentation")
    config = get_section(data, "Configuration")

    rst = docstring + example_code + config

    url = f"https://github.com/sequana/sequana-wrappers/blob/main/wrappers/{name}/README.md"
    rst += f"\n`Extra information on the wrapper page itself. <{url}>`_"
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
