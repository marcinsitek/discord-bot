from datetime import datetime
from dataclasses import dataclass

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from db.db import DBClient

@dataclass(frozen=True)
class User:
    name: str
    value: str
    colour: str

@dataclass(frozen=True)
class Plot:
    title: str
    x_title: str
    y_title: str
    y_format: str | None = None

def get_users(dbclient: DBClient) -> list:
    QUERY = "SELECT DISTINCT message_user FROM messages;"
    users = dbclient.retrieve(QUERY).iloc[:,0].to_list()
    return users

def get_min_message_ts(dbclient: DBClient) -> datetime:
    QUERY = "SELECT MIN(message_ts) FROM messages;"
    min_ts = dbclient.retrieve(QUERY).iloc[0, 0]
    return min_ts

def get_messages(dbclient: DBClient, users: list[User]) -> pd.DataFrame:
    names = [user.name for user in users]
    if "ALL" in names:
        query = """
            SELECT *
            FROM messages;
        """
    else:
        names_sql = "', '".join(names)
        query = f"""
            SELECT *
            FROM messages
            WHERE message_user IN ('{names_sql}');
        """
    print(query)
    return dbclient.retrieve(query)

def get_messages_count(dbclient: DBClient, users: list[User]) -> pd.DataFrame:
    query = ''
    for i, user in enumerate(users):
        query += f"""
            {'UNION' if i > 0 else ''}
            SELECT 
                '{user.name}' as message_user, 
                message_ts::date as date, 
                count(*) as count 
            FROM messages
            WHERE message_user IN ('{user.value}')
            GROUP BY 1,2
        """
    query += ';'
    messages_df = dbclient.retrieve(query)
    return messages_df

def create_scatter_plot(df: pd.DataFrame, users: list[User]):
    DEFAULT_PLOT_CONFIG = {
    "modeBarButtonsToRemove": ["select2d", "lasso2d", "zoomIn2d", "zoomOut2d"],
    "displayModeBar": True
    }

    fig = go.Figure()
    for user in users:
        segment_df = df[df['message_user']==user.name].sort_values(by='date', ascending=True)
        fig.add_trace(
            go.Scatter(
                x=segment_df["date"],
                y=segment_df["count"],
                mode="lines+markers",
                name=user.name,
                marker_color=user.colour,
            )
        )
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="left", x=0.7)
    )
    fig.update_xaxes(
        showspikes=True,
        spikedash="solid",
        spikemode="across+marker",
        spikethickness=1,
    )
    fig.update_xaxes(showgrid=True)
    return fig, DEFAULT_PLOT_CONFIG


def create_plot(
    df: pd.DataFrame,
    start_dt: datetime.date,
    end_dt: datetime.date,
    plot: Plot,
    users: list[User]
):

    fig, DEFAULT_PLOT_CONFIG = create_scatter_plot(df, users)

    fig.update_layout(
        title=plot.title,
        title_font_size=17,
        title_subtitle=go.layout.title.Subtitle(
            text=plot.title, font_color="#000037"
        ),
        hovermode="x unified",
    )
    fig.update_xaxes(
        title=plot.x_title,
        range=[start_dt - pd.Timedelta(days=1), end_dt + pd.Timedelta(days=1)],
    )
    fig.update_yaxes(
        title=plot.y_title,
        showspikes=True,
        spikedash="solid",
        spikemode="across",
        spikesnap="cursor",
        spikethickness=1,
        fixedrange=True,
    )
    if plot.y_format is not None:
        fig.update_yaxes(tickformat=plot.y_format)

    fig.update_layout(margin=dict(l=67))
    return fig, DEFAULT_PLOT_CONFIG
