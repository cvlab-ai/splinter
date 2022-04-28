import argparse


class GeneratorArgs(argparse.ArgumentParser):
    def __init__(self):
        super().__init__(description="Generate exam files")
        self.add_argument(
            "-d",
            "--destdir",
            type=str,
            required=False,
            default="exams",
            help="Destination directory for generated files",
        )
        self.add_argument(
            "-n",
            "--number",
            type=int,
            required=False,
            default=1,
            help="Number of exams to generate",
        )
        self.add_argument(
            "-z",
            "--zip",
            action="store_true",
            required=False,
            help="Zip exam and instrucion files",
        )
        self.add_argument(
            "-t",
            "--test",
            action="store_true",
            required=False,
            help="Generate exam with static name for testing",
        )
