from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output
import dash_bio as dashbio
from dash_bio.utils import PdbParser, create_mol3d_style
from dash import html
import pandas as pd
from dash import dash_table
from django.core.cache import cache
from dash import dcc
from dash.exceptions import PreventUpdate
import re
import os

# parser = PdbParser('glygly.pdb')
parser = PdbParser('https://git.io/4K8X.pdb')

data = parser.mol3d_data()
styles = create_mol3d_style(
    data['atoms'], visualization_type='stick', color_element='atom'
)

df = pd.DataFrame(data["atoms"])
# df = df.drop_duplicates(subset=['residue_name'])
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
                   650: "650", 700: "700", 850: "850", 900: "900", 950: "950", 1000: "1000"},
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
    with open('FASPR_output_cached.txt', 'w+') as f:
        f.write(pdb_cached)
    os.chmod('FASPR_output_cached.txt', 0o775)
    parser = PdbParser('FASPR_output_cached.txt')
    reloaded_protein = parser.mol3d_data()
    df = pd.DataFrame(data["atoms"])
    # df = df.drop_duplicates(subset=['residue_name'])
    df['positions'] = df['positions'].apply(lambda x: ', '.join(map(str, x)))

    repacked = cache.get('positions')
    # print('residues cached (called from plotly) are', repacked)
    residue_numerical = int(str(re.findall(r'\d+', CCID)[0]))

    row = df.iloc[[value]]
    row['positions'] = row['positions'].apply(lambda x: [float(x) for x in x.split(',')])

    if value is None:
        raise PreventUpdate

    if value > length:
        value = length

    output_text = f'You have zoomed to residue {value}. The SNV is at: {residue_numerical}. Full length is {length}'
    marks_output = {(residue_numerical): {'label': f'{residue_numerical}', 'style': {'color': '#f50'}}, 50: "50",
                    100: "100", 150: "150", 200: "200", 250: "250", 300: "300",
                    350: "350", 400: "400", 450: "450", 500: "500", 550: "550", 600: "600",
                    650: "650", 700: "700", 850: "850", 900: "900", 950: "950", 1000: "1000"}

    output_text_footer = f'The repacked residues are: {repacked}'

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
