from rest_framework.views import APIView
from rest_framework.response import Response
from .business.faspr_prep import FasprPrep
from .business.faspr_run import FasprRun
from .business.metabolite_gen import MetabPrep
from .business.best_resolution import FindBestResolution
from .business.find_plddt import CheckPLDDT

from django.core.cache import cache
from django.http import HttpResponse

class FasprPrepAPI(APIView):

    def post(self, request):
        ccid = request.data['CCID']
        gene_ID = request.data['gene_ID']
        angstroms = request.data['angstroms']
        useAlphafold = request.data['toggleAlphaFoldOn']
        file_location = request.data['file_location']
        chain_id = request.data['chain_id']
        faspr_prep = FasprPrep(ccid, gene_ID, angstroms, useAlphafold, file_location, chain_id)
        sequence_length = faspr_prep.sequence_length
        residues = faspr_prep.positions
        get_mut_seq = faspr_prep.get_mut_seq
        repack_pLDDT = faspr_prep.repack_pLDDT
        header = str(f'REMARK created on GTexome ')# {get_mut_seq}
        header += ('\nREMARK FASPR Repacked these residues:')
        header += (str(residues))
        header += ('\n')
        header += faspr_prep.header
        cache.set('pdb_header', header)
        chain_pdb = faspr_prep.chain_pdb
        chain_pdb = "".join(chain_pdb)
        cache.set('chain_pdb', chain_pdb)
        protein_location = faspr_prep.protein_location

        return Response({"residue_output": list(residues),
                         "sequence_length": sequence_length,
                         "mut_seq": get_mut_seq,
                         "repack_pLDDT": repack_pLDDT,
                         "protein_location": protein_location})

    def get(self, request):
        returned_protein_structure = cache.get('protein_structure')
        return Response(returned_protein_structure)


class FasprRunAPI(APIView):
    def post(self, request):
        mutated_sequence = request.data['mutated_sequence']
        protein_location = request.data['protein_location']
        faspr_output = FasprRun(mutated_sequence, protein_location)
        # if 'error' in faspr_output.FASPR_pdb_text:
        #     faspr_output.FASPR_pdb_text = 'error'
        return Response({'protein_structure': faspr_output.FASPR_pdb_text})


class CacheCCIDAPI(APIView):
    def post(self, request):
        ccid = request.data['CCID']
        cache.set('CCID', ccid)
        return Response({'CCID':ccid})

    def get(self, request):
        returned_CCID = cache.get('CCID')
        return Response(returned_CCID)


class CachePositionsAPI(APIView):
    def post(self, request):
        positions = request.POST.getlist('positions[]')
        cache.set('positions', positions)
        return HttpResponse(positions)

    def get(self, request):
        returned_positions = cache.get('positions')
        return Response(returned_positions)

class CacheLengthAPI(APIView):
    def post(self, request):
        sequence_length = request.data['sequence_length']
        cache.set('sequence_length', sequence_length)
        return HttpResponse({'sequence_length':sequence_length})

    def get(self, request):
        returned_length = cache.get('sequence_length')
        return Response(returned_length)


class CacheProteinAPI(APIView):
    def post(self, request):
        protein_structure = request.data['protein_structure']
        cache.set('protein_structure', protein_structure)
        return Response({'protein_structure':protein_structure})

    def get(self, request):
        returned_protein_structure = cache.get('protein_structure')
        return Response(returned_protein_structure)


class MetabPrepAPI(APIView):
    def post(self, request):
        smiles_code = request.data['smiles']
        MetabPrep(smiles_code)
        return Response(True)


class FindResolutionAPI(APIView):
    def post(self, request):
        gene_ID = request.data['gene_ID']
        CCID = request.data['CCID']
        find_best_res = FindBestResolution(gene_ID, CCID)
        resolution = find_best_res.best_resolution
        file_location = find_best_res.file_location
        chain_id = find_best_res.chain_id
        return Response({'resolution':resolution, 'file_location':file_location, 'chain_id':chain_id})


class FindpLDDTAPI(APIView):

    def post(self, request):
        gene_ID = request.data['gene_ID']
        ccid = request.data['CCID']
        find_plddt = CheckPLDDT(gene_ID, ccid)
        plddt_snv = find_plddt.plddt_snv
        plddt_avg = find_plddt.plddt_avg
        return Response({'plddt_snv': plddt_snv, 'plddt_avg': plddt_avg})