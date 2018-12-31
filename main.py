import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', type=str, choices=['train', 'test'])
    parser.add_argument('game', type=str, choices=['reversi'])
    return parser.parse_args()


def set_cuda(args: argparse.Namespace):
    if args.mode == 'train':
        os.environ['CUDA_VISIBLE_DEVICES'] = '1'
    else:
        os.environ['CUDA_VISIBLE_DEVICES'] = '0'


def train(args):
    pass


def test(args):
    pass


def main():
    args = parse_args()
    set_cuda(args)

    if args.mode == 'train':
        train(args)
    elif args.mode == 'test':
        test(args)


if __name__ == '__main__':
    main()
