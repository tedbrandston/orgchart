
# These are just to prevent spelling error bugs
DOTFILE = 'ORGCHART_DOTFILE'
GRAPH = 'ORGCHART_GRAPH'
SVG = 'ORGCHART_SVG'


# This seems like the best place to put this, but I don't
# think it's a great place for it.
def set_defaults(config):
    """Fill in some reasonable defaults for config values"""
    defaults = [
        (DOTFILE, 'orgchart.dot'),
        (SVG, 'orgchart.svg'),
    ]
    for k, v in defaults:
        config.setdefault(k, v)
