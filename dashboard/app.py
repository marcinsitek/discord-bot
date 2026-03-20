import datetime
import os
from datetime import datetime

import pandas as pd
import streamlit as st
import plotly.express as px

from db.db import DBClient
from dashboard.utils import (
    Plot,
    User,
    get_messages,
    get_messages_count,
    get_min_message_ts,
    get_users,
    create_plot,
)


dbc = DBClient(
    dbname=os.getenv("POSTGRES_DB"), 
    user=os.getenv("POSTGRES_USER"), 
    password=os.getenv("POSTGRES_PASSWORD"), 
    host='postgres'
)

users_from_db = get_users(dbc)
cmap = px.colors.sequential.Plasma
users = []
counter = 0
for i, user in enumerate(users_from_db):
    users.append(User(
        name=user, 
        value=user,
        colour=cmap[i % len(cmap)]
    )
)
    counter = i
users.append(User(
    name='ALL',  
    value=f"""{"', '".join(users_from_db)}""",
    colour=cmap[(counter+1) % len(cmap)]
    )
)


plot = Plot(
    title='Number of messages',
    x_title='date',
    y_title='Count [#]',
    y_format='.0f',
)


st.set_page_config(layout="wide", page_title="discord-bot-dashboard")

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 400px !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


with st.sidebar:
    with st.expander("Users", expanded=True):

        def on_change_users():
            if st.session_state["users"] is None:
                st.session_state["users"] = users
            else:
                st.query_params.pop("users", None)

        def default_users():
            from_query = st.query_params.get_all("users")
            if len(from_query) > 0:
                return [user for user in users if user.name in from_query]
            return [user for user in users if user.name == 'uksw_user']

        selected_users = st.multiselect(
            label="Users",
            label_visibility="collapsed",
            options=users,
            format_func=lambda a: a.name,
            default=default_users(),
            key="users",
            on_change=on_change_users,
        )
        st.query_params["user"] = selected_users


a1, a2 = st.columns([10, 1])
with a1:
    st.title(", ".join([user.name for user in selected_users]))

messages_count_df = get_messages_count(dbc, users=selected_users)
start_dt = get_min_message_ts(dbc).date()
end_dt = datetime.now().date()
fig, fig_config = create_plot(messages_count_df, start_dt, end_dt, plot, users)
messages_df = get_messages(dbc, users=selected_users)

with st.container(border=True):
    st.plotly_chart(fig, width='stretch', config=fig_config)
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.popover("Raw data", icon=":material/table:", width='stretch'):
            st.markdown(plot.title)
            st.dataframe(
                messages_count_df,
                hide_index=True,
                width='stretch',
                column_config={
                    "y": st.column_config.NumberColumn(format="%.8g")
                },
            )

column_config = {
    "message_user": st.column_config.TextColumn("message_user", width=80),
    "message_ts": st.column_config.DatetimeColumn("message_ts", width=130),
}


with st.container(border=True):
    st.markdown("**Messages**")
    st.dataframe(messages_df, hide_index=True, column_config=column_config)
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.popover("Raw data", icon=":material/table:", use_container_width=True):
            st.markdown("Messages")
            st.dataframe(
                messages_df,
                hide_index=True,
                use_container_width=True,
            )
