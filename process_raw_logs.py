import pandas as pd


def parse_content(content: str) -> dict:
    try:
        last_close_bracket = content.rindex(')')
        last_open_bracket = content.rindex('(')
        content_in_brackets = content[last_open_bracket + 1:last_close_bracket]
        weapon = content_in_brackets.split(',')[0]
        distance = float(content_in_brackets.split(', ')[1].split('m')[0])

        killer = content[:last_open_bracket].split(" убил ")[0]
        victim = content[:last_open_bracket - 1].split(" убил ")[1]
        return {"оружие": weapon, "расстояние": distance, "имя игрока": killer, "жертва": victim}
    except:
        print(content)
        return {"оружие": None, "расстояние": None, "имя игрока": None, "жертва": None}


def process_raw_log(source_log_path, destination_path):
    source_df = pd.read_csv(source_log_path)
    source_df = source_df[source_df.Author == "Integration"]
    source_df.Date = pd.to_datetime(source_df['Date'], format='%m/%d/%Y %I:%M %p')

    result_df = source_df[source_df.Date > pd.to_datetime("2023-11-07 15:00:00")][["Date", "Content"]]

    # Apply the function to the DataFrame and add returned dict values as new columns
    new_columns = result_df['Content'].apply(lambda x: pd.Series(parse_content(x)))
    result_df = pd.concat([result_df, new_columns], axis=1)
    result_df.dropna()

    result_df.to_csv(destination_path, index=False)


process_raw_log("__raw_data/GROZA DAYZ - Основная информация - 💣killfeed-livonia [1135206174980050965] (after 2023-11-05).csv",
                "data/livonia.csv")


process_raw_log("__raw_data/GROZA DAYZ - Основная информация - 💣killfeed-cherno-1 [1066788171632889886] (after 2023-11-05).csv",
                "data/chernarus_1.csv")


process_raw_log("__raw_data/GROZA DAYZ - Основная информация - 💣killfeed-cherno-2 [1070609632680235038] (after 2023-11-05).csv",
                "data/chernarus_2.csv")


process_raw_log("__raw_data/GROZA DAYZ - Основная информация - 💣killfeed-cherno-3 [1124684878445817889] (after 2023-11-05).csv",
                "data/chernarus_3.csv")


process_raw_log("__raw_data/GROZA DAYZ - Основная информация - 💣killfeed-cherno-5 [1173283269056397372] (after 2023-11-05).csv",
                "data/chernarus_5.csv")