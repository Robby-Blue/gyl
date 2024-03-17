from gyl.element import Element
from gyl.size import lineheight
from PIL import Image
from io import BytesIO
import cairosvg
import subprocess
import os
import shutil

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
        
        tmp_folder = "latextmp"
        tmp_tex_file = f"{tmp_folder}/tmp.tex"
        expected_output_file = f"{tmp_folder}/tmp.dvi"

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

        svg_file = f"{tmp_folder}/tmp.svg"

        p = subprocess.Popen(["dvisvgm", expected_output_file, "-n", "-o", svg_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
        p.wait()

        out = BytesIO()
        cairosvg.svg2png(url=svg_file, write_to=out, scale=10)
        self.image = Image.open(out)

        shutil.rmtree(tmp_folder)

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