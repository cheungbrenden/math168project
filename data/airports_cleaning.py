import pandas as pd

airport = pd.read_csv("airports.dat", index_col=0, header=None)
airport = airport[(airport[3] == "United States") | (airport[3] == "Puerto Rico") | (airport[3] == "Virgin Islands")]
airport = airport[airport[4] != "\\N"][[4, 6, 7]]
airport.columns = ["airport", "latitude", "longitude"]
airport.set_index("airport").to_csv("airports_us.csv")