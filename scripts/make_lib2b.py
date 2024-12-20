#!/usr/bin/env python

import seaborn as sns
sns.set_context('poster')
sns.set_style('white')
import numpy as np
#from arnie.pfunc import pfunc
#from arnie.free_energy import free_energy
#from arnie.bpps import bpps
#from arnie.mfe import mfe
#import arnie.utils as utils
from decimal import Decimal
import operator as op
import matplotlib.pyplot as plt
import pandas as pd

def get_other_controls(seriestype, filename):
    readfile = open(filename, 'r')

    var_lib = {}
    var_lib[seriestype] = []
    
    for line in readfile:

        nameseq = line.split()
        var_lib[seriestype].append(nameseq[1])
        
    readfile.close()
   
    return var_lib

def get_rc(seqlist): 
    rcseq = []
    
    for seq in seqlist: 
        cseq = ''
        for c in seq[::-1].upper():
            if c == 'A':
                b = 'T'
            elif c == 'T':
                b = 'A'
            elif c == 'G':
                b = 'C'
            elif c == 'C':
                b = 'G'
            cseq += b
        newseq = seq + cseq
        rcseq.append(newseq)
    return rcseq

def def_stems():
    #Return a list of all possible pairs that can be at the base of a loop of length 2
    #Is in the form of a sequence 4 nts long where the you have nt1 pairing with nt4 and nt2 pairing with nt3
    
    pairs = ['AT', 'TA', 'GC', 'CG']
    stacks = []
    
    for pair1 in pairs: 
        for pair2 in pairs:
            
            seq = pair1[0] + pair2 + pair1[1]
            stacks.append(seq)
    
    return stacks

def def_triloops():
    #Return a list of all possible triloops
    
    nts = ['A', 'T', 'C', 'G']
    loops = []
    
    for nt1 in nts: 
        for nt2 in nts: 
            for nt3 in nts: 
                seq = nt1 + nt2 + nt3
                loops.append(seq) 
    
    return loops

def def_tetraloops():
    #Return a list of all possible tetraloops
    nts = ['A', 'T', 'C', 'G']
    loops = []
    
    for nt1 in nts: 
        for nt2 in nts: 
            for nt3 in nts: 
                for nt4 in nts: 
                    seq = nt1 + nt2 + nt3 + nt4
                    loops.append(seq)
                
    return loops    

def def_bulges():
    #return a list of all single nucleotide and double nucleotide bugles
    
    nts = ['A', 'C', 'T', 'G']
    bulges = []
    
    for nt1 in nts: 
        bulges.append(nt1)
        for nt2 in nts: 
            doublent = nt1+nt2
            bulges.append(doublent)
            
    return bulges

def def_mismatches():
    #return a list of all possible mismatch nts
    nts = ['A', 'C', 'T', 'G']
    pairs = ['AT', 'TA', 'CG', 'GC']
    
    mismatches = []
    
    for nt1 in nts: 
        for nt2 in nts: 
            tmp = nt1+nt2
            if not (tmp in pairs): 
                mismatches.append(tmp)           
    return mismatches

def make_triloops(scaffolds): 
    #Return a dictionary of triloops where the key is the scaffold, and the values are a list of all possible triloops
    #the stem is all possible 2mer stacks
    bases = ['AT', 'TA', 'GC', 'CG']
    tops = def_triloops()
    
    tris = []
    for base in bases: 
        for loop in tops: 
            seq = 'G' + base[0:1] + loop + base[1:] + 'C'
            tris.append(seq)
            
    var_lib = {}

    for scaffold in scaffolds: 
        tmp = []
        for triloop in tris: 
            seq = scaffold[0:int(len(scaffold)/2)] + triloop + scaffold[int(len(scaffold)/2):]
            tmp.append(seq)
        
        var_lib[scaffold] = tmp
    
    return var_lib

def make_triloopsNNN(scaffolds): 
    #Return a dictionary of triloops where the key is the scaffold, and the values are a list of all possible triloops
    #the stem is all possible 2mer stacks
    bases = def_stems()
    tops = def_triloops()
    
    tris = []
    for base in bases: 
        for loop in tops: 
            seq = base[0:2] + loop + base[2:]
            tris.append(seq)
            
    var_lib = {}

    for scaffold in scaffolds: 
        tmp = []
        for triloop in tris: 
            seq = scaffold[0:int(len(scaffold)/2)] + triloop + scaffold[int(len(scaffold)/2):]
            tmp.append(seq)
        
        var_lib[scaffold] = tmp
    
    return var_lib

def make_tetraloops(scaffolds):
    #Return a dictionary of tetraloops where the key is the scaffold, and the values are a list of all possible tetraloops
    #the stem is all possible 2mer stacks
    bases = ['AT', 'TA', 'GC', 'CG']
    top = def_tetraloops()

    tets = []
    for base in bases: 
        for loop in top: 
            seq = 'G' + base[0:1] + loop + base[1:] + 'C'
            tets.append(seq)
            
    var_lib = {}

    for scaffold in scaffolds: 
        tmp = []
        for tetraloop in tets: 
            seq = scaffold[0:int(len(scaffold)/2)] + tetraloop + scaffold[int(len(scaffold)/2):]
            tmp.append(seq)
        
        var_lib[scaffold] = tmp
    
    return var_lib

def make_tetraloopsNNN(scaffolds):
    #Return a dictionary of tetraloops where the key is the scaffold, and the values are a list of all possible tetraloops
    #the stem is all possible 2mer stacks
    bases = def_stems()
    top = def_tetraloops()

    tets = []
    for base in bases: 
        for loop in top: 
            seq = base[0:2] + loop + base[2:]
            tets.append(seq)
            
    var_lib = {}

    for scaffold in scaffolds: 
        tmp = []
        for tetraloop in tets: 
            seq = scaffold[0:int(len(scaffold)/2)] + tetraloop + scaffold[int(len(scaffold)/2):]
            tmp.append(seq)
        
        var_lib[scaffold] = tmp
    
    return var_lib


def make_mismatches(scaffolds):
    mismatches = def_mismatches()
    stack = def_stems()

    var_lib = {}
    mismatch_vars = []
    
    for base in stack:
        for mismatch in mismatches: 
            seq = base[0:1] + mismatch[0] + base[1:3] + mismatch[1] + base[3:]
            mismatch_vars.append(seq)

    for scaffold in scaffolds: 
        tmp = []
        split = int(len(scaffold)/2/2)

        for mismatch in mismatch_vars: 
            seq = scaffold[0:split] + mismatch[0:int(len(mismatch)/2)] + scaffold[split:split*2] + 'GAAA' + scaffold[split*2:split*3] + mismatch[int(len(mismatch)/2):] + scaffold[split*3:]
            tmp.append(seq)
        
        var_lib[scaffold] = tmp
    
    return var_lib    

def make_bulges(scaffolds):
    bulges = def_bulges()
    stack = def_stems()

    var_lib = {}

    for scaffold in scaffolds: 
        tmp = []
        split = int(len(scaffold)/2/2)
        
        for base in stack:
            for bulge in bulges: 

                seq1 = scaffold[0:split] + base[0:1] + bulge + base[1:2] + scaffold[split:split*2] + 'GAAA' + scaffold[split*2:split*3] + base[2:] + scaffold[split*3:]
                seq2 = scaffold[0:split] + base[0:2] + scaffold[split:split*2] + 'GAAA' + scaffold[split*2:split*3] + base[2:3] + bulge + base[3:] + scaffold[split*3:]
                tmp.append(seq1)
                tmp.append(seq2)
 
        var_lib[scaffold] = tmp
    
    return var_lib    

def make_watson_crick():
    #makes all watson crick pairs of length WC1: 5, WC2: 6, WC3: 7
    
    var_lib = {}
    var_lib['WC1'] = []
    var_lib['WC2'] = []
    var_lib['WC3'] = []
    
    loop = 'GAAA'
    pairs = ['AT', 'TA', 'GC', 'CG']
    
    for nt1 in pairs:
        for nt2 in pairs: 
            for nt3 in pairs:
                for nt4 in pairs:
                    for nt5 in pairs:
                        WC1_tmp = nt1[0] + nt2[0] + nt3[0] + nt4[0] + nt5[0] + loop + nt5[1] + nt4[1] + nt3[1] + nt2[1] + nt1[1]
                        WC2_tmp = 'G' + WC1_tmp + 'C'
                        WC3_tmp = 'G' + nt1[0] + nt2[0] + nt3[0] + nt4[0] + nt5[0] + 'G' + loop + 'C' + nt5[1] + nt4[1] + nt3[1] + nt2[1] + nt1[1] + 'C'
                        var_lib['WC1'].append(WC1_tmp)
                        var_lib['WC2'].append(WC2_tmp)
                        var_lib['WC3'].append(WC3_tmp)                                
    
    return var_lib

def make_mismatches_AC():
    #makes a CA mismatch randomly within different stem length 5
    
    var_lib = {}
    var_lib['mismatches_AC'] = []
    
    loop = 'GAAA'
    pairs = ['AT', 'TA', 'GC', 'CG', 'AC', 'CA']
    
    for nt1 in pairs:
        for nt2 in pairs: 
            for nt3 in pairs:
                for nt4 in pairs:
                    for nt5 in pairs:
                        check = [nt1, nt2, nt3, nt4, nt5]
                        if 'AC' in check or 'CA' in check:
                            if check.count('AC') < 2 and check.count('CA') < 2:
                                    WC3_tmp = 'G' + nt1[0] + nt2[0] + nt3[0] + nt4[0] + nt5[0] + 'G' + loop + 'C' + nt5[1] + nt4[1] + nt3[1] + nt2[1] + nt1[1] + 'C'
                                    var_lib['mismatches_AC'].append(WC3_tmp)
    return var_lib

def make_mismatches_GT():
    #makes a CA mismatch randomly within different stem length 5
    
    var_lib = {}
    var_lib['mismatches_GT'] = []
    
    loop = 'GAAA'
    pairs = ['AT', 'TA', 'GC', 'CG', 'GT', 'TG']
    
    for nt1 in pairs:
        for nt2 in pairs: 
            for nt3 in pairs:
                for nt4 in pairs:
                    for nt5 in pairs:
                        check = [nt1, nt2, nt3, nt4, nt5]
                        if 'GT' in check or 'TG' in check:
                            if check.count('TG') < 2 and check.count('GT') < 2:
                                    WC3_tmp = 'G' + nt1[0] + nt2[0] + nt3[0] + nt4[0] + nt5[0] + 'G' + loop + 'C' + nt5[1] + nt4[1] + nt3[1] + nt2[1] + nt1[1] + 'C'
                                    var_lib['mismatches_GT'].append(WC3_tmp)
    return var_lib

def make_mismatches_NNN(scaffolds):
    mismatches = def_mismatches()
    stack1 = def_stems()
    stack2 = def_stems()

    var_lib = {}
    mismatch_vars = []
    
    for base1 in stack1:
        for base2 in stack2: 
            for mismatch in mismatches: 
                seq = base1[:2] + mismatch[0] + base2[:2] + base2[2:] + mismatch[1] + base1[2:]
                mismatch_vars.append(seq)

    for scaffold in scaffolds: 
        tmp = []
        split = int(len(scaffold)/2/2)

        for mismatch in mismatch_vars: 
            seq = scaffold[0:split] + mismatch[0:int(len(mismatch)/2)] + scaffold[split:split*2] + 'GAAA' + scaffold[split*2:split*3] + mismatch[int(len(mismatch)/2):] + scaffold[split*3:]
            tmp.append(seq)
        
        var_lib[scaffold] = tmp
    
    return var_lib    

def make_bulges_NNN(scaffolds):
    bulges = def_bulges()
    stack1 = def_stems()
    stack2 = def_stems()

    var_lib = {}

    
    for scaffold in scaffolds: 
        tmp = []
        split = int(len(scaffold)/2/2)
        
        for base1 in stack1:
            for base2 in stack2: 
                for bulge in bulges: 
    
                    seq1 = scaffold[0:split] + base1[0:2] + bulge + base2[0:2] + scaffold[split:split*2] + 'GAAA' + scaffold[split*2:split*3] + base2[2:] + base1[2:] + scaffold[split*3:]
                    seq2 = scaffold[0:split] + base1[0:2] + base2[0:2] + scaffold[split:split*2] + 'GAAA' + scaffold[split*2:split*3] + base2[2:] + bulge + base1[2:] + scaffold[split*3:]
                    tmp.append(seq1)
                    tmp.append(seq2)
 
                var_lib[scaffold] = tmp
    
    return var_lib    

def make_repeats(maxlen, seqs):
    #returns a list of repeats of the given seq varying from 1 repeat upto n where seq length * n is less than the max insert size
    
    var_lib = {}
    
    for seq in seqs:
        var_lib[seq] = []
        for i in range(int(maxlen/len(seq))): 
            seq_repeat = (i+1)*seq
            if len(seq_repeat) <= maxlen:
                var_lib[seq].append(seq_repeat)
    
    return var_lib

def make_polynt(maxlen, nts):
    var_lib = {}

    for nt in nts:
        var_lib[nt] = []
        for i in range(maxlen): 
            var_lib[nt].append(nt*(i+1))
            
    return var_lib        
    

def make_loop_vars(scaffolds, maxfulllen):
    #returns a dictionary of loops of different lengths into the given scaffold structure. Key: scaffold, value list of constructs with different size loops
    
    var_lib = {}
    
    loopstart = 'GAAA'  
    otherscaffolds = ['GCCGCCGGGCCC']
    otherscaffolds = get_rc(otherscaffolds)
    scaffolds = scaffolds + otherscaffolds    
    
    for scaffold in scaffolds: 
        tmp = []
        for i in range(maxfulllen): 
            loop = loopstart + 'A'*i
            seq = scaffold[0:int(len(scaffold)/2)] + loop + scaffold[int(len(scaffold)/2):]
            if len(seq) <= maxfulllen:
                tmp.append(seq)
            loop2 = loopstart + 'AAC'*i
            seq2 = scaffold[0:int(len(scaffold)/2)] + loop2 + scaffold[int(len(scaffold)/2):]
            if len(seq2) <= maxfulllen:
                tmp.append(seq2)            
        
        var_lib[scaffold] = tmp     
    
    return var_lib

def make_stem_ctrls(scaffolds, maxlength):
    
    var_lib = {}
    loop = 'GAAA'
    
    #adding some super stable scaffolds for the stem controls
    otherscaffolds = ['GCCGCCCG', 'GCCGCCGGGCCC']
    scaffolds = scaffolds + otherscaffolds
    scaffolds = get_rc(scaffolds)

    for scaffold in scaffolds: 
        tmp = []
        for i in range(1, int((maxlength-len(scaffold))/2)): 
            dangle = 'A'*i
            seq = dangle + scaffold[0:int(len(scaffold)/2)] + loop + scaffold[int(len(scaffold)/2):] + dangle
            if len(seq) <= maxlength:
                tmp.append(seq)
            seq = dangle + scaffold[0:int(len(scaffold)/2)] + loop + scaffold[int(len(scaffold)/2):]
            if len(seq) <= maxlength:
                tmp.append(seq)            
            seq = scaffold[0:int(len(scaffold)/2)] + loop + scaffold[int(len(scaffold)/2):] + dangle
            if len(seq) <= maxlength:
                tmp.append(seq)            
        
        var_lib[scaffold] = tmp     
    
    return var_lib    

def make_superstem(maxlength):
    varlib = {}
    loop = 'GAAA'
    
    lenstem = int((maxlength - len(loop))/2)
    
    #a gc rich sequence that avoids 4 Gs in a row
    gcrichseqs = ['GCGGCCGCGCCGCAGGCGGCGCGCGCG', 'GCAAGGCACCAGGACGCAAGCA', 'GTCGTTGCCGTGCCTGCGCGTGCCC', 'GGCGCGTAGCCGTGCCGTGCGGTG', 'GCACCGGGACCACCGGAGGCACCGG']

    for gcrichseq in gcrichseqs:
        stem = gcrichseq[0:int(lenstem)]
        stem = get_rc([stem])

        superstem = stem[0][0:int(lenstem)] + loop + stem[0][int(lenstem):lenstem*2]
        varlib[gcrichseq] = [superstem]
        print (superstem)
    
    print(varlib)
    
    return (varlib)

def read_PK_file(filename):
    
    PKfile = open(filename, 'r')
    constructs = {}
    line = PKfile.readline()
    
    while PKfile :
        line = PKfile.readline().split('\t')
        if len(line) > 2:
            constructs[line[1]] = [line[3],line[4]]
        else: 
            break
    return constructs

def make_PKs(PKconstructs):
    # take a dictionary of key: type of PK and value: list of pseudoknot sequences and dot brackets
    
    var_lib = {}
    stemsym = ['(', ')', '[', ']']

    for construct in PKconstructs.keys():
        sequence = PKconstructs[construct][0]
        var_lib[construct] = [sequence]
        for bracket in stemsym:
            indices = [i for i in range(len(PKconstructs[construct][1])) if PKconstructs[construct][1].startswith(bracket, i)]
            lenpolyA = len(indices)
            var_lib[construct].append(sequence[0:indices[0]] + 'A'*lenpolyA + sequence[indices[-1]+1:])
            var_lib[construct].append(sequence[0:indices[0]] + 'A'*lenpolyA + sequence[indices[-1]+1:])
    return var_lib

def make_bae_controls():
    #Args: the filename of the mismatch constructs used in Bae et al. 2020 NAR. 
    #The file is in the format of col1: name of sequence col2: sequence, the 
    #first row is the reference seq and subsequent rows are the same sequence 
    #but with mismatches introduced. Noticed their constructs always have A-mismatch-C even thought the mismatch is at different positions in the construct
    #Returns: a dictionary where the key is the reference stem and the value is the mismatch stem.
    scaffolds = ['CG', 'AGCT']
    refstems = ['AAGCC', 'AACCA', 'TAACT']
    loop = 'GAAA'
    nts = ['A', 'T', 'G', 'C']
    varlib = {}
    for scaffold in scaffolds: 
        for stem in refstems: 
            perfectstem = get_rc([stem])[0]
            fullperfectstem = scaffold[0:int(len(scaffold)/2)] + perfectstem[0:int(len(perfectstem)/2)] + loop + perfectstem[int(len(perfectstem)/2):] + scaffold[int(len(scaffold)/2):]
            if scaffold in varlib.keys():
                varlib[scaffold].append(fullperfectstem)
            else: 
                varlib[scaffold] = [fullperfectstem]
            for nt in nts: 
                newstem = stem[0:int(len(stem)/2)] + nt + stem[-int(len(stem)/2):]
                if newstem != stem: 
                    fullstem = newstem + perfectstem[int(len(perfectstem)/2):]
                    varlib[scaffold].append(scaffold[0:int(len(scaffold)/2)] + fullstem[0:int(len(fullstem)/2)] + loop + fullstem[int(len(fullstem)/2):] + scaffold[int(len(scaffold)/2):])
    
    return varlib

def make_ss_fluor_ctrls(maxlen):
    #makes a set of controls that are single stranded with the max length possible and have all possible 3 mers closest to the fluor labeled oligo. 
    nts = ['A', 'C', 'T', 'G']
    threemers = []
    ssaddon = 'AAC'*int((maxlen-3)/3)
    
    for nt1 in nts: 
        for nt2 in nts: 
            for nt3 in nts: 
                threemers.append(nt1+nt2+nt3+ssaddon)
    threemer_lib = {}
    threemer_lib['fluor_ctrls'] = threemers
    print (threemers)
    return threemer_lib

def get_dGs(var_lib): 
    #Given a library of variants, return a dictionary where the key is the scaffold and the values are clcualted dGs. 
    
    dG_lib = {}
    
    for scaffold in var_lib: 
        tmp = []
        for var in var_lib[scaffold]:
            tmp.append(free_energy(var, package = 'nupack', dna = True))
            dG_lib[scaffold] = tmp    
            
    return dG_lib

def filter_dGs(var_lib): 
    #Given a library of variants, return a dictionary where the key is the scaffold and the values are clcualted dGs. 
    
    dG_lib = {}
    
    for scaffold in var_lib: 
        tmp = []
        if scaffold != ['WC1']:
            for var in var_lib[scaffold]:
                if free_energy(var, package = 'nupack', dna = True) < -6:
                    dG_lib[scaffold] = tmp    
            
    return dG_lib


def plot_median_dG(dG_lib, figname):
    #Given a dictionary of key: scaffold and value: list of dGs of constructs, plot box plots of the dGs by scaffold. 
    #sorted_keys, sorted_vals = zip(*sorted(dG_lib.items(), key=op.itemgetter(1)))
    
    lib_data = pd.DataFrame.from_dict(dG_lib)
    
    plt.clf()
    
    sns.set(context='notebook', style='whitegrid')
    
    sns_plot = sns.boxplot(data=lib_data, width=.9, palette='Blues')
    sns_plot = sns.swarmplot(data=lib_data, size=6, edgecolor="black", linewidth=.18, palette='Blues', alpha=0.5)
    #g.set_xticklabels(g.get_xticklabels(), rotation=30
    sns_plot.set_xticklabels(sns_plot.get_xticklabels(), rotation=45)

    plt.savefig(figname, bbox_inches="tight")
    
def write_lib_to_file(series, filename):
    
    writefile = open(filename, 'w')
    total = 0
    
    for type_ in series: 
        for scaffold in series[type_]:
            for i in series[type_][scaffold]:
                line = type_ + '\t' + i + '\n'
                writefile.write(line)
                total += 1

    writefile.close()
    print (total)


if __name__ == '__main__':
    
   
    #define the scaffolds you want to test
    scaffolds = ['GC','CGCG','GATC']
    scaffolds = get_rc(scaffolds)

    maxlength = 40
    PKs = read_PK_file('short_pseudoknots.txt')
    
    #make all the variants for each scaffold
    triloop_libNNN = make_triloopsNNN([scaffolds[2]])
    triloop_lib = make_triloops([scaffolds[0], scaffolds[1]])
    tetraloop_lib = make_tetraloops([scaffolds[0], scaffolds[1]])
    tetraloop_libNNN = make_tetraloopsNNN([scaffolds[2]])
    bulges_lib = make_bulges([scaffolds[1], scaffolds[2]])
    bulges_libNNN = make_bulges_NNN([scaffolds[0]])
    mismatches_lib = make_mismatches([scaffolds[1], scaffolds[2]])
    mismatches_libNNN = make_mismatches_NNN([scaffolds[0]])
    WC_lib = make_watson_crick()
    superstem = make_superstem(maxlength)
    repeat = make_repeats(maxlength, ['AC', 'AAC', 'AAAC', 'AG', 'AAG', 'AAAG',\
                                      'AT', 'AAT', 'AAAT', 'TC', 'TTC', 'TTTC',\
                                      'TG', 'TTG', 'TTTG', 'TA', 'TTA', 'TTTA',\
                                      'AGGA', 'ACCA', 'ACCCA'])
    polynt = make_polynt(maxlength, ['A', 'T'])
    variableloops = make_loop_vars(scaffolds, maxlength)
    stem_controls = make_stem_ctrls(scaffolds, maxlength)
    PK_lib = make_PKs(PKs)
    WB_controls = get_other_controls('WB', 'WB_controls.txt')
    PUM_controls = get_other_controls('PUM', 'PUM_controls.txt')
    mismatches_GT = make_mismatches_GT()
    mismatches_AC = make_mismatches_AC()
    bae_controls = make_bae_controls()

    series = {'triloops': triloop_lib, 'tetraloops': tetraloop_lib, \
              'bulges':bulges_lib, 'triloopsNNN': triloop_libNNN, \
              'tetraloopsNNN': tetraloop_libNNN, \
              'bulgesNNN':bulges_libNNN, 'mismatchesNNN':mismatches_libNNN, \
              'WC':WC_lib, 'repeats':repeat, 'poly_nucleotides': polynt, \
              'varloop':variableloops, 'stem_ctrls':stem_controls, \
              'pseudoknots':PK_lib, \
              'WB_controls':WB_controls, 'PUM_controls':PUM_controls, \
              'superstem': superstem, 'mismatches_GT':mismatches_GT, \
              'mismatches_AC':mismatches_AC, 'mismatches':mismatches_lib, 
              'bae_controls':bae_controls}
              
    # series = {'ssfluor_ctrls':make_ss_fluor_ctrls(maxlength)}
    
    print('superstems', superstem)
    # make one master table for each category that describes them in more detail 1)how many in each series 2) detailed descripter of what 3) detailed of why 
    # make a second table for each sequence variant that includes: 1) where is the variant 2) what it is 3) how many 4) scaffold
    
    # write_lib_to_file(series, 'NNN_ssfluor_ctrls.txt')
    
    for seri in series: 
        write_lib_to_file({seri:series[seri]}, seri + '.txt')      
    
    # # plot the median dG for the scaffolds, only DNA capable at this point.
    # dG_mismatches_AC = get_dGs(mismatches_AC)
    # plot_median_dG(dG_mismatches_AC, 'mismatches_AC.png')
    
    # dG_mismatches_GT = get_dGs(mismatches_GT)
    # plot_median_dG(dG_mismatches_GT, 'mismatches_GT.png')    
    
    # dG_bae_controls = get_dGs(bae_controls)
    # plot_median_dG(dG_bae_controls, 'bae_controls.png')
    
    # dG_triloops = get_dGs(triloop_lib)
    # dG_triloopsNNN = get_dGs(triloop_libNNN)
    # dG_tetraloops = get_dGs(tetraloop_lib) 
    # dG_tetraloopsNNN = get_dGs(tetraloop_libNNN)     
    # dG_WCs = filter_dGs(WC_lib)
    # dG_bulges = get_dGs(bulges_lib)
    # dG_bulgesNNN = get_dGs(bulges_libNNN)
    # dG_mismatches = get_dGs(mismatches_lib)
    # dG_mismatchesNNN = get_dGs(mismatches_libNNN)
    # dG_mismatches2 = get_dGs(mismatch2_lib)
    # dG_variableloops = get_dGs(variableloops)  

    # plot_median_dG(dG_triloops, 'triloops_scaffold_dG.png')
    # plot_median_dG(dG_tetraloops, 'tetraloops_scaffold_dG.png')
    # plot_median_dG(dG_triloopsNNN, 'triloopsNNN_scaffold_dG.png')
    # plot_median_dG(dG_tetraloopsNNN, 'tetraloopsNNN_scaffold_dG.png')    
    # plot_median_dG(dG_WCs, 'watson_crick_dG.png')
    # plot_median_dG(dG_bulges, 'bulges_dG.png')
    # plot_median_dG(dG_bulgesNNN, 'bulgesNNN_dG.png')
    # plot_median_dG(dG_mismatches2, 'mismatches2.png')
    # plot_median_dG(dG_mismatches, 'mismatches_dG.png')
    # plot_median_dG(dG_mismatchesNNN, 'mismatchesNNN_dG.png')
    # plot_median_dG(dG_variableloops, 'varloops_dG.png')