import requests
from bs4 import BeautifulSoup
import pandas


def get_dict(address, btc):
    mylist = [i.text for i in adds[1 : len(adds)]]
    data = {
        "receivers": mylist,
        adds[0].text: [i["data-value"] for i in money[1 : len(money)]],
    }
    return data


if __name__ == "__main__":

    url = "https://learnmeabitcoin.com/explorer/block/00000000000000000001664977c4571466eeebb18533e843c5e9d424bd20a2df"
    html = requests.get(url).content
    soup = BeautifulSoup(html, "lxml")
    urls = [link.get("href") for link in links]
    cleaned_urls = [
        url[9:]
        for url in urls
        if "/transaction/" in url
        if len(url) > 25
        if len(url) <= 86
    ]

    link_start = "https://learnmeabitcoin.com/browser"

    ## loop through all tx urls to extract addresses involved in tx
    for i in range(len(cleaned_urls)):
        cleaned_link = link_start + cleaned_urls[i]
        html = requests.get(cleaned_link).content
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all("a")

        btc = soup.find_all("div", class_="value")
        adds = soup.find_all("a", class_="address")

        if len(adds) == 0 or len(btc) == 0:
            continue
        else:
            data = get_dict(adds, btc)

        if len(data["receivers"]) != len(data[adds[0].text]):
            continue
        else:
            data2 = pd.DataFrame(data)
            final_data = pd.concat([final_data, data2], sort=False)

    final_data_vstack = final_data.stack()
    final_data_vstack = final_data_vstack.reset_index()
    final_data_vstack.rename(
        columns={"": "target", "level_1": "source", 0: "btc"}, inplace=True
    )
    final_data1vstack_ = final_data_vstack.loc[final_data_vstack["btc"] != 0].copy()
