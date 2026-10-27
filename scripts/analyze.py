import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/clean/gaming_revenue.csv")

print(df.shape)
print(df.head())
print(df.dtypes)

df["year"] = df["month"].str[:4]

annual = df.groupby("year")[["casino_win", "internet_win"]].sum()
annual["online_share"] = annual["internet_win"] / annual["casino_win"]
annual["months"] = df.groupby("year").size()

print(annual)

df["date"] = pd.to_datetime(df["month"])

plt.figure(figsize=(10, 5))
plt.plot(df["date"], df["casino_win"] / 1_000_000, label="Casino floor", color="#2a78d6", linewidth=2)
plt.plot(df["date"], df["internet_win"] / 1_000_000, label="Online", color="#eb6834", linewidth=2)

plt.title("Online gaming caught Atlantic City's casino floor")
plt.ylabel("Monthly win ($ millions)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("charts/online_vs_floor.png", dpi=200)
print("Saved chart")

covid = df[df["year"] == "2020"]
print(covid[["month", "casino_win", "internet_win"]])

df["floor_won"] = df["casino_win"] > df["internet_win"]

since_cross = df[df["month"] >= "2024-10"]
print(since_cross[["month", "casino_win", "internet_win", "floor_won"]])

wins = since_cross["floor_won"].sum()
print("Floor won", wins, "of", len(since_cross), "months since October 2024")