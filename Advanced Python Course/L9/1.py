import asyncio
import json
from aiohttp import ClientSession
from matplotlib import pyplot as plt

gbp21_url = "http://api.nbp.pl/api/exchangerates/rates/a/gbp/2021-01-01/2021-12-31/?format=json"
gbp22_url = "http://api.nbp.pl/api/exchangerates/rates/a/gbp/2022-01-01/2022-12-31/?format=json"
usd21_url = "http://api.nbp.pl/api/exchangerates/rates/a/usd/2021-01-01/2021-12-31/?format=json"
usd22_url = "http://api.nbp.pl/api/exchangerates/rates/a/usd/2022-01-01/2022-12-31/?format=json"

async def collectData(url, session, headers=None):
    async with session.get(url, headers=headers) as response:
        return await response.text()

async def getData(session, url):
    return await collectData(url, session, None)

def calculateMean(dates, values):
    new_values = []
    new_args = []
    i = 0
    while i < len(dates):
        current_month = int(dates[i][5:7])
        sum_val = 0
        days = 0
        while int(dates[i][5:7]) == current_month:
            days += 1
            sum_val += values[i]
            i += 1
            if i >= len(dates):
                break
        new_values.append(sum_val / days)
        new_args.append(dates[i - 1][0:7])

    return (new_args, new_values)

async def getPair(url):
    async with ClientSession() as session:
        d = await getData(session, url)
        dataJson = json.loads(d)
        rates = dataJson.get('rates', [])
        values = [rate.get('mid') for rate in rates]
        dates = [rate.get('effectiveDate') for rate in rates]
        new = calculateMean(dates, values)
    return new

def guess(year1, year2):
    forecast = []
    date = []
    for i in range(12):
        change = (year1[i] - year2[i]) / year2[i]
        forecast.append((1 + change) * year1[i])
        date.append(f"2023-{i + 1}")
    return (date, forecast)

async def main():
    gbp1 = await getPair(gbp21_url)
    gbp2 = await getPair(gbp22_url)
    usd1 = await getPair(usd21_url)
    usd2 = await getPair(usd22_url)

    f1 = guess(gbp2[1], gbp1[1])
    f2 = guess(usd2[1], usd1[1])

    plt.title("Wykres kursu GBP oraz USD w stosunku do PLN w latach 2021-2022 wraz z prognozą na przyszłość")

    plt.plot(gbp1[0] + gbp2[0] + f1[0], gbp1[1] + gbp2[1] + f1[1], color='#bc5090', label='GBP')
    plt.plot(usd1[0] + usd2[0] + f2[0], usd1[1] + usd2[1] + f2[1], color='#58508d', label='USD')
    
    plt.axvline(x=len(gbp1[0] + gbp2[0]), color='red', linestyle='--')

    plt.ylabel('Wartość [PLN]')
    plt.xlabel('Czas')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    asyncio.run(main())
