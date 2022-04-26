from textwrap import dedent
import pylatex as ptex
from .generator_config import GeneratorConfig


class Rules(ptex.lists.Description):
    """
    A class representing a custom LaTeX environment.
    This class represents a custom LaTeX environment named
    ``rules``.
    """

    _latex_name = "rules"

    @classmethod
    def create_env_variable(cls, config: GeneratorConfig):
        return ptex.UnsafeCommand(
            "newenvironment",
            "rules",
            extra_arguments=[
                dedent(
                    rf"""
                    \begin{{itemize}}
                        \setlength{{\itemsep}}{{{config.rules_interline}pt}}
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
