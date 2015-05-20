
import os
import pydot
import subprocess


def load(dotfile):
    """Get a graph from a file, or a default graph if the file is missing"""
    if os.path.exists(dotfile):
        g = load_from_file(dotfile)
    else:
        g = pydot.Graph(graph_name='orgchart')
    return g


def load_from_file(dotfile):
    """Get a graph from a file"""
    return pydot.graph_from_dot_file(dotfile)


def write_to_dotfile(graph, dotfile):
    """Write a graph into a file"""
    with open(dotfile, 'w') as fp:
        fp.write(graph.to_string())


def generate_svg(dotfile, outfile):
    """Runs 'dot' to generate an svg"""
    subprocess.check_call(['dot', '-Tsvg', dotfile, '-o' + outfile])