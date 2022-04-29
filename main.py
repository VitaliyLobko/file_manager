import argparse

parser = argparse.ArgumentParser(description='sorting  files')
parser.add_argument('--source', '-s', required=True, help='Source folder')
args = vars(parser.parse_args())

source = args.get('source')
