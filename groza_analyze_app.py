import locale

import streamlit as st
from figures import get_plot_distance_per_killer, get_plot_n_unique_weapons_per_player, get_plot_kills, get_plot_kd, \
    get_plot_deathes, get_plot_weapons, get_max_kills_per_hour
from groza_process import top_killers, get_players, favourite_weapon_per_player, GROZA_SERVER_FILES



st.set_page_config(
        page_title=f"Groza: Октябрьский сезон 2023", page_icon="⚡",
)
selected_server = st.selectbox(
   "Выберите сервер для просмотра статистики",
   tuple(GROZA_SERVER_FILES.keys()),
   index=3,
)
st.header(f"⚡ Groza  {selected_server}: Октябрьский вайп 2023")
st.subheader("Стрелки и стреляемые этого сервера")

selected_players = st.multiselect(
    'Выбранные игроки',
    get_players(selected_server),
    list(top_killers(server=selected_server).index))
killers, kd, distances, most_death, monster = st.tabs(["Киллеры", "Убийства/Смерти","Дистанции убийства", "Невезунчики", "RRRRAMPAGE"])
selected_players = frozenset(selected_players)

with killers:
    st.plotly_chart(get_plot_kills(players=selected_players, server=selected_server), theme="streamlit", use_container_width=True)
with kd:
    st.plotly_chart(get_plot_kd(players=selected_players, server=selected_server), theme="streamlit", use_container_width=True)
with distances:
    st.plotly_chart(get_plot_distance_per_killer(players=selected_players, server=selected_server),
                    theme="streamlit", use_container_width=True)
with most_death:
    st.plotly_chart(get_plot_deathes(players=selected_players, server=selected_server), theme="streamlit", use_container_width=True)
with monster:
    st.plotly_chart(get_max_kills_per_hour(players=selected_players, server=selected_server), theme="streamlit", use_container_width=True)

st.subheader("Ак-74 или каменный нож - гроза этого сервера?")
top_weapons, fav_weapon, top_by_kills, last_by_kills = \
    st.tabs(["Количество уникальных вещей, которыми игрок убил",
             "Любимое оружие",
             "Топ вещей по убийствам",
             "Топ редких вещей по убийствам"])
with top_weapons:
    st.plotly_chart(get_plot_n_unique_weapons_per_player(players=selected_players, server=selected_server),
                    theme="streamlit", use_container_width=True)
with fav_weapon:
    st.dataframe(favourite_weapon_per_player(players=selected_players, server=selected_server))
with top_by_kills:
    st.plotly_chart(get_plot_weapons(top=15, ascending=False, server=selected_server), theme="streamlit")
with last_by_kills:
    st.plotly_chart(get_plot_weapons(top=25, ascending=True, server=selected_server), theme="streamlit")