import argparse
import random
from tqdm import tqdm

from utils import read_fastq

parser = argparse.ArgumentParser()

parser.add_argument('--input_file', type=str, default="data/SRR6756023.fastq", help='input fastq file')
parser.add_argument('--mix_file', type=str, default="data/SRR6756025.fastq,data/SRR6756028.fastq", help='files to be mixed, separated by ","')
parser.add_argument('--output_file', type=str, default="output.fastq", help='output file')
parser.add_argument('--mix_percentage', type=float, default=0.1, help='contamination level')
parser.add_argument('--number_of_reads', type=int, default=1000000, help='total number of reads')
parser.add_argument('--mix_partition', type=int, default=10, help='whether to mix continues segments, default: False')

args = parser.parse_args()


def prepare_mix():
    mix_filenames = args.mix_file.split(",")
    number_read_per_file = int(args.number_of_reads * args.mix_percentage / len(mix_filenames))

    all_reads = []
    for filename in mix_filenames:
        reads = []
        for read in read_fastq(filename):
            reads.append(read)
            if len(reads) == number_read_per_file:
                break
        all_reads += reads[:]

    return all_reads


def main():

    mix_reads = prepare_mix()
    random.shuffle(mix_reads)

    number_reads_per_insertion = len(mix_reads) // args.mix_partition

    with open(args.output_file, "w", encoding="utf-8") as fw:
        for i, line in tqdm(enumerate(read_fastq(args.input_file))):
            fw.write(line)
            if i % (args.number_of_reads // args.mix_partition) == 0:
                for _ in range(number_reads_per_insertion):
                    fw.write(mix_reads.pop())

            if i == args.number_of_reads * (1-args.mix_percentage):
                break

main()