from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output
import dash_bio as dashbio
from dash_bio.utils import PdbParser, create_mol3d_style
from dash import html
import pandas as pd
from django.core.cache import cache
from dash import dcc
from dash.exceptions import PreventUpdate
import re
import os
import hashlib
import logging

error_logger = logging.getLogger('django.error')


parser = PdbParser('./pharmacogenomics_website/glygly.pdb')
# parser = PdbParser('https://git.io/4K8X.pdb')

data = parser.mol3d_data()
styles = create_mol3d_style(
    data['atoms'], visualization_type='stick', color_element='atom'
)

df = pd.DataFrame(data["atoms"])
df = df.drop_duplicates(subset=['residue_name'])

df['positions'] = df['positions'].apply(lambda x: ', '.join(map(str, x)))

mutation_app = DjangoDash('MutationViewer')

mutation_app.layout = html.Div(
    [
        html.Div(id="output_text"),
        dcc.Slider(
            id="mutation_slider",
            min=1,
            max=100,
            step=1,
            value=1,
            marks={50: "50", 100: "100", 150: "150", 200: "200", 250: "250", 300: "300",
                   350: "350", 400: "400", 450: "450", 500: "500", 550: "550", 600: "600",
                   650: "650", 700: "700", 850: "850", 900: "900", 950: "950", 1000: "1000",
                   1100: "1100", 1150: "1150", 1200: "1200", 1250: "1250", 1300: "1300",
                   1350: "1350", 1400: "1400", 1450: "1450", 1500: "1500", 1550: "1550", 1600: "1600",
                   1650: "1650", 1700: "1700", 1850: "1850", 1900: "1900", 1950: "1950", 2000: "2000"
                   },
        ),
        dashbio.Molecule3dViewer(
            id="molecule3d-zoomto",
            modelData=data,
            styles=styles,
        ),
        html.Div(id="output_text_footer"),
    ]
)


@mutation_app.callback(
    Output(component_id="molecule3d-zoomto", component_property="zoomTo"),
    Output(component_id="molecule3d-zoomto", component_property="labels"),
    Output(component_id="output_text", component_property="children"),
    Output(component_id="mutation_slider", component_property="max"),
    Output(component_id="molecule3d-zoomto", component_property='modelData'),
    Output(component_id="mutation_slider", component_property='marks'),
    Output(component_id="output_text_footer", component_property="children"),
    [Input(component_id="mutation_slider", component_property='value')],
    prevent_initial_call=False
)

def residue(value):
    CCID = cache.get('CCID')
    length = int(cache.get('sequence_length'))
    pdb_cached = cache.get('protein_structure')
    with open('FASPR_output_cached.pdb', 'w+') as f:
        f.write(pdb_cached)
    os.chmod('FASPR_output_cached.pdb', 0o775)
    dpd_parsed_file = PdbParser('FASPR_output_cached.pdb')
    reloaded_protein = dpd_parsed_file.mol3d_data()

    hasher_for_cache = hashlib.sha1()
    protein_structure_from_cache = pdb_cached.encode('utf-8')
    hasher_for_cache.update(protein_structure_from_cache)
    hashed_pdb_from_cache = hasher_for_cache.hexdigest()

    f = open('FASPR_output_cached.pdb', 'r')
    protein_structure_from_file = f.readlines()
    f.close()

    hasher_for_file = hashlib.sha1()
    protein_structure_from_file = ''.join(protein_structure_from_file)
    protein_structure_from_file = protein_structure_from_file.encode('utf-8')
    hasher_for_file.update(protein_structure_from_file)
    hashed_pdb_from_file = hasher_for_file.hexdigest()

    df = pd.DataFrame(reloaded_protein["atoms"])

    df['positions'] = df['positions'].apply(lambda x: ', '.join(map(str, x)))
    df = df.drop_duplicates(subset=['residue_name', 'residue_index'])
    row = df.iloc[[value]]
    row['positions'] = row['positions'].apply(lambda x: [float(x) for x in x.split(',')])

    repacked = cache.get('positions')
    residue_numerical = int(str(re.findall(r'\d+', CCID)[0]))
    if value is None:
        print('value is none')
        raise PreventUpdate

    if value > length:
        print('value is > len')
        value = length

    output_text = f'You have zoomed to residue {value}. The SNV is at: {residue_numerical}. Full length is {length}'
    marks_output = {(residue_numerical): {'label': f'{residue_numerical}', 'style': {'color': '#f50'}}, 50: "50",
                    100: "100", 150: "150", 200: "200", 250: "250", 300: "300",
                    350: "350", 400: "400", 450: "450", 500: "500", 550: "550", 600: "600",
                    650: "650", 700: "700", 750: "750", 800: "800", 850: "850", 900: "900",
                    950: "950", 1000: "1000", 1100: "1100", 1150: "1150", 1200: "1200", 1250: "1250",
                    1300: "1300", 1350: "1350", 1400: "1400", 1450: "1450", 1500: "1500", 1550: "1550",
                    1600: "1600", 1650: "1650", 1700: "1700", 1750: "1750", 1800: "1800", 1850: "1850",
                    1900: "1900", 1950: "1950", 2000: "2000"
                    }

    output_text_footer = f'The repacked residues are: {repacked}'

    if hashed_pdb_from_file != hashed_pdb_from_cache:
        output_text = 'Stored pdb file does not match cache. Recommend recreating protein'
        error_logger.error(output_text)
        raise Exception(output_text)

    return [
        {
            "sel": {"chain": row["chain"], "resi": row["residue_index"]},
            "animationDuration": 1500,
            "fixedPath": True,
        },
        [
            {
                "text": "Residue Name: {}".format(row["residue_name"].values[0]),
                "position": {
                    "x": row["positions"].values[0][0],
                    "y": row["positions"].values[0][1],
                    "z": row["positions"].values[0][2],
                },
            }
        ],
        output_text,
        length,
        reloaded_protein,
        marks_output,
        output_text_footer,
    ]
