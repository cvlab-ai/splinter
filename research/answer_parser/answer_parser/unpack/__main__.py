from . import unpack_answers
from . import unpack_args


def main(args):
    unpack_answers(args.search_dir, args.dest_dir, args.archive_re)

if __name__ == "__main__":
    args = unpack_args.get_args()
    main()
