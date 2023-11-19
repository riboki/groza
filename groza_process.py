from functools import lru_cache

import pandas as pd

GROZA_SERVER_FILES = {"Чернарусь 1": "chernarus_1.csv",
                      "Чернарусь 2": "chernarus_2.csv",
                      "Чернарусь 3": "chernarus_3.csv",
                      "Чернорусь 5": "chernarus_5.csv",
                      "Ливония": "livonia.csv"}


@lru_cache(maxsize=None)
def get_wipe_data(server):
    df: pd.DataFrame = pd.read_csv(f"data/{GROZA_SERVER_FILES[server]}")
    df.Date = pd.to_datetime(df['Date'])

    return df


@lru_cache(maxsize=None)
def max_killer_within_hour(server, players: frozenset):
    wipe_data = get_wipe_data(server)
    wipe_data = wipe_data[wipe_data["имя игрока"].isin(players)]
    time_groups = wipe_data.set_index('Date').groupby(pd.Grouper(freq='60Min'))

    max_counts = {}
    for name, group in time_groups:
        filtered_group = group.apply(lambda row: row['жертва'] == row['имя игрока'], axis=1)
        if not group[~filtered_group].empty:
            counts = group[~filtered_group]['имя игрока'].value_counts()
            if not counts.empty:
                for player, count in counts.items():
                    if player in max_counts:
                        max_counts[player] = max(max_counts[player], count)
                    else:
                        max_counts[player] = count

    # Create DataFrame from the max_counts dictionary
    result_df = pd.DataFrame(list(max_counts.items()), columns=['имя игрока', 'Максимальное количество убийств'])

    result_df = result_df.sort_values(by='Максимальное количество убийств', ascending=False)
    return result_df


@lru_cache(maxsize=None)
def get_players(server, min_kills: int = 5) -> frozenset:
    kill_stats = get_kill_statistics(server)
    return frozenset(kill_stats[kill_stats > min_kills].index)


@lru_cache(maxsize=None)
def get_kill_statistics(server) -> pd.Series:
    return get_wipe_data(server)["имя игрока"].value_counts()


@lru_cache(maxsize=None)
def top_killers(server, top: int = 20) -> pd.Series:
    killers = get_kill_statistics(server).iloc[:top]
    return killers


@lru_cache(maxsize=None)
def get_kills(server, players: frozenset) -> pd.DataFrame:
    killers = get_wipe_data(server)["имя игрока"]
    player_kills = killers[killers.isin(players)].value_counts()
    player_kills = pd.DataFrame({"имя игрока": player_kills.index, "количество убийств": player_kills.values})
    player_kills = player_kills.sort_values(by="количество убийств", ascending=False)
    return player_kills


@lru_cache(maxsize=None)
def get_victims(server, players: frozenset) -> pd.DataFrame:
    victims = get_wipe_data(server)["жертва"]
    victims = victims[victims.isin(players)].value_counts()
    victims = pd.DataFrame({"имя игрока": victims.index, "количество смертей": victims.values})
    victims = victims.sort_values(by="количество смертей", ascending=False)
    return victims


@lru_cache(maxsize=None)
def get_kill_death_stats(server, players: frozenset) -> pd.DataFrame:
    killers = get_wipe_data(server=server)["имя игрока"]
    victims = get_wipe_data(server=server)["жертва"]
    player_kills = killers[killers.isin(players)].value_counts()
    player_victims = victims[victims.isin(players)].value_counts()
    victim_kills = pd.DataFrame(dict(kills=player_kills, victims=player_victims))
    victim_kills = victim_kills[victim_kills.victims > 0]
    kd = victim_kills.assign(kd=victim_kills.kills / victim_kills.victims)
    kd["имя игрока"] = kd.index
    kd = pd.DataFrame({"имя игрока": kd["имя игрока"], "Убийства/Cмерти": kd["kd"]})
    return kd.sort_values(by="Убийства/Cмерти", ascending=False)


@lru_cache(maxsize=None)
def distances_per_players(server, players: frozenset | None = None, quantile: float = 0.95):
    wipe_data = get_wipe_data(server)
    if not players:
        players = get_players(server=server)
    return wipe_data[wipe_data["имя игрока"].isin(players)
                     & (wipe_data["расстояние"] < 1_000)][
        ["имя игрока", "расстояние"]]


@lru_cache(maxsize=None)
def weapons_per_player(server, players: frozenset):
    killer_weapon = get_wipe_data(server)[["имя игрока", "оружие"]]
    killer_weapon = killer_weapon[killer_weapon["имя игрока"].isin(players)]
    unique_weapons_per_player = killer_weapon.groupby(by="имя игрока")["оружие"].nunique()
    unique_weapons_per_player = pd.DataFrame({"имя игрока": unique_weapons_per_player.index,
                                              "кол-во уникальных": unique_weapons_per_player.values}) \
        .sort_values(by="кол-во уникальных", ascending=False)
    return unique_weapons_per_player


@lru_cache(maxsize=None)
def favourite_weapon_per_player(server, players: frozenset):
    weapon_counts = get_wipe_data(server)[get_wipe_data(server)["имя игрока"].isin(players)]
    weapon_counts = weapon_counts.groupby(["имя игрока", "оружие"]).size().reset_index(name='count')

    # Finding the index of the maximum count for each "имя игрока"
    idx = weapon_counts.groupby("имя игрока")['count'].idxmax()

    # Getting the rows corresponding to the max counts for each killer
    favourite_weapon_df = weapon_counts.loc[idx].reset_index(drop=True)[["имя игрока", "оружие"]]

    favourite_weapon_df.columns = ["имя игрока", "любимое оружие"]
    return favourite_weapon_df


@lru_cache(maxsize=None)
def weapons_with_kills(server, top: int = 30, ascending: bool = False):
    weapon_kills = get_wipe_data(server)["оружие"].value_counts()
    weapon_kills = pd.DataFrame({"оружие": weapon_kills.index,
                                 "количество убийств": weapon_kills.values}) \
        .sort_values(by="количество убийств", ascending=ascending)
    return weapon_kills.iloc[:top]


@lru_cache(maxsize=None)
def num_unique_weapons(server, players: frozenset | None = None, quantile: float = 0.95):
    wipe_data = get_wipe_data(server)
    if not players:
        players = get_players(server)
    return wipe_data[wipe_data["имя игрока"].isin(players)
                     & (wipe_data["расстояние"] < wipe_data["расстояние"].quantile(quantile))][
        ["имя игрока", "расстояние"]]
