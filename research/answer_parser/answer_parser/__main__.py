import logging
from answer_parser import logger
from answer_parser.unpack import unpack_answers
from answer_parser.main_args import get_args
from answer_parser.log_format import CustomFormatter
from answer_parser.exam_key import ExamKey


ch = logging.StreamHandler()
ch.setFormatter(CustomFormatter())
logging.basicConfig(level=logging.DEBUG, handlers=[ch])

args = get_args()

if args.command:
    logger.info("Running command: %s", args.command)
    args.func(args)
    exit(0)

unpack_answers(args.search_dir, args.dest_dir, args.archive_re)
logger.info("Loaind exam key")
exams = ExamKey.load_exam_keys(args.dest_dir)
logger.info("Found %d exam keys", len(exams))
