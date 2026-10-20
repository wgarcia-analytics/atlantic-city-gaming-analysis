import requests
import os
import time

months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

missing = []

for year in range(2017, 2027):
    for month_number in range(1, 13):
        month = months[month_number - 1]
        filename = f"data/raw/{year}-{month_number:02d}.pdf"

        if os.path.exists(filename):
            print("Already have:", filename)
            continue

        patterns = [
            f"https://www.nj.gov/oag/ge/docs/Financials/PressRelease{year}/{month}{year}.pdf",
            f"https://www.nj.gov/oag/ge/docs/Financials/PressRel{year}/{month}{year}.pdf",
        ]

        found = False

        for url in patterns:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(response.content)
                print("Saved:", filename)
                found = True
                break

        if not found:
            print("MISSING:", year, month)
            missing.append(f"{year}-{month_number:02d}")

        time.sleep(1)

print("Done. Missing months:", missing)