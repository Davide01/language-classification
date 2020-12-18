import os
import wikipediaapi as wikiapi

class DataDownloader:
    def __init__(self, countries, titles):
        self.countries = countries
        self.titles = titles

    def download_for_country(categorymembers, country, level=0, max_level=1):
        print(len(categorymembers.values()))
        for c in categorymembers.values():
            print("%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns))
            if c.ns == wikiapi.Namespace.CATEGORY and level < max_level:
                download_for_country(c.categorymembers, country, level=level + 1, max_level=max_level)
            download_and_save(c.title, country)
                
    def download_and_save(title, folder):
        page = wiki_wiki.page(title)
        path = os.path.join(folder, f"{title.strip('/')}.txt")
        if os.path.exists(path):
            return
        with open(path, 'w') as file:
            file.write(page.text)