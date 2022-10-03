import pylatex as ptex
from .logger import logger
from .generator_config import GeneratorConfig
from .answers import Answers
from .rules import Rules
from .generator_config import Font


class ExamDocument(ptex.Document):
    def __init__(self, config: GeneratorConfig):
        self.config = config
        geometry_options = self.get_geometry_options()

        super().__init__(geometry_options=geometry_options)

        self.documentclass = ptex.Command(
            "documentclass",
            options=["a4paper", f"{self.config.font_size}pt"],
            arguments=["article"],
        )
        self.set_font(self.config.font)
        self.set_section_font(self.config.font_size)
        self.set_question_interline()
        self.set_footer()
        self.packages.append(ptex.Package("enumitem"))
        self.packages.append(ptex.Package("graphicx"))
        self.append(Answers.create_env_variable(self.config))
        self.append(Rules.create_env_variable(self.config))

    def set_font(self, font: Font):
        self.packages.remove(ptex.Package("textcomp"))
        self.packages.append(ptex.Package(font.value))

    def set_question_interline(self):
        self.preamble.append(ptex.Command("setlength", arguments=[ptex.Command("parindent"), "0pt"]))
        self.preamble.append(ptex.Command("setlength", arguments=[ptex.Command("parskip"), f"{self.config.question_interline}pt"]))
        pass

    def set_section_font(self, font_size: int):
        logger.debug(f"Setting section title font to {self.config.font_size}pt")
        self.packages.append(ptex.Package("sectsty"))
        self.preamble.append(
            ptex.Command(
                "sectionfont",
                ptex.NoEscape(
                    f"\\normalfont\\fontsize{{{self.config.font_size}pt}}{{10}}\\bfseries"
                ),
            )
        )

    def set_footer(self):
        self.packages.append(ptex.Package("fancyhdr"))
        self.append(ptex.Command("fancyhf",arguments=[""]))
        self.append(ptex.Command("pagestyle", arguments=["fancy"]))
        # \lfoot{UID: 30f4b51e-bd20-4b70-8fb0-3a7cf014f21d}
        # \rfoot{\thepage}
        # \fontfamily{qcr}\selectfont
        #\fontsize{15pt}{18pt}
        footer_style = f"{ptex.Command('fontsize',arguments=['15pt', '18pt']).dumps()} \
            {ptex.Command('fontfamily', arguments='qcr').dumps()} \
            {ptex.Command('selectfont').dumps()} \
            {ptex.Command('large').dumps()}"
        self.append(ptex.Command("lfoot", arguments=[ptex.NoEscape(f"{footer_style} UUID: {self.config.exam_id}")]))
        self.append(ptex.Command("rfoot", arguments=[ptex.NoEscape(rf"{footer_style}\thepage")]))

    def get_geometry_options(self):
        return {
            "tmargin": f"{self.config.top_margin}cm",
            "lmargin": f"{self.config.left_margin}cm",
        }
