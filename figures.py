from functools import lru_cache

import plotly.express as xx

from groza_process import distances_per_players, weapons_per_player, get_kills, get_kill_death_stats, get_victims, \
    weapons_with_kills, max_killer_within_hour


@lru_cache(maxsize=None)
def get_plot_distance_per_killer(players: frozenset, server):
    return xx.box(distances_per_players(players=players, server=server), x="имя игрока", y="расстояние")


@lru_cache(maxsize=None)
def get_plot_kills(players: frozenset, server):
    return xx.bar(get_kills(players=players, server=server), x="имя игрока", y="количество убийств", color="количество убийств")


@lru_cache(maxsize=None)
def get_plot_kd(players: frozenset, server):
    return xx.bar(get_kill_death_stats(players=players, server=server), x="имя игрока", y="Убийства/Cмерти",
                  color='Убийства/Cмерти')

@lru_cache(maxsize=None)
def get_plot_n_unique_weapons_per_player(players: frozenset, server):
    return xx.bar(weapons_per_player(players=players, server=server), x="имя игрока", y="кол-во уникальных", color='кол-во уникальных')

@lru_cache(maxsize=None)
def get_plot_deathes(players: frozenset, server):
    return xx.bar(get_victims(players=players, server=server), x="имя игрока", y="количество смертей", color='количество смертей')


@lru_cache(maxsize=None)
def get_plot_weapons(server, top, ascending):
    if ascending:
        title = "Самые редкие вещи по убийствам"
    else:
        title = "Топ вещей по убийствам"
    return xx.bar(weapons_with_kills(server=server, top=top, ascending=ascending), x="количество убийств", y="оружие", orientation='h', title=title)


@lru_cache(maxsize=None)
def get_max_kills_per_hour(server, players: frozenset):
    return xx.bar(max_killer_within_hour(players=players, server=server),
                  y='имя игрока', x='Максимальное количество убийств', orientation='h',
                  color='Максимальное количество убийств',
                  title="Максимальное количество убийств за час без смертей")