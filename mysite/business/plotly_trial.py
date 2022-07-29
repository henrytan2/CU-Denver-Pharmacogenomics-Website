from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output
import dash_table
import dash_bio as dashbio
from dash_bio.utils import PdbParser, create_mol3d_style
from dash import html
import pandas as pd
import dash
from uuid import uuid4
from django.core.cache import cache
import dash_bootstrap_components as dbc
from dash import dcc
import dpd_components as dpd
from django_plotly_dash.consumers import send_to_pipe_channel

from mysite.api.views import CacheCCIDAPI

# cache_instance = CacheCCIDAPI
# CCID = CacheCCIDAPI.retrieve()
CCID = cache.get('CCID')
# print('CCID is', CCID)

app = DjangoDash('MutationViewer')

# residue_numerical = re.findall(r'\d+', CCID)
# parser = PdbParser('FASPR_output.txt')
parser = PdbParser('https://git.io/4K8X.pdb')

data = parser.mol3d_data()
styles = create_mol3d_style(
    data['atoms'], visualization_type='stick', color_element='atom'
)

df = pd.DataFrame(data["atoms"])
# df = df.drop_duplicates(subset=['residue_name'])
df['positions'] = df['positions'].apply(lambda x: ', '.join(map(str, x)))
print(df)
residue_number = 'EMPTY'
# use df residue_index for inputting CCID
app.layout = html.Div(
    [
        # dash_table.DataTable(
        #     id="zooming-specific-residue-table",
        #     columns=[{"name": i, "id": i} for i in df.columns[5:7]],
        #     data=df.to_dict("records"),
        #     row_selectable="single",
        #     fill_width=False,
        #     cell_selectable=True,
        #     page_size=1,
        #     editable=True,
        #     page_current=22,
        #     style_cell={'textAlign': 'center'},
        #     style_as_list_view=True,
        #     row_deletable=True,
        #     selected_columns=[],
        #     selected_rows=[],
        # ),
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
    Input("zooming-specific-residue-table", "selected_rows"),
    prevent_initial_call=True
)

def residue(selected_row):
    row = df.iloc[selected_row]
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

# @app.expanded_callback(
#     Output("output", "children"),
#     Input("residue_number", "value"),
#     # dash.dependencies.Output('residue_number', 'children'),
#     # [dash.dependencies.Input('residue_number', 'residue')]
#     prevent_initial_call=True
#     )
#
# def session_mutation_callback(residue, session_state=None, **kwargs):
#     if session_state is None:
#         raise NotImplementedError("Cannot handle a missing session state")
#     return "New residue is ", residue


# def session_demo_alert_callback(n_clicks, session_state=None, **kwargs):
#     'Output text based on both app state and session state'
#     if session_state is None:
#         raise NotImplementedError("Cannot handle a missing session state")
#     csf = session_state.get('bootstrap_demo_state', None)
#     if not csf:
#         csf = dict(clicks=0, overall=0)
#     else:
#         csf['clicks'] = n_clicks
#         # if n_clicks is not None and n_clicks > csf.get('overall_max',0):
#         #     csf['overall_max'] = n_clicks
#     session_state['bootstrap_demo_state'] = csf
#     return f"Button has been clicked {n_clicks} times since the page was rendered"



liveIn = DjangoDash("LiveInput",
                    serve_locally=True,
                    add_bootstrap_links=False)#problem?

liveIn.layout = html.Div(
    [
        html.I(f'residue zoomed to is {residue_number} currently'),
        # dcc.Markdown(f'CCID is {CCID}'),
        dcc.Input(id='residue_number', type='number', placeholder="residue", min=1, max=1000, step=1),
        html.Div(id="output"),
    ], className="")

def callback_liveIn_button_press(residue_number, **kwargs):

    value = {'residue_number':residue_number,
                 'user':str(kwargs.get('user', 'UNKNOWN'))}
    send_to_pipe_channel(channel_name="mutation_tracker",
                        label="new_mutation",
                        value=value)

    return "Number is  %s" % (residue_number)



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
        # dcc.Graph(id="timeseries_plot"),
        dcc.Input(value=str(uuid4()),
                  id="state_uid",
                  style={'display':'none'},
                 )
        ])

liveOut.layout = generate_liveOut_layout

@liveOut.callback(
    dash.dependencies.Output('output_text', 'children'),
    [dash.dependencies.Input('mutation_pipe', 'value'),
     dash.dependencies.Input('state_uid', 'value'),],
    )

def callback_liveOut_pipe(output_text, state_uid):
    cache_key = _get_cache_key(state_uid)
    state = cache.get(cache_key)
        # If nothing in cache, prepopulate
    if not state:
        state = {}
    user = mutation_tracker.get('user', None)
    residue_number = residue_number.get('residue_number', None)

    return output_text
# def callback_liveOut_pipe_in(named_count, state_uid, **kwargs):
#     'Handle something changing the value of the input pipe or the associated state uid'
#
#     cache_key = _get_cache_key(state_uid)
#     state = cache.get(cache_key)
#
#     # If nothing in cache, prepopulate
#     if not state:
#         state = {}
#
#     # Guard against missing input on startup
#     if not named_count:
#         named_count = {}
#
#     # extract incoming info from the message and update the internal state
#     user = named_count.get('user', None)
#     click_colour = named_count.get('click_colour', None)
#     click_timestamp = named_count.get('click_timestamp', 0)

    # if click_colour:
    #     colour_set = state.get(click_colour, None)
    #
    #     if not colour_set:
    #         colour_set = [(None, 0, 100) for i in range(5)]
    #
    #     _, last_ts, prev = colour_set[-1]

        # Loop over all existing timestamps and find the latest one
        # if not click_timestamp or click_timestamp < 1:
        #     click_timestamp = 0
        #
        #     for _, the_colour_set in state.items():
        #         _, lts, _ = the_colour_set[-1]
        #         if lts > click_timestamp:
        #             click_timestamp = lts
        #
        #     click_timestamp = click_timestamp + 1000

        # if click_timestamp > last_ts:
        #     colour_set.append((user, click_timestamp, prev * random.lognormvariate(0.0, 0.1)),)
        #     colour_set = colour_set[-100:]

    #     state[click_colour] = colour_set
    #     cache.set(cache_key, state, 3600)
    #
    # return "(%s,%s)" % (cache_key, click_timestamp)

# @liveOut.callback(
#     dash.dependencies.Output('output_text', 'text'),
#     [dash.dependencies.Input('internal_state', 'children'),
#      dash.dependencies.Input('state_uid', 'value'),],
#     )

# def callback_show_timeseries(internal_state_string, state_uid, **kwargs):
#     'Build a timeseries from the internal state'
#
#     cache_key = _get_cache_key(state_uid)
#     state = cache.get(cache_key)
#
#     # If nothing in cache, prepopulate
#     if not state:
#         state = {}
#
#     colour_series = {}
#
#     colors = {'red':'#FF0000',
#               # 'blue':'#0000FF',
#               # 'green':'#00FF00',
#               # 'yellow': '#FFFF00',
#               # 'cyan': '#00FFFF',
#               # 'magenta': '#FF00FF',
#               # 'black' : '#000000',
#              }
#
#     # for colour, values in state.items():
#     #     timestamps = [datetime.fromtimestamp(int(0.001*ts)) for _, ts, _ in values if ts > 0]
#     #     #users = [user for user, ts, _ in values if ts > 0]
#     #     levels = [level for _, ts, level in values if ts > 0]
#     #     if colour in colors:
#     #         colour_series[colour] = pd.Series(levels, index=timestamps).groupby(level=0).first()
#
#     # df = pd.DataFrame(colour_series).fillna(method="ffill").reset_index()[-25:]
#
#     # traces = [go.Scatter(y=df[colour],
#     #                      x=df['index'],
#     #                      name=colour,
#     #                      line=dict(color=colors.get(colour, '#000000')),
#     #                     ) for colour in colour_series]
#
#     return {'data':traces,
#             #'layout': go.Layout
#            }
