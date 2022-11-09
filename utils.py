
def read_fastq(filename):

    cur_read = []
    with open(filename, "r", encoding="utf-8") as fr:
        for line in fr:
            cur_read.append(line)

            if len(cur_read) == 4:
                yield "".join(cur_read)
                cur_read = []

