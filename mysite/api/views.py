from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer,  TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from .business.faspr_prep import FasprPrep
from .business.faspr_run import FasprRun
from .business.metabolite_gen import MetabPrep
from .business.best_resolution import FindBestResolution
from .business.find_plddt import CheckPLDDT
from django.core.cache import cache
import logging
from datetime import date
from rest_framework.permissions import AllowAny

error_logger = logging.getLogger('django.error')

class FasprPrepAPI(APIView):
    permission_classes = (AllowAny,)

    @method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
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

    @method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
    def get(self, request):
        returned_protein_structure = cache.get('protein_structure')
        return Response(returned_protein_structure)


class FasprRunAPI(APIView):
    permission_classes = (AllowAny,)

    @method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
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


class MetabPrepAPI(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(auto_schema=None)
    def post(self, request):
        smiles_code = request.data['smiles']
        metabolites = MetabPrep(smiles_code)
        bt_output = metabolites.bt_output
        return Response({'bt_output': bt_output})

class FindResolutionAPI(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(auto_schema=None)
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

    @method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
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

    @method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
    def get(self, request):
        return Response(request)

class FindPlddtPublicAPI(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Find pLDDT Score (Public)",
        operation_description="""Public endpoint to find pLDDT (predicted Local Distance Difference Test) scores. 
        If a valid JWT token is provided, it will use the authenticated endpoint""",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'gene_ID': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Identifier for gene"
                ),
                'CCID': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Identifier for CCID"
                ),
            },
            required=['gene_ID', 'CCID']
        ),
        responses={
            200: openapi.Response(
                description="Successfully retrieved pLDDT score",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'plddt_score': openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            description="The pLDDT score for the protein",
                            example=92.5
                        ),
                    }
                )
            ),
            400: openapi.Response(
                description="Bad request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Error message"
                        )
                    }
                )
            ),
            401: "Invalid authentication token",
            500: "Internal server error"
        },
        tags=['Protein Analysis'],
        security=[
            {'Bearer': []}
        ],
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token (required)",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def post(self, request):
        """
        Find pLDDT score for a protein. Can be accessed with or without authentication.
        If authenticated, uses the authenticated endpoint's functionality.
        """
        try:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                jwt = auth_header.split()[1]
                AccessToken(jwt)
                return FindPlddtAPI.post(FindPlddtAPI(), request)
            else:
                return Response("Auth header must begin with Bearer", status=401)
        except TokenError as e:
            return Response('Could not validate credentials', status=401)



class FindResolutionPublicAPI(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Find Resolution (Public)",
        operation_description="""Public endpoint to find protein resolution data. 
        If a valid JWT token is provided, processes the request""",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'CCID': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Identifier for the protein structure",
                    example="p.His144Gln"
                ),
                'gene_id': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Identifier in the gene structure",
                    example="ENSG00000001561"
                ),
            },
            required=['CCID', 'gene_id']
        ),
        responses={
            200: openapi.Response(
                description="Successfully retrieved resolution data",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'resolution': openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            description="Resolution in Angstroms",
                            example=2.5
                        ),
                        'method': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Method used for structure determination",
                            example="X-RAY DIFFRACTION"
                        ),
                        # Add other response fields based on what FindResolutionAPI returns
                    }
                )
            ),
            400: openapi.Response(
                description="Bad request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Error message"
                        )
                    }
                )
            ),
            401: "Invalid authentication credentials",
            500: "Internal server error"
        },
        tags=['Protein Structure Analysis'],
        security=[
            {'Bearer': []}
        ],
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token (required) - If provided and valid, enables additional features",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def post(self, request):
        """
        Find resolution data for a protein structure.
        Accessible without authentication, but authenticated users may receive additional data.
        Invalid or missing authentication returns 401.
        """
        try:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                jwt = auth_header.split()[1]
                AccessToken(jwt)
            else:
                return Response("Auth header must begin with Bearer", status=401)
        except TokenError as e:
            return Response('Could not validate credentials', status=401)

        return FindResolutionAPI.post(FindResolutionAPI(), request)

    @method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
    def get(self, request):
        return Response()


@method_decorator(csrf_exempt, name='dispatch')
class FasprPrepPublicAPI(APIView):

    @method_decorator(csrf_exempt)
    @swagger_auto_schema(
        operation_summary="Faspr Prep (Public)",
        operation_description="""Public endpoint to prepare PDB 
            JWT Required""",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'CCID': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Identifier for the protein structure",
                    example="p.His144Gln"
                ),
                'angstroms': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="",
                    example="10"
                ),
                'chain_id': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Chain identifier in the protein structure",
                    example="A"
                ),
                'file_location': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="File location to store PDBGEN file",
                    example="/home/boss/website_activity/remote_pdb/remote_pdb/proteins/lr/pdb4lr2.ent"
                ),
                'gene_ID': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Identifier for the gene",
                    example="ENSG00000001561"
                ),
                'reported_location': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Location for the pdb file",
                    example="AF-Q9Y6X5-F1-model_v1.pdb"
                ),
                'toggleAggleFoldOn': openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description="AlphaFold2 or Experimental parameter",
                    example="true"
                )
            },
            required=['CCID', 'angstroms', 'chain_id', 'file_location','gene_id','reported_location','toggleAlphaFoldOn']  # List required fields
        ),
        responses={
            200: openapi.Response(
                description="Successfully retrieved resolution data",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'resolution': openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            description="Resolution in Angstroms",
                            example=2.5
                        ),
                        'method': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Method used for structure determination",
                            example="X-RAY DIFFRACTION"
                        ),
                    }
                )
            ),
            400: openapi.Response(
                description="Bad request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Error message"
                        )
                    }
                )
            ),
            401: "Invalid authentication credentials",
            500: "Internal server error"
        },
        tags=['Protein Structure Analysis'],
        security=[
            {'Bearer': []}
        ],
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token (required)",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def post(self, request):
        try:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                jwt = auth_header.split()[1]
                AccessToken(jwt)
                return FasprPrepAPI.post(FasprPrepAPI(), request)
            else:
                return Response("Bearer must be present in authorization header")
        except TokenError as e:
            return Response('Could not validate credentials', status=401)



    @method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
    def get(self, request):
        return Response(request)
