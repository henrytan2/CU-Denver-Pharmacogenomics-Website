from django.views import generic
from mysite.business.alderaan import Alderaan
import pickle5 as pickle

class IndexView(generic.TemplateView):
    template_name = 'index.html'


class ContactView(generic.TemplateView):
    template_name = 'contact.html'


class PeopleView(generic.TemplateView):
    template_name = 'people.html'


# def get_Pnum(GIGG):
#     with open('ENSG_PN_dictALL.pickle', 'rb') as f:
#         ENSG_Pnum_dict = pickle.load(f)
#         P_num = ENSG_Pnum_dict[f'{GIDD}']
#     return P_num
#
# def get_sequence_unmut(pnum):
#     # p = PDBParser()
#     a = Alderaan()
#     a.run_command('cp Documents/alphafold/AF-P81605-F1-model_v1.pdb.gz tmp.pdb.gz')
#     a.run_command('gzip -d tmp.pdb.gz')

    # perform on server?

    # pdb_string=str(pdb_file_unmut)
    # pdb_file_=pdb_string.strip('[]')
    # pdb_file=pdb_file_.strip("''")
    # structure = p.get_structure('PDBunzip', pdb_file)
    # ppb = PPBuilder()
    # for pp in ppb.build_peptides(structure):
    #     PDBs = str(pp.get_sequence())
    #     unmutated_sequence_l = PDBs.lower()
    #     return unmutated_sequence_l

# def get_mutation_position(poss_mutation):
#     if poss_mutation.startswith('p.') and poss_mutation[2:5] != poss_mutation[-3:] and poss_mutation[-3:] != 'del' and poss_mutation[-3:] != 'Ter' and poss_mutation[-3:] != 'dup' and len(poss_mutation)<12:
#         act_mutation=poss_mutation.split(' ')
#         for mutation in act_mutation:
#             mutation_position = int(mutation[5:-3])
#             return mutation_position
#

# CCID = 'p.Thr198Met'
# GIDD = 'ENSG00000160882'
# Pnum = get_Pnum(GIDD)
#
# print('P_num is: ', Pnum)
# position_mutation = get_mutation_position(CCID)
# print('position_mutation is', position_mutation)
#
# unmutated_seq = get_sequence_unmut(f'{Pnum}')
