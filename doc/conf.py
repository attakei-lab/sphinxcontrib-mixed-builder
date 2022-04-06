# -- Path setup

# -- Project information
project = "sphinxcontrib-mixer"
copyright = "2022, Kazuya Takei"
author = "Kazuya Takei"
release = "0.1.0"

# -- General configuration
extensions = ["sphinxcontrib.mixed_builder", "sphinx_revealjs", "sphinx_rtd_theme"]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# -- Options for REVEALJS output
revealjs_context = {}

# -- Options for MIXED output
mixed_builders = ["html", "revealjs"]
mixed_rules = [
    {
        "docname": "test",
        "builder": "revealjs",
    }
]
