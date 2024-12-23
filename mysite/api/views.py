from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer,  TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .business.faspr_prep import FasprPrep
from .business.faspr_run import FasprRun
from .business.metabolite_gen import MetabPrep
from .business.best_resolution import FindBestResolution
from .business.find_plddt import CheckPLDDT
from django.core.cache import cache
import logging
from django.shortcuts import redirect
from datetime import date
from datetime import datetime, timedelta
from rest_framework.permissions import AllowAny

error_logger = logging.getLogger('django.error')

class FasprPrepAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, **kwargs):
        ccid = request.data['CCID']
        gene_ID = request.data['gene_ID']
        angstroms = request.data['angstroms']
        useAlphafold = request.data['toggleAlphaFoldOn']
        file_location = request.data['file_location']
        chain_id = request.data['chain_id']
        reported_location = request.data['reported_location']
        faspr_prep = FasprPrep(ccid, gene_ID, angstroms, useAlphafold, file_location, chain_id, reported_location)
        sequence_length = faspr_prep.sequence_length
        residues = faspr_prep.positions
        get_mut_seq = faspr_prep.get_mut_seq
        repack_pLDDT = faspr_prep.repack_pLDDT
        reported_location = faspr_prep.reported_location
        header = str(f'REMARK created on GTExome (https://pharmacogenomics.clas.ucdenver.edu/gtexome/)')
        header += (f'\nREMARK created on: {date.today()}')
        header += (f'\nREMARK using gene ID: {gene_ID}')
        header += (f'\nREMARK from file: {reported_location}')
        header += (f'\nREMARK introducing mutation: {ccid}')
        header += ('\nREMARK FASPR Repacked these residues:')
        header += (str(residues))
        header += ('\n')
        header += faspr_prep.header
        cache.set('pdb_header', header)
        chain_pdb = faspr_prep.chain_pdb
        chain_pdb = "".join(chain_pdb)
        cache.set('chain_pdb', chain_pdb)
        protein_location = faspr_prep.protein_location
        response_dict = {"residue_output": list(residues),
                         "sequence_length": sequence_length,
                         "mut_seq": get_mut_seq,
                         "header": header,
                         "repack_pLDDT": repack_pLDDT,
                         "protein_location": protein_location}
        if kwargs:
            response_dict.update(kwargs)
        return Response(response_dict)

    def get(self, request):
        returned_protein_structure = cache.get('protein_structure')
        return Response(returned_protein_structure)


class FasprRunAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            mutated_sequence = request.data['mutated_sequence']
            protein_location = request.data['protein_location']
            header = request.data['header']
            faspr_output = FasprRun(mutated_sequence, protein_location, header)
            if 'error' in faspr_output.FASPR_pdb_text:
                error_logger.error(faspr_output.FASPR_pdb_text)
                faspr_output.FASPR_pdb_text = 'error with structure'
                # raise ValueError
            return Response({'protein_structure': faspr_output.FASPR_pdb_text})
        except:
            return Response()

class CacheCCIDAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        ccid = request.data['CCID']
        cache.set('CCID', ccid)
        return Response({'CCID': ccid})

    def get(self, request):
        returned_CCID = cache.get('CCID')
        return Response(returned_CCID)


class CachePositionsAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        positions = request.POST.getlist('positions[]')
        cache.set('positions', positions)
        return Response({'positions': positions})

    def get(self, request):
        returned_positions = cache.get('positions')
        return Response(returned_positions)

class CacheLengthAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        sequence_length = request.data['sequence_length']
        cache.set('sequence_length', sequence_length)
        return Response({'sequence_length': sequence_length})

    def get(self, request):
        returned_length = cache.get('sequence_length')
        return Response(returned_length)


class CacheProteinAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        protein_structure = request.data['protein_structure']
        cache.set('protein_structure', protein_structure)
        return Response({'protein_structure': protein_structure})

    def get(self, request):
        returned_protein_structure = cache.get('protein_structure')
        return Response(returned_protein_structure)


class MetabPrepAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        smiles_code = request.data['smiles']
        metabolites = MetabPrep(smiles_code)
        bt_output = metabolites.bt_output
        return Response({'bt_output': bt_output})


class FindResolutionAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, **kwargs):
        gene_ID = request.data['gene_ID']
        CCID = request.data['CCID']
        find_best_res = FindBestResolution(gene_ID, CCID)
        resolution = find_best_res.best_resolution
        file_location = find_best_res.file_location
        chain_id = find_best_res.chain_id
        exp_file_location = find_best_res.file_location
        if resolution.startswith('Downloading'):
            resolution = 'refresh page'
        response_dict = {'resolution': resolution,
                         'file_location': file_location,
                         'chain_id': chain_id,
                         'exp_file_location':exp_file_location,
                         }
        if kwargs:
            response_dict.update(kwargs)
        return Response(response_dict)


class FindPlddtAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, **kwargs):
        gene_ID = request.data['gene_ID']
        ccid = request.data['CCID']
        find_plddt = CheckPLDDT(gene_ID, ccid)
        plddt_snv = find_plddt.plddt_snv
        plddt_avg = find_plddt.plddt_avg
        charge_change = find_plddt.charge_change
        disulfide_check = find_plddt.disulfide_check
        proline_check = find_plddt.proline_check
        buried = find_plddt.buried
        hydrogen_bond = find_plddt.hbond
        salt_bridge = find_plddt.salt_bridge
        recommendation = find_plddt.recommendation
        af_file_location = find_plddt.file_location
        pocket_input = find_plddt.pocket_info
        pocket_info = []
        if pocket_input == 'No Adjacent Pockets' or pocket_input == 'no pocket info':
            pocket_info = 'No Adjacent Pockets'
        else:
            for key, value in pocket_input.items():
                pocket_number = key
                volume = value[0]
                druggability = value[1]
                pocket_info.append(f"pocket # {pocket_number} with volume {volume} Å\u00b3 and druggability {druggability}")

        response_dict = {
                'plddt_snv': plddt_snv,
                'plddt_avg': plddt_avg,
                'charge_change': charge_change,
                'disulfide_check': disulfide_check,
                'proline_check': proline_check,
                'buried': buried,
                'hydrogen_bond': hydrogen_bond,
                'salt_bridge': salt_bridge,
                'recommendation': recommendation,
                'af_file_location': af_file_location,
                'pocket_info': pocket_info,
            }
        if kwargs:
            response_dict.update(kwargs)
        return Response(response_dict)

    def get(self, request):
        return Response(request)

class CustomAPIRenderer(BrowsableAPIRenderer):
    renderer_classes = [BrowsableAPIRenderer, TemplateHTMLRenderer, JSONRenderer]

    def get_default_renderer(self, view):
        return JSONRenderer()

    @property
    def template(self):
        return 'rest_framework/api.html'


class FindPlddtPublicAPI(APIView):

    renderer_classes = [CustomAPIRenderer]

    def post(self, request):
        try:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                jwt = auth_header.split()[1]
                AccessToken(jwt)
        except TokenError as e:
            return FindPlddtAPI.post(FindPlddtAPI(), request)

    def get(self, request):
        return Response()


class FindResolutionPublicAPI(APIView):

    renderer_classes = [CustomAPIRenderer]

    def post(self, request):
        try:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                jwt = auth_header.split()[1]
                AccessToken(jwt)
        except TokenError as e:
            return redirect('user_accounts:account-welcome')

        return FindResolutionAPI.post(FindResolutionAPI(), request)

    def get(self, request):
        return Response()


@method_decorator(csrf_exempt, name='dispatch')
class FasprPrepPublicAPI(APIView):

    renderer_classes = [CustomAPIRenderer]

    @method_decorator(csrf_exempt)
    def post(self, request):
        try:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                jwt = auth_header.split()[1]
                AccessToken(jwt)
        except TokenError as e:
            return redirect('user_accounts:account-welcome')

        return FasprPrepAPI.post(FasprPrepAPI(), request)

    def get(self, request):
        return Response(request)
