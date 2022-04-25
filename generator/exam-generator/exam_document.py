import pylatex as ptex
from .logger import logger
from .generator_config import GeneratorConfig
from .answers import Answers
from .rules import Rules

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
        self.set_section_font(self.config.font_size)
        self.packages.append(ptex.Package("enumitem"))
        self.packages.append(ptex.Package("graphicx"))
        self.append(Answers.create_env_variable(self.config))
        self.append(Rules.create_env_variable(self.config))

    def set_section_font(self, font_size: int):
        logger.debug(f"Setting section title font to {font_size}pt")
        self.packages.append(ptex.Package('sectsty'))
        self.preamble.append(ptex.Command("sectionfont", ptex.NoEscape(f"\\normalfont\\fontsize{{{font_size}pt}}{{10}}\\bfseries")))

    def get_geometry_options(self):
        return {
            "tmargin": f"{self.config.top_margin}cm",
            "lmargin": f"{self.config.left_margin}cm"
        }
