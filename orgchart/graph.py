
import os
import pydot
import re
import subprocess


class Graph():
    """Encapsulates the various things one does to the orgchart graph

    Things to keep in mind (enforce):
    * There should never more than one node with a given name.
    * Since we're doing fancy stuff in labels we will need to eliminate/escape
      certain characters ([]{}| ) from names and tags.
    """
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

        self._graph = None

        self.reload()

    @staticmethod
    def _escape_name_or_tag(name):
        """
        Because of the fancy things we do to the labels, names and tags have
        to be rid of any characters that would mess with the labels.
        """
        # replace any unescaped []{}| or   (space) with an escaped one
        return re.sub(r'(?<!\\)[[\]{}| ]', r'\\\g<0>', name)

    def _get_or_create_person(self, name):
        """Return a node named name, using an existing one if possible.

        Seems like the best way to ensure duplicate nodes never occur
        is to avoid an interface that allows the creation of a node
        separate from the check for a pre-existing node.
        """
        name = self._escape_name_or_tag(name)
        nodes = self._graph.get_node(name)
        if len(nodes) == 0:
            label = self._pack_person_label(name, [])
            node = pydot.Node(name, label=label, shape="Mrecord")
            self._graph.add_node(node)
            return node
        elif len(nodes) == 1:
            return nodes[0]
        else:
            # TODO: Log instead of crashing.
            # This _should_ be impossible. The only ways to create nodes
            # are on load of graph and here, and both are guarded.
            raise Exception('Expected one person named {}, found {}'
                .format(name, len(nodes)))

    @staticmethod
    def _unpack_person_label(label):
        """Handle the way tags on a person are encoded in a label
        on a record.

        returns a pair of person name and list of tags on person
        """
        _person_label_regex = re.compile(
            "\{\s*(?P<name>\w*)\s*\|\s*\{\s*(?P<tags>[\w\n]*)\s*\}\s*\}")
        # JIC
        label = label.strip()
        match = _person_label_regex.match(label)
        if match:
            name = match.group('name')
            tags = match.group('tags')
            if tags != '':
                tags = tags.split('\n')
            else:
                tags = []
            return name, tags
        else:
            return None, None

    def _get_person_tags(self, name):
        """Return the list of tags on a node"""
        node = self._get_or_create_person(name)
        _, tags = self._unpack_person_label(node.get_label())
        return node, tags

    @staticmethod
    def _pack_person_label(name, tags):
        """Handle the way tags on a person are encoded in a label
        on a record.

        I would probably have this, and some of the other person-methods
        on a Person(Node) class, but I'm a bit nervous about shadowing
        methods on Node.

        returns a string to be set as the label attribute on a Node
        """
        return "{{ {name} |{{ {tags} }}}}".format(
            name=name,
            tags='\n'.join(tags))

    def _set_person_tags(self, node, name, tags):
        """Set the list of tags on a node"""
        new_node_label = self._pack_person_label(name, tags)
        node.set_label(new_node_label)

    def ensure_person_exists(self, name):
        """Create a person, if they don't already exist"""
        self._get_or_create_person(name)

    def list_people(self):
        """Return a list of the names of all the people"""
        return [node.get_name() for node in self._graph.get_nodes()]

    def delete_person(self, name):
        """Remove a person from the graph"""
        self._graph.del_node(name)
        # TODO: delete all links to and from this person?

    def list_person_tags(self, name):
        """Return the list of tags on a person"""
        _, tags = self._get_person_tags(name)
        return tags

    def tag_person(self, name, tag):
        """Add a tag to a person"""
        tag = self._escape_name_or_tag(tag)
        node, tags = self._get_person_tags(name)
        tags.append(tag)
        self._set_person_tags(node, name, tags)

    def untag_person(self, name, tag):
        """Remove a tag from a person"""
        node, tags = self._get_person_tags(name)
        # err on the side of removing one accidental duplicate (if),
        # or all of something someone is intentionally spamming (while)?
        if tag in tags:
            idx = tags.index(tag)
            tags = tags[:idx] + tags[idx+1:]
        self._set_person_tags(node, name, tags)

    def link_people(self, name_src, name_dst, relationship):
        """Add a link between two nodes"""
        self.ensure_person_exists(name_src)
        self.ensure_person_exists(name_dst)
        self._graph.add_edge(pydot.Edge(
            src=name_src,
            dst=name_dst,
            label=relationship))

    def delete_link(self, name_src, name_dst, relationship):
        """Remove a link between two nodes

        If multiple links exist with the same relationship,
        removes one of them.
        """
        # find the index of a link that matches relationship
        edges = self._graph.get_edge(name_src, name_dst)
        edges = filter(lambda e: e.get_label() == relationship, edges)
        # If none match, it's probably because multiple
        # people were editing at the same time
        if len(edges) == 0:
            return
        # If there are multiple, I think it's fine to just delete the first
        edge = edges[0]

        self._graph.del_edge(edge)

    def list_links_between(self, person_a, person_b):
        """Return a list of all links between two nodes in either direction"""
        # Do I need to make the entries unique? probably.
        edges = self._graph.get_edge(person_a, person_b)
        return [edge.get_label() for edge in edges]

    def reload(self):
        """Re-read graph from file, or make a new graph if file is missing"""
        # TODO: investigate why this is run twice at startup?
        if os.path.exists(self._dotfile):
            g = pydot.graph_from_dot_file(self._dotfile)
            if g is None:
                raise Exception('Malformed file: {}'.format(self._dotfile))
            # Might want to move this into a verify() or something?
            # To ensure that we only ever have one node with a given name:
            nodes = g.get_nodes()
            all_names = [node.get_name() for node in nodes]
            _ = set()
            duplicates = set(x for x in all_names if x in _ or _.add(x))
            if len(all_names) != len(set(all_names)):
                raise Exception(
                    'Multiple nodes with the same name specified: {}'
                        .format(list(duplicates)))
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
