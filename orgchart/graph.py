
import os
import pydot
import subprocess


class Graph():
    """Encapsulates the various things one does to the orgchart graph"""
    def __init__(self, dotfile, svgfile, revision_dir):
        """
        @param dotfile The graphviz "dot" format file to read/write
                       the graph from/to
        @param svgfile The svg file to write the visual representation
                       of the graph into
        @param revision_dir The directory in which revision control
                            takes place
        """
        self._dotfile = dotfile
        self._svgfile = svgfile

        if revision_dir is None:
            raise Exception("No directory specified for revision control")
        self._revision_dir = revision_dir

        self._graph = self.reload()

    def reload(self):
        """Re-read graph from file, or make a new graph if file is missing"""
        if os.path.exists(self._dotfile):
            g = pydot.graph_from_dot_file(self._dotfile)
            if g is None:
                raise Exception('Malformed file: {}'.format(self._dotfile))
        else:
            g = pydot.Graph(graph_name='orgchart')
        self._graph = g

    def save(self, comment):
        """Convenience wrapper around write, record_revision, and gen_svg"""
        self.write(self._dotfile)
        self.record_revision(comment)
        self.generate_svg()

    def write(self, dotfile):
        """Write the in-memory graph to a file"""
        with open(dotfile, 'w') as fp:
            fp.write(self._graph.to_string())

    def record_revision(self, comment):
        """Record the current on-disk graph as a revision in version control
        """
        subprocess.check_call(
            ['git', 'add', self._dotfile],
            cwd=self._revision_dir)
        subprocess.check_call(
            ['git', 'commit', '-m', '"{}"'.format(comment)],
            cwd=self._revision_dir)

    def generate_svg(self):
        """Runs 'dot' to generate an svg"""
        subprocess.check_call(
            ['dot', '-Tsvg', self._dotfile, '-o' + self._svgfile])
