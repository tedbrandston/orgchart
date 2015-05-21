
import os
import pydot
import subprocess


def load(dotfile):
    """Get a graph from a file, or a default graph if the file is missing"""
    if os.path.exists(dotfile):
        g = load_from_file(dotfile)
        if g is None:
            raise Exception('File not found: {}'.format(dotfile))
    else:
        g = pydot.Graph(graph_name='orgchart')
    return g


def save(graph, dotfile, svgfile, revision_dir, comment):
    """Convenience wrapper around write, record_revision, and gen_svg"""
    write_to_dotfile(graph, dotfile)
    record_revision(dotfile, revision_dir, comment)
    generate_svg(dotfile, svgfile)


def load_from_file(dotfile):
    """Get a graph from a file"""
    return pydot.graph_from_dot_file(dotfile)


def write_to_dotfile(graph, dotfile):
    """Write a graph into a file"""
    with open(dotfile, 'w') as fp:
        fp.write(graph.to_string())


def record_revision(file, working_dir, comment):
    """Record the current state of file as a revision in version control"""
    subprocess.check_call(
        ['git', 'add', file],
        cwd=working_dir)
    subprocess.check_call(
        ['git', 'commit', '-m', '"{}"'.format(comment)],
        cwd=working_dir)


def generate_svg(dotfile, outfile):
    """Runs 'dot' to generate an svg"""
    subprocess.check_call(['dot', '-Tsvg', dotfile, '-o' + outfile])
