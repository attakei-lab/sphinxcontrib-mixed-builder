from copy import deepcopy
from typing import Dict

from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.util import logging

logger = logging.getLogger(__name__)


class MixedBuilder(Builder):
    name = "mixed"

    default_builder: StandaloneHTMLBuilder = None
    builders: Dict[str, StandaloneHTMLBuilder] = {}

    def __init__(self, app: Sphinx):
        super().__init__(app)
        # Init sub-builders
        config = app.config  # Keep origin config
        for name in self.get_builder_config("builders", "mixed"):
            builder_class = app.registry.builders[name]
            if not issubclass(builder_class, StandaloneHTMLBuilder):
                msg = "MixedBuilder accepts only html-based builders"
                logger.error(msg)
                raise ValueError(msg)
            # To avoid side-effect by pass to sub-builders
            app.config = deepcopy(app.config)
            self.builders[name] = app.create_builder(name)
            if self.default_builder is None:
                self.default_builder = self.builders[name]
        app.config = config  # Recover origin

    def set_environment(self, env):
        super().set_environment(env)
        for builer in self.builders.values():
            builer.env = self.env

    def init(self):
        for builder in self.builders.values():
            self.app.builder = builder
            builder.init()
            self.app.builder = self
        self.templates = self.default_builder.templates

    def get_outdated_docs(self):
        return self.default_builder.get_outdated_docs()

    def prepare_writing(self, docnames):
        for builder in self.builders.values():
            self.app.builder = builder
            builder.prepare_writing(docnames)
            self.app.builder = self

    def get_target_uri(self, docname, typ=None):
        return self.default_builder.get_target_uri(docname, typ)

    def get_builder(self, docname: str) -> StandaloneHTMLBuilder:
        rules = self.get_builder_config("rules", "mixed")
        target = None
        for rule in rules:
            if "equal" in rule and rule["equal"] == docname:
                target = rule["builder"]
                return self.builders[target]
            if "start" in rule and docname.startswith(rule["start"]):
                target = rule["builder"]
                return self.builders[target]
            if "end" in rule and docname.endswith(rule["end"]):
                target = rule["builder"]
                return self.builders[target]
        logger.debug(f"'{docname} is written by '{target or 'DEFAULT'}'")
        return self.default_builder

    def write_doc_serialized(self, docname, doctree):
        for builder in self.builders.values():
            self.app.builder = builder
            builder.write_doc_serialized(docname, doctree)
            self.app.builder = self

    def write_doc(self, docname: str, doctree):
        builder = self.get_builder(docname)
        self.app.builder = builder
        builder.write_doc(docname, doctree)
        self.app.builder = self

    def finish(self):
        for builder in self.builders.values():
            self.app.builder = builder
            builder.finish_tasks = self.finish_tasks
            builder.finish()
            self.app.builder = self

    def cleanup(self):
        for builder in self.builders.values():
            self.app.builder = builder
            builder.cleanup()
            self.app.builder = self


def setup(app: Sphinx):
    """
    Setup function for this extension.
    """
    logger.debug(f"Using {__name__}")
    app.add_config_value("mixed_builders", ["html"], "env")
    app.add_config_value("mixed_rules", [], "env")
    app.add_builder(MixedBuilder)
