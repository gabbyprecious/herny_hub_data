from bs4 import BeautifulSoup
import requests
from utils import get_weekdays, get_monthlist, generate_dates
from datetime import timedelta
import csv, sys, warnings

class HenryHubData():
    def __init__(self,data="d"):
        options = ["d","m"]
        if data.lower() in options:
            url = "https://www.eia.gov/dnav/ng/hist/rngwhhd{}.htm".format(data.upper())
            response = requests.get(url)
            soup = BeautifulSoup(response.text, features="lxml")
            func = {
                "d":self.get_daily_data,
                "m":self.get_monthly_data
            }
            func[data.lower()](soup)
        else:
            warnings.warn("Not a valid argument")

    def get_daily_data(self, soup):
        dates = []
        prices = self.get_prices(soup)

        table_dates = soup.find_all("td", class_="B6")
        for table_date in table_dates:
            start, _ = generate_dates(table_date.text)
            end = start + timedelta(days=4)
            dates.extend(list(get_weekdays(start, end)))
        
        data = zip(dates, prices)

        self.create_csv(data, "daily_data.csv")

    def get_monthly_data(self, soup):
        dates = []
        prices = self.get_prices(soup)

        table_prices = soup.find_all("td", class_="B3") 
        for price in table_prices:
            final_price = price.text if price.text != "" else 0
            prices.append(final_price)

        dates.extend(list(get_monthlist()))

        data = zip(dates, prices)

        self.create_csv(data, "monthly.csv")
    
    def create_csv(self, data, file_path):
        with open(file_path, "w") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow(["Dates", "Prices"])
            for result in data:
                writer.writerow(result)
    
    def get_prices(self, soup):
        prices = []
        table_prices = soup.find_all("td", class_="B3") 
        for price in table_prices:
            final_price = price.text if price.text != "" else 0
            prices.append(final_price)
        return prices

if __name__ == "__main__":
    try:
        runner = HenryHubData(sys.argv[1])
    except IndexError:
        runner = HenryHubData()
    
        