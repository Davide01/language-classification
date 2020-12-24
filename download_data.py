import os
import wikipediaapi as wikiapi
import click


DATA_DIR = os.path.join("app", "lang_model", "data")


class WikiDataDownloader:
    def __init__(self, country: str, topic: str):
        self.country = country
        self.topic = topic
        self.wiki = wikiapi.Wikipedia(country)
        self.__set_folder(country=country)

    def __set_folder(self, country: str):
        self.folder_path = os.path.join(DATA_DIR, country)
        os.makedirs(self.folder_path, exist_ok=True)

    def _download_for_country(self, categorymembers, level=0, max_level=1):
        for c in categorymembers.values():
            if c.ns == wikiapi.Namespace.CATEGORY and level < max_level:
                self._download_for_country(
                    c.categorymembers, level=level + 1, max_level=max_level
                )
            self._download_and_save(c.title)

    def _download_and_save(self, title):
        page = self.wiki.page(title)
        path = os.path.join(self.folder_path, f"{title.replace('/', '')}.txt")
        if os.path.exists(path):
            return
        try:
            with open(path, "w") as file:
                print(title)
                file.write(page.text)
        except OSError as e:
            print(f"Error downloading {title}. {e.args}")

    def download(self):
        cat = self.wiki.page(f"Category:{self.topic}")
        print(f"Category members: Category:{self.topic}")

        self._download_for_country(cat.categorymembers)


@click.command()
@click.option("-c", "--country", type=str, prompt="Enter country code (da/sv/no)")
@click.option("-t", "--topic", type=str, prompt="Enter topic title")
def main(country: str, topic: str):
    downloader = WikiDataDownloader(country=country, topic=topic)
    downloader.download()


if __name__ == "__main__":
    main()
