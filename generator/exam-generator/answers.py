from textwrap import dedent
import pylatex as ptex
from .generator_config import GeneratorConfig


class Answers(ptex.lists.Description):
    """
    A class representing a custom LaTeX environment.
    This class represents a custom LaTeX environment named
    ``answers``.
    """

    _latex_name = "answers"

    @classmethod
    def create_env_variable(cls, config: GeneratorConfig):
        return ptex.UnsafeCommand(
            "newenvironment",
            "answers",
            extra_arguments=[
                dedent(
                    rf"""
                    \begin{{itemize}}
                        \setlength{{\itemsep}}{{{config.answers_interline}pt}}
                        \fontsize{{{int(config.font_size)}}}{{{int(config.font_size*1.2)}}}
                        \selectfont"""
                ),
                dedent(
                    r"""
                    \end{itemize}
                    """
                ),
            ],
        )
