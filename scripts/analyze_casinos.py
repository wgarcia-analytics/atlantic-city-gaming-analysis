import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)

df = pd.read_csv("data/clean/casino_monthly.csv")

df["group"] = df["unit"].replace({
    "Caesars": "Caesars Ent.",
    "Harrah's": "Caesars Ent.",
    "Tropicana": "Caesars Ent.",
    "Caesars Interactive NJ": "Caesars Ent.",
})
df["year"] = df["month"].str[:4]

annual = df.groupby(["year", "group"])[["floor_win", "online_win"]].sum()
annual["ratio"] = annual["online_win"] / annual["floor_win"]

table = annual["ratio"].unstack().round(2)
print(table)

import matplotlib.pyplot as plt

full_years = table.drop("2026")

online_first = full_years[["Golden Nugget", "Resorts", "Bally's"]]
floor_first = full_years[["Borgata", "Caesars Ent.", "Hard Rock", "Ocean Casino"]]

online_first.plot(figsize=(10, 6), linewidth=2)
plt.axhline(1, color=["#d62728", "#e377c2", "#1f77b4"], linestyle="--")
plt.title("Three casinos crossed the line: online now outearns their floors")
plt.ylabel("Online win ÷ floor win")
plt.tight_layout()
plt.savefig("charts/online_first.png", dpi=200)

floor_first.plot(figsize=(10, 6), linewidth=2,
                color=["#ff7f0e", "#2ca02c", "#9467bd", "#8c564b"])
plt.title("Four casinos are still floor-first. Ocean is the only one slipping")
plt.ylabel("Online win ÷ floor win")
plt.tight_layout()
plt.savefig("charts/floor_first.png", dpi=200)

print("Saved charts")