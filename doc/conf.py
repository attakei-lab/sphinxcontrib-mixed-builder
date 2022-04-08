# -- Path setup

# -- Project information
project = "sphinxcontrib-mixer"
copyright = "2022, Kazuya Takei"
author = "Kazuya Takei"
release = "0.2.0"
language = "ja"

# -- General configuration
extensions = [
    "sphinx.ext.intersphinx",
    "sphinxcontrib.mixed_builder",
    "sphinx_revealjs",
    "sphinx_rtd_theme",
]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# -- Options for REVEALJS output
revealjs_static_path = ["_static"]
revealjs_style_theme = "black"
revealjs_script_conf = {
    "controls": True,
    "progress": True,
    "history": True,
    "center": True,
    "transition": "none",
}
revealjs_script_plugins = [
    {
        "name": "RevealHighlight",
        "src": "revealjs4/plugin/highlight/highlight.js",
    },
]
revealjs_css_files = [
    "revealjs4/plugin/highlight/zenburn.css",
]

# -- Options for MIXED output
mixed_builders = ["dirhtml", "revealjs"]
mixed_rules = [
    {
        "start": "slides/",
        "builder": "revealjs",
    }
]


def setup(app):
    app.add_object_type(
        "confval",
        "confval",
        objname="configuration value",
        indextemplate="pair: %s; configuration value",
    )
