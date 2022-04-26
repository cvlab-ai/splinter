import typing as tp
import pylatex as ptex
from .generator_config import GeneratorConfig, RuleStructure
from .logger import logger
from .rules import Rules


class RuleGenerator:
    def __init__(self, config: GeneratorConfig):
        self.config = config

    def generate(self):
        strutures_functions = RuleGenerator._map_structures_functions()
        rules = Rules()
        section = ptex.Section(f"{self.config.rule_section_title}")
        for rule_structure in self.config.rule_structures:
            structure_function = strutures_functions.get(
                rule_structure, RuleGenerator.__no_function_waring
            )
            rules.add_item("", structure_function(self))
        return rules

    def _generate_description(self) -> str:
        return self.config.rule_description

    ########### TODO Add correct function content
    def _generate_index(self) -> str:
        content = "Indeks: "
        return ptex.NoEscape(
            rf"{content}\framebox{self.config.rule_index_box_size}{{}}"
        )

    def _generate_exam_duration(self) -> str:
        content = f"Examin trwa {self.config.rule_exam_duration} minut"
        return content

    def _generate_max_points(self) -> str:
        content = (
            f"Za test można zdobyć maksymalnie {self.config.rule_max_points} punktów"
        )
        return content

    def _generate_date(self) -> str:
        content = f"Data: {self.config.rule_exam_date}"
        return content

    def _generate_mark_demo(self) -> str:
        content = "Sposób zaznaczania: "
        zaznaczanie = ptex.NoEscape(fr"Sposób zaznaczania: ")
        anulowanie = ptex.NoEscape(fr"Sposób anulowania: ")
        return zaznaczanie + anulowanie

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
            RuleStructure.MARK_DEMO: cls._generate_mark_demo,
        }
