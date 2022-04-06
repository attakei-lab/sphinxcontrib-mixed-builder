from typing import Dict

from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.util import logging

logger = logging.getLogger(__name__)


class MixedBuilder(Builder):
    name = "mixed"

    defult_builder: StandaloneHTMLBuilder = None
    builders: Dict[str, StandaloneHTMLBuilder] = {}

    def __init__(self, app: Sphinx):
        super().__init__(app)
        # Init sub-builders
        for name in self.get_builder_config("builders", "mixed"):
            builder_class = app.registry.builders[name]
            if not issubclass(builder_class, StandaloneHTMLBuilder):
                msg = "MixedBuilder accepts only html-based builders"
                logger.error(msg)
                raise ValueError(msg)
            self.builders[name] = app.create_builder(name)
            if self.defult_builder is None:
                self.defult_builder = self.builders[name]

    def set_environment(self, env):
        super().set_environment(env)
        for builer in self.builders.values():
            builer.env = self.env

    def init(self):
        for builder in self.builders.values():
            builder.init()
        self.templates = self.defult_builder.templates

    def get_outdated_docs(self):
        return self.defult_builder.get_outdated_docs()

    def prepare_writing(self, docnames):
        for builder in self.builders.values():
            builder.prepare_writing(docnames)

    def get_target_uri(self, docname, typ=None):
        return self.defult_builder.get_target_uri(docname, typ)

    def write_doc_serialized(self, docname, doctree):
        for builder in self.builders.values():
            builder.write_doc_serialized(docname, doctree)

    def write_doc(self, docname, doctree):
        rules = self.get_builder_config("rules", "mixed")
        target = None
        for rule in rules:
            if "docname" in rule and rule["docname"] == docname:
                target = rule["builder"]
                break
        logger.debug(f"'{docname} is written by '{target or 'DEFAULT'}'")
        if target is None:
            self.defult_builder.write_doc(docname, doctree)
        elif target in self.builders:
            self.builders[target].write_doc(docname, doctree)
        else:
            raise Exception("Invalid builder")

    def finish(self):
        for builder in self.builders.values():
            builder.finish_tasks = self.finish_tasks
            builder.finish()

    def cleanup(self):
        for builder in self.builders.values():
            builder.cleanup()


def setup(app: Sphinx):
    """
    Setup function for this extension.
    """
    logger.debug(f"Using {__name__}")
    app.add_config_value("mixed_builders", ["html"], "env")
    app.add_config_value("mixed_rules", [], "env")
    app.add_builder(MixedBuilder)
