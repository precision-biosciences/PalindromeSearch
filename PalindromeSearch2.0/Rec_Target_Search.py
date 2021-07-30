#Takes a sequence file and returns scored recombinase sites or pairs of scored recombinase sites

from Bio import SeqIO
import pandas as pd


def import_kmers(file_path):
    regions = {}
    for dna in SeqIO.parse(open(file_path), "fasta"):
        kmer_size = 34
        kmers = {}
        for start in range(0, len(dna.seq) - (kmer_size - 1), 1):
            kmer = dna.seq[start:start + kmer_size]
            kmers[str(start)] = str(kmer).upper()
        regions[dna.id] = kmers
    return regions


def comp(sequence):
    comp_seq = ""
    for bp in sequence:
        if bp == "A":
            comp_seq += "T"
        if bp == "C":
            comp_seq += "G"
        if bp == "G":
            comp_seq += "C"
        if bp == "T":
            comp_seq += "A"
    return comp_seq


def score_palindromy(sequence, weighting=1, score=0):
    if len(sequence) <= 1:
        return score
    else:
        if sequence[0] == sequence[-1]:
            score += weighting
        return score_palindromy(sequence[1:-1], weighting, score)


def filter_possible_sites(kmer_dict, ta, red_weight=4, yellow_weight=2):
    target_dict = {}
    for start, sequence in kmer_dict.iteritems():
        score = [0, 0, 0]
        first_seq = sequence[7:12] + comp(sequence[22:27])
        second_seq = sequence[5:7] + sequence[12] + comp(sequence[21]) + comp(sequence[27:29])
        third_seq = sequence[0] + sequence[2:4] + sequence[30:32] + sequence[33]
        score[0] = score_palindromy(first_seq)
        score[1] = score_palindromy(second_seq)
        score[2] = third_seq.count("A") + third_seq.count("T")
        if ta == "Y":
            if score[0] >= red_weight and score[1] >= yellow_weight and sequence[16:18] == "TA":
                target_dict[start] = [sequence, score]
        else:
            if score[0] >= red_weight and score[1] >= yellow_weight:
                target_dict[start] = [sequence, score]
    return target_dict


def get_middles(kmer_dict):
    middles = []
    for k, v in kmer_dict.iteritems():
        if v[0][13:21] in middles:
            pass
        else:
            middles.append(v[0][13:21])
    return middles


def match_pairs(kmer_dict, list_name1, list_name2, flip="N"):
    middle_list1 = get_middles(kmer_dict[list_name1])
    middle_list2 = get_middles(kmer_dict[list_name2])
    if flip == "Y":
        flip_middle1 = [comp(x[::-1]) for x in middle_list1]
        flip_middle2 = [comp(x[::-1])  for x in middle_list2]
        common_middles = list(set(middle_list1) & set(flip_middle2)) + list(set(middle_list2) & set(flip_middle1))
    else:
        common_middles = list(set(middle_list1) & set(middle_list2))
    sites = dict([(x, {'sequences': [], 'scores': [], 'locs': [], 'intron': []}) for x in common_middles])
    for key, value in kmer_dict[list_name1].iteritems():
        middle = value[0][13:21]
        if middle in sites.keys():
            sites[middle]['sequences'].append(value[0])
            sites[middle]['scores'].append(value[1])
            sites[middle]['locs'].append(key)
            sites[middle]['intron'].append(list_name1)
        if comp(middle[::-1]) in sites.keys() and flip =="Y":
            sites[comp(middle[::-1])]['sequences'].append(value[0])
            sites[comp(middle[::-1])]['scores'].append(value[1])
            sites[comp(middle[::-1])]['locs'].append(key)
            sites[comp(middle[::-1])]['intron'].append(list_name1 + "_flip")
    for key, value in kmer_dict[list_name2].iteritems():
        middle = value[0][13:21]
        if middle in sites.keys():
            sites[middle]['sequences'].append(value[0])
            sites[middle]['scores'].append(value[1])
            sites[middle]['locs'].append(key)
            sites[middle]['intron'].append(list_name2)
        if comp(middle[::-1]) in sites.keys() and flip == "Y":
            sites[comp(middle[::-1])]['sequences'].append(value[0])
            sites[comp(middle[::-1])]['scores'].append(value[1])
            sites[comp(middle[::-1])]['locs'].append(key)
            sites[comp(middle[::-1])]['intron'].append(list_name2 + "_flip")
    return sites


def put_stuff_in_excel(sites, output_file):
    ew = pd.ExcelWriter(output_file, engine='xlsxwriter')
    workbook = ew.book
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter'})
    cell_format = workbook.add_format()
    cell_format.set_font_name('Courier New')
    i = 0
    for middle in sites.keys():
        df = pd.DataFrame(pairs[middle])
        df = df[['sequences', 'scores', 'locs', 'intron']]
        df.to_excel(ew, sheet_name="Sheet1", startrow=1, startcol=i, index=False)
        worksheet = ew.sheets['Sheet1']
        worksheet.merge_range(0, i, 0, i + 3, middle, merge_format)
        worksheet.set_column(i, i, None, cell_format)
        worksheet.set_column(i+4, i+4, 1, None)
        i += 5
    workbook.close()
    return


if __name__ == '__main__':
    region_kmer_dicts = import_kmers(r"C:\Users\jlape\Box\0_Work_Folder\NewSiteResearch\19_02_27 DMD\DMD_introns_fasta.fa")
    excel_file = r"C:\Users\jlape\Box\0_Work_Folder\NewSiteResearch\19_02_27 DMD\recomb_sites.xlsx"
    ta_restrict = "Y"
    red = 4
    yellow = 1
    paired = "Y"
    flip = "N"
    region_filtered_sites = {}
    for i in region_kmer_dicts.keys():
        filtered_sites = filter_possible_sites(region_kmer_dicts[i], ta_restrict, red, yellow)
        region_filtered_sites[i] = filtered_sites
    for i in region_filtered_sites.keys():
        print i
        print len(region_filtered_sites[i])
    pairs = match_pairs(region_filtered_sites, "Intron44-45", "Intron55-56", flip)
    put_stuff_in_excel(pairs, excel_file)



