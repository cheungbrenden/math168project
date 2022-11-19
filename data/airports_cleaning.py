import pandas as pd

airport = pd.read_csv("airports.dat", index_col=0, header=None)
airport = airport[airport[3] == "United States"]
airport = airport[airport[4] != "\\N"][[4, 6, 7]]
airport.columns = ["airport", "latitude", "logitude"]
airport.set_index("airport").to_csv("data/airports_us.csv")