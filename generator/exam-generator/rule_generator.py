import typing as tp
import pylatex as ptex
from .generator_config import GeneratorConfig, RuleStructure
from .logger import logger


class RuleGenerator:
    def __init__(self, config: GeneratorConfig):
        self.config = config

    def generate(self):
        strutures_functions = RuleGenerator._map_structures_functions()
        section = ptex.Section(f"{self.config.rule_section_title}")
        for rule_structure in self.config.rule_structures:
            structure_function = strutures_functions.get(rule_structure, RuleGenerator.__no_function_waring)
            section.append(structure_function(self))
            section.append(ptex.NoEscape("\\newline "))
        return section

    def _generate_description(self) -> str:
        return ptex.NoEscape(f"{{\\fontsize{{{self.config.font_size}}}{{{int(self.config.font_size*1.2)}}}\selectfont {{{self.config.rule_description}}}}}")

    ########### TODO Add correct function content
    def _generate_index(self) -> str:
        content = "Indeks: "
        return ptex.NoEscape(f"{{\\fontsize{{{self.config.font_size}}}{{{int(self.config.font_size*1.2)}}}\selectfont {{{content}}}}}")

    def _generate_exam_duration(self) -> str:
        content = f"Examin trwa {self.config.rule_exam_duration} minut"
        return ptex.NoEscape(f"{{\\fontsize{{{self.config.font_size}}}{{{int(self.config.font_size*1.2)}}}\selectfont {{{content}}}}}")

    def _generate_max_points(self) -> str:
        content = f"Za test można zdobyć maksymalnie {self.config.rule_max_points} punktów"
        return ptex.NoEscape(f"{{\\fontsize{{{self.config.font_size}}}{{{int(self.config.font_size*1.2)}}}\selectfont {{{content}}}}}")

    def _generate_date(self) -> str:
        content = f"Data: {self.config.rule_exam_date}"
        return ptex.NoEscape(f"{{\\fontsize{{{self.config.font_size}}}{{{int(self.config.font_size*1.2)}}}\selectfont {{{content}}}}}")

    def _generate_mark_demo(self) -> str:
        content = "TODO Mark demo"
        return ptex.NoEscape(f"{{\\fontsize{{{self.config.font_size}}}{{{int(self.config.font_size*1.2)}}}\selectfont {{{content}}}}}")
    #############

    def __no_function_waring(self, *args, **kwargs):
        logger.warning("No function in created map")

    @classmethod
    def _map_structures_functions(cls) -> tp.Dict[RuleStructure, tp.Callable]:
        return {
            RuleStructure.DESCRIPTION: cls._generate_description,
            RuleStructure.INDEX: cls._generate_index,
            RuleStructure.EXAM_DURATION: cls._generate_exam_duration,
            RuleStructure.MAX_POINTS: cls._generate_max_points,
            RuleStructure.DATE: cls._generate_date,
            RuleStructure.MARK_DEMO: cls._generate_mark_demo
        }
