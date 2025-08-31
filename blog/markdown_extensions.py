import xml.etree.ElementTree as etree

from markdown import Markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


class ImageSizesProcessor(Treeprocessor):
    def run(self, root: etree.Element) -> etree.Element | None:
        for image in root.iter("img"):
            if "sizes" not in image.attrib:
                image.set("sizes", "(max-width: 768px) 100vw")
        return root


class ImageSizesExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        md.treeprocessors.register(ImageSizesProcessor(md), "imagesizes", 15)
