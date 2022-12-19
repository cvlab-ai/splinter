import typing as tp
import pylatex as ptex
from .generator_config import GeneratorConfig, RuleStructure
from .logger import logger
from .rules import Rules


class RuleGenerator:
    def __init__(self, config: GeneratorConfig):
        self.config = config

    def generate(self):
        structures_functions = RuleGenerator._map_structures_functions()
        rules = Rules()
        rules.add_item("", self._generate_title())
        for rule_structure in self.config.rule_structures:
            structure_function = structures_functions.get(rule_structure, RuleGenerator.__no_function_waring)
            rules.add_item("", structure_function(self))
        return rules

    def _generate_title(self) -> ptex.NoEscape:
        font_size = self.config.font_size + self.config.rule_title_font_size
        footer_style = f"{ptex.Command('fontsize',arguments=[font_size, '24pt']).dumps()}" \
                       f"{ptex.Command('selectfont').dumps()}"
        return ptex.NoEscape(f"{{{footer_style} {self.config.rule_section_title}}}")

    def _generate_description(self) -> str:
        content = f"Test zawiera {self.config.number_of_questions} " \
                  f"pytań wielokrotnego wyboru. Za każde pytanie można zdobyć " \
                  f"{self.config.rule_max_points_per_question} punktów"
        return content

    def _generate_index(self) -> str:
        content = "Indeks: "
        return ptex.NoEscape(
            rf"{content}\framebox{self.config.rule_index_box_size}{{}}"
        )

    def _generate_exam_duration(self) -> str:
        content = f"Czas trwania egzaminu - {self.config.rule_exam_duration} minut"
        return content

    def _generate_date(self) -> str:
        content = f"Data: {self.config.rule_exam_date}"
        return content

    def _generate_mark_demo(self) -> str:
        content = f"{self.config.check_mark_type} aby zaznaczyć prawidłową odpowiedź. " \
                  f"{self.config.uncheck_mark_type} aby odznaczyć odpowiedź."
        return content

    def __no_function_waring(self, *args, **kwargs):
        logger.warning("No function in created map")

    @classmethod
    def _map_structures_functions(cls) -> tp.Dict[RuleStructure, tp.Callable]:
        return {
            RuleStructure.DESCRIPTION: cls._generate_description,
            RuleStructure.INDEX: cls._generate_index,
            RuleStructure.EXAM_DURATION: cls._generate_exam_duration,
            RuleStructure.DATE: cls._generate_date,
            RuleStructure.MARK_DEMO: cls._generate_mark_demo,
        }
