from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output
import dash_bio as dashbio
from dash_bio.utils import PdbParser, create_mol3d_style
from dash import html
import pandas as pd
from dash import dash_table
from uuid import uuid4
from django.core.cache import cache
from dash import dcc
import dpd_components as dpd
from dash.exceptions import PreventUpdate
import re

# parser = PdbParser('FASPR_output.txt')
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
        # html.Tbody([
        #     html.Tr([
        #         html.Td(0, id='memory-clicks'),
        #         ])
        #     ]),
        # dcc.Store(id='memory'),
        dcc.Slider(
            id="mutation_slider",
            min=1,
            max=100,#cache.get('sequence_length'),
            step=1,
            value=1,#cache.get('positions'),
            marks={50: "50", 100: "100", 150: "150", 200: "200", 250: "250", 300: "300",
                   350: "350", 400: "400", 450: "450", 500: "500", 550: "550", 600: "600",
                   650: "650", 700: "700", 850: "850", 900: "900", 950: "950", 1000: "1000"},
        ),
        dashbio.Molecule3dViewer(
            id="molecule3d-zoomto",
            modelData=data,
            styles=styles,
        ),
    ]
)


@mutation_app.callback(
    Output(component_id="molecule3d-zoomto", component_property="zoomTo"),
    Output(component_id="molecule3d-zoomto", component_property="labels"),
    Output(component_id="output_text", component_property="children"),
    Output(component_id="mutation_slider", component_property="max"),
    Output(component_id="molecule3d-zoomto", component_property='modelData'),
    [Input(component_id="mutation_slider", component_property='value')],
    prevent_initial_call=True
)


def residue(value):
    parser = PdbParser('FASPR_output.txt')
    reloaded_protein = parser.mol3d_data()
    CCID = cache.get('CCID')
    print('CCID cached is ', CCID)
    length = int(cache.get('sequence_length'))
    print('sequence_length is ', length)
    repacked = cache.get('positions')
    print('residues cached (called from plotly) are', repacked)
    residue_numerical = int(re.findall(r'\d+', CCID)[0])

    row = df.iloc[[value]]
    row['positions'] = row['positions'].apply(lambda x: [float(x) for x in x.split(',')])
    output_text = f'you have zoomed to {value} out of {length}, last repacked residue at: {repacked}, SNV at: {residue_numerical}'

    if value is None:
        raise PreventUpdate

    if value > length:
        output_text = "try lower"

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
        # html.Div([output_text]),
        reloaded_protein,
        # positions
    ]


# atomLabelsShown = True,
#


# liveIn = DjangoDash("LiveInput",
#                     serve_locally=True,
#                     add_bootstrap_links=False)#problem?

# liveIn.layout = html.Div(
#     [
#         # html.Div(id="output_text"),
#         dcc.Input(id='mutation_pipe', type='number', placeholder="residue", min=1, max=1000, step=1),
#         dcc.Interval(
#             id='interval-timer',
#             interval=1*1000,
#             n_intervals=0
#         )
#     ], className="")

# @liveIn.callback(
#     Output(component_id='output_text', component_property='children'),
#     Input(component_id='mutation_pipe', component_property='value')
# )
# def retreive_CCID(mutation_pipe):
#     CCID = cache.get('CCID')
#     residue_numerical = re.findall(r'\d+', CCID)
#     return f"the mutation_pipe is {mutation_pipe} not {CCID} at {residue_numerical}"

#
# @liveIn.callback(
#     dash.dependencies.Output('output_text', 'children'),
#     [dash.dependencies.Input('mutation_pipe', 'value'),
#      dash.dependencies.Input('state_uid', 'value'),],
#     )
#
# def callback_liveIn_button_press(residue_number, **kwargs):
#
#     value = {'residue_number':residue_number,
#                  'user':str(kwargs.get('user', 'UNKNOWN'))}
#     send_to_pipe_channel(channel_name="mutation_tracker",
#                         label="new_mutation",
#                         value=value)
#
#     return "Number is  %s" % (residue_number)



# liveOut = DjangoDash("LiveOutput")
#
# def _get_cache_key(state_uid):
#     return "demo-liveout-s6-%s" % state_uid
#
# def generate_liveOut_layout():
#     'Generate the layout per-app, generating each tine a new uuid for the state_uid argument'
#     return html.Div([
#         dpd.Pipe(id="mutation_pipe",
#                  value=None,
#                  label="new_mutation",
#                  channel_name="mutation_tracker"),
#         html.Div(id="internal_state",
#                  children="No state has been computed yet",
#                  style={'display':'none'}),
#         html.Div(id="output_text"),
#         dcc.Input(value=str(uuid4()),
#                   id="state_uid",
#                   style={'display':'none'},
#                  )
#         ])
