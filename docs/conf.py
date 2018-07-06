from pkg_resources import get_distribution

# -- Project information -----------------------------------------------------

project = 'aap-client-python'
copyright = '2018, EMBL-EBI'
author = 'EMBL-EBI'

# The full version, including alpha/beta/rc tags
release = get_distribution(project).version
# The short X.Y version
version = '.'.join(release.split('.')[:2])

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = []
source_suffix = '.rst'
master_doc = 'index'

language = None

pygments_style = 'pastie'

autoclass_content = "both"  # include both class docstring and __init__

autodoc_default_flags = [
    # Make sure that any autodoc declarations show the right members
    "members",
    "inherited-members",
    "private-members",
    "show-inheritance",
]

autosummary_generate = True  # Make _autosummary files and include them
autosummary_default_flags = ['members']

napoleon_numpy_docstring = False  # Force consistency, leave only Google
napoleon_use_rtype = False  # More legible

html_theme = 'alabaster'
html_theme_options = {
    "github_user": "EMBL-EBI-TSI",
    "github_repo": project,
    "description": "Integrates AAP into your code",
    "travis_button": "true",
    "badge_branch": "master",
}
html_sidebars = {
    "**": ["about.html", "localtoc.html", "relations.html", "searchbox.html", "donate.html"]
}
html_static_path = ['_static']
htmlhelp_basename = "{}doc".format(project)


latex_documents = [
    (master_doc, 'aap-client-python.tex', 'aap-client-python Documentation',
     'EMBL-EBI', 'manual'),
]

man_pages = [
    (master_doc, 'aap-client-python', 'aap-client-python Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'aap-client-python', 'aap-client-python Documentation',
     author, 'aap-client-python', 'One line description of project.',
     'Miscellaneous'),
]
