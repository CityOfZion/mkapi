from mkapi.core.node import get_node, is_member


def test_generator():
    node = get_node("google_style.gen")
    assert node.object.kind == "generator"


def test_class():
    node = get_node("google_style.ExampleClass")
    assert node.object.prefix == "google_style"
    assert node.object.name == "ExampleClass"
    assert node.object.kind == "class"
    assert len(node) == 3
    p = node.members[-1]
    assert p.object.type.name == "list of int"
    assert p.docstring.sections[0].markdown.startswith("Read-write property")


def test_dataclass():
    node = get_node("google_style.ExampleDataClass")
    assert node.object.prefix == "google_style"
    assert node.object.name == "ExampleDataClass"
    assert node.object.kind == "dataclass"


def test_is_member_private():
    class A:
        def _private():
            pass

        def func():
            pass

    class B(A):
        pass

        def _private():
            pass

    assert is_member(A._private) == -1
    assert is_member(A.func) == 0


def test_is_member_source_file_index():
    node = get_node("mkapi.core.node.Node")
    assert node["__getitem__"].sourcefile_index == 1

    node = get_node("mkapi.core.base")
    assert node["Inline"].sourcefile_index == 0


def test_get_markdown():
    node = get_node("mkapi.core.base.Base")
    markdown = node.get_markdown()
    parts = [x.strip() for x in markdown.split("<!-- mkapi:sep -->")]
    x = "[mkapi.core.base](!mkapi.core.base).[Base](!mkapi.core.base.Base)"
    assert parts[0] == x
    assert parts[1] == "Base class."
    assert parts[6] == "Sets `html` attribute."

    markdown = node.get_markdown(level=2)
    parts = [x.strip() for x in markdown.split("<!-- mkapi:sep -->")]
    x = "[mkapi.core.base](!mkapi.core.base).[Base](!mkapi.core.base.Base)"
    assert parts[0] == "## " + x

    def callback(base):
        return "123"

    markdown = node.get_markdown(callback=callback)
    parts = [x.strip() for x in markdown.split("<!-- mkapi:sep -->")]
    assert all(x == "123" for x in parts)


def test_set_html_and_render():
    node = get_node("mkapi.core.base.Base")
    markdown = node.get_markdown()
    sep = "<!-- mkapi:sep -->"
    n = len(markdown.split(sep))
    html = sep.join(str(x) for x in range(n))
    node.set_html(html)
    for k, x in enumerate(node):
        assert x.html == str(k)

    html = node.render()

    assert html.startswith('<div class="mkapi-node" id="mkapi.core.base.Base">')
    assert 'mkapi-object-kind-dataclass">DATACLASS</div>' in html
    assert '<div class="mkapi-section-body">1</div>' in html
    assert '<span class="mkapi-args-desc">2</span></li>' in html
    assert '<code class="mkapi-object-name">set_html</code>' in html
    assert '<li><code class="mkapi-args-name">html</code>' in html


def test_package():
    node = get_node("mkapi.core")
    assert node.object.kind == 'package'
