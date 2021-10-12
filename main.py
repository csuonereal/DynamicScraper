from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd
import csv
import sys
import json
import os


class DynamicScrapper:
    def __init__(self, config_path):
        self.data = DynamicScrapper.load_config_file(config_path)
        self.parent_XPATH = self.data["parent"]
        self.childs_XPATHS = self.data["childs"]
        self.driver_path = self.data["driver_path"]
        self.url = self.data["web_url"]

    @staticmethod
    def load_config_file(path):
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        else:
            raise Exception("config file not found!")

    def set_driver(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(
            executable_path=self.driver_path, options=options)

    def run(self):
        self.set_driver()
        self.driver.get(self.url)

        row = []
        parents = self.driver.find_elements_by_xpath(self.parent_XPATH)
        for parent in parents:
            for i in range(0, len(self.childs_XPATHS)):
                obj = parent.find_element_by_xpath(self.childs_XPATHS[i]).text
                m = {f"{i+1}": obj}
                row.append(m)
        self.convert_json(self.reformatter(row))
        self.driver.close()
        self.driver.quit()

    def reformatter(self, row):
        print(row)
        r_row = []
        counter = 1
        values = []
        for i in row:
            if counter < len(self.childs_XPATHS):
                values.append(i[str(counter)])
                counter += 1
            else:
                values.append(i[str(counter)])
                counter = 1
                m = {}
                keys = range(0, len(self.childs_XPATHS))
                values_ = values
                for j in keys:
                    m[j+1] = values_[j]
                r_row.append(m)
                values = []
        return r_row

    def convert_csv(self, row):
        df = pd.DataFrame(row)
        df.to_csv("data4.csv", index=False)

    def convert_json(self, row):
        with open("data2.json", "w", encoding="utf-8") as f:
            json.dump(row, f, ensure_ascii=False)


if __name__ == "__main__":
    obj = DynamicScrapper("imdb.json")
    obj.run()
