
# These are just to prevent spelling error bugs,
# the ORGCHART_ prefixes are to prevent accidental
# collisions with other config values
DOTFILE = 'ORGCHART_DOTFILE'
GRAPH = 'ORGCHART_GRAPH'
SVG = 'ORGCHART_SVG'
JQUERY = 'ORGCHART_JQUERY'
JQUERY_MOUSEWHEEL = 'ORGCHART_JQUERY_MOUSEWHEEL'
JQUERY_COLOR = 'ORGCHART_JQUERY_COLOR'
JQUERY_GRAPHVIZ_SVG = 'ORGCHART_JQUERY_GRAPHVIZ_SVG'
REVISION_DIR = 'ORGCHART_REVISION_DIR'


# This seems like the best place to put this, but I don't
# think it's a great place for it.
def set_defaults(config):
    """Fill in some reasonable defaults for config values"""
    defaults = [
        (DOTFILE, 'orgchart.dot'),
        (SVG, 'orgchart.svg'),
        (JQUERY, 'https://code.jquery.com/jquery-2.1.3.min.js'),
        (JQUERY_MOUSEWHEEL, "https://cdn.rawgit.com/jquery/jquery-mousewheel/master/jquery.mousewheel.min.js"),
        (JQUERY_COLOR, "https://cdn.rawgit.com/jquery/jquery-color/master/jquery.color.js"),
        (JQUERY_GRAPHVIZ_SVG, "https://cdn.rawgit.com/mountainstorm/jquery.graphviz.svg/master/js/jquery.graphviz.svg.js"),
        (REVISION_DIR, None)
    ]
    for k, v in defaults:
        config.setdefault(k, v)
