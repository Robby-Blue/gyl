import xml.etree.ElementTree as ET
from gyl.element import Element
from gyl.size import lineheight
from PIL import Image
from io import BytesIO
import cairosvg
import subprocess
import os
import shutil
import hashlib

preample="""
\\documentclass{article}
\\pagestyle{empty}
\\usepackage[english]{babel}
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage{amsmath}
\\usepackage{amssymb}
\\usepackage{mathrsfs}
\\linespread{1}
\\begin{document}
"""

class Latex(Element):

    def __init__(self, content, position, width=None):
        if not width:
            width = lineheight(10)
        super().__init__(position, width)
        self.content = content

        full_latex = preample+ \
            content+"\n"+\
            "\\end{document}"

        cache_folder = os.path.join("scenes", ".cache")
        md5_hash = hashlib.md5(full_latex.encode()).hexdigest()

        svg_file = f"{cache_folder}/{md5_hash}.svg"
        
        if not os.path.exists(svg_file):
            self.create_latex(full_latex)
            self.create_svg(svg_file)
            self.process_svg(svg_file)

        out = BytesIO()
        cairosvg.svg2png(url=svg_file, write_to=out, negate_colors=True)
        self.image = Image.open(out)

    def create_latex(self, full_latex):
        tmp_folder = "latextmp"
        tmp_tex_file = f"{tmp_folder}/tmp.tex"

        if not os.path.exists(tmp_folder):
            os.mkdir(tmp_folder)

        with open(tmp_tex_file, "w") as f:
            f.write(full_latex)

        p = subprocess.Popen(["latex", "-halt-on-error", "-output-directory=latextmp", tmp_tex_file],
            stdout=subprocess.DEVNULL)
        p.wait()

        if p.returncode == 1:
            # todo: maybe make program check installation
            # and equation
            # just execute latex by itself to see it if exists
            # and read the log if theres any error messages
            raise ValueError("Latex failed, check installation and equation")

    def create_svg(self, svg_file):
        expected_output_file = f"latextmp/tmp.dvi"
        p = subprocess.Popen(["dvisvgm", expected_output_file, "-e", "-c", "10,10", "-n", "-o", svg_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
        p.wait()
        shutil.rmtree("latextmp")

    def process_svg(self, svg_file):
        tree = ET.parse(svg_file)
        root = tree.getroot()

        x, y, width, height = [float(n) for n in root.attrib['viewBox'].split(" ")]
        
        # 1%
        x_padding = width*.01
        y_padding = height*.01

        x-=x_padding
        y-=y_padding
        width+=x_padding*2
        height+=y_padding*2
        
        root.attrib['width'] = f"{width}pt"
        root.attrib['height'] = f"{height}pt"
        root.attrib['viewBox'] = f"{x} {y} {width} {height}"

        tree.write(svg_file)

    def draw(self):
        return self.image
    
    def get_size(self):
        return self.image.width, self.image.height
    
    def get_cache(self):
        return {
            "type": "Latex",
            "pos": self.normal_pos(),
            "size": self.normal_width(),
            "content": self.content
        }