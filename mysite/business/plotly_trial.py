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
from django_plotly_dash.consumers import send_to_pipe_channel
from django_plotly_dash.util import pipe_ws_endpoint_name
import re


print('pipe_ws_endpoint_name', pipe_ws_endpoint_name())


# parser = PdbParser('FASPR_output.txt')
parser = PdbParser('https://git.io/4K8X.pdb')

data = parser.mol3d_data()
styles = create_mol3d_style(
    data['atoms'], visualization_type='stick', color_element='atom'
)

df = pd.DataFrame(data["atoms"])
# df = df.drop_duplicates(subset=['residue_name'])
df['positions'] = df['positions'].apply(lambda x: ', '.join(map(str, x)))

# use df residue_index for inputting CCID

app = DjangoDash('MutationViewer')

app.layout = html.Div(
    [
        html.Div(id="output_text"),
        dcc.Slider(
            id="mutation_pipe",
            min=1,
            max=200,
            step=1,
            marks={100: "100", 150: "150"},
            value=55,
        ),
        dashbio.Molecule3dViewer(
            id="zooming-specific-molecule3d-zoomto",
            modelData=data,
            styles=styles
        ),
    ]
)


@app.callback(
    Output("zooming-specific-molecule3d-zoomto", "zoomTo"),
    Output("zooming-specific-molecule3d-zoomto", "labels"),
    [Input(component_id='mutation_pipe', component_property='value')]
)


def residue(value):
    print('current value in callback is', value)
    row = df.iloc[[value]]
    row['positions'] = row['positions'].apply(lambda x: [float(x) for x in x.split(',')])
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
    ]

#
# @app.callback(
#     Output("zooming-specific-molecule3d-zoomto", "zoomTo"),
#     Output("zooming-specific-molecule3d-zoomto", "labels"),
#     Input("zooming-specific-residue-table", "selected_rows"),
#     prevent_initial_call=True
# )
#
# def residue(selected_row):
#     row = df.iloc[selected_row]
#     row['positions'] = row['positions'].apply(lambda x: [float(x) for x in x.split(',')])
#     return [
#         {
#             "sel": {"chain": row["chain"], "resi": row["residue_index"]},
#             "animationDuration": 1500,
#             "fixedPath": True,
#         },
#         [
#             {
#                 "text": "Residue Name: {}".format(row["residue_name"].values[0]),
#                 "position": {
#                     "x": row["positions"].values[0][0],
#                     "y": row["positions"].values[0][1],
#                     "z": row["positions"].values[0][2],
#                 },
#             }
#         ],
#     ]


# def retreive_CCID(mutation_pipe):
#     CCID = cache.get('CCID')
#     print(CCID)
#     residue_numerical = re.findall(r'\d+', CCID)
#     return f"the mutation_pipe is {mutation_pipe} not {CCID} at {residue_numerical[0]}"
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



liveOut = DjangoDash("LiveOutput")

def _get_cache_key(state_uid):
    return "demo-liveout-s6-%s" % state_uid

def generate_liveOut_layout():
    'Generate the layout per-app, generating each tine a new uuid for the state_uid argument'
    return html.Div([
        dpd.Pipe(id="mutation_pipe",
                 value=None,
                 label="new_mutation",
                 channel_name="mutation_tracker"),
        html.Div(id="internal_state",
                 children="No state has been computed yet",
                 style={'display':'none'}),
        html.Div(id="output_text"),
        dcc.Input(value=str(uuid4()),
                  id="state_uid",
                  style={'display':'none'},
                 )
        ])
#
# liveOut.layout = generate_liveOut_layout
#
# @liveOut.callback(
#     dash.dependencies.Output('output_text', 'children'),
#     [dash.dependencies.Input('mutation_pipe', 'value'),
#      dash.dependencies.Input('state_uid', 'value'),],
#     )
#
# def callback_liveOut_pipe(output_text, state_uid):
#     cache_key = _get_cache_key(state_uid)
#     state = cache.get(cache_key)
#         # If nothing in cache, prepopulate
#     if not state:
#         state = {}
#     user = mutation_tracker.get('user', None)
#     residue_number = residue_number.get('residue_number', None)
#
#     return output_text
