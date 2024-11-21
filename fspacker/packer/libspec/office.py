from fspacker.packer.libspec.base import ChildLibSpecPacker


class PyMuPdfPacker(ChildLibSpecPacker):
    PATTERNS = dict(pymupdf={"fitz.*/"})
