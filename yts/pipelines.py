from scrapy.exceptions import DropItem


class Rating(object):
    def process_item(self, item, spider):
        try:
            if float(item["criticts"][:-1]) < 60 and float(item["audience"][:-1]) < 80:
                item["criticts"] = "Not Recommended"
        except KeyError:
            pass
        if float(item["imdb_rating"]) < 6:
            item["imdb_rating"] = "Not Recommended"
        elif int(item["rating_count"]) < 10000:
            item["rating_count"] = "Not Recommended"
        return item


class CheckAsViable(object):
    def process_item(self, item, spider):
        try:
            if (
                item["criticts"] != "Not Recommended"
                and item["imdb_rating"] != "Not Recommended"
                and item["rating_count"] != "Not Recommended"
            ):
                print("\r\n Movie found ->")
                print("Movie Title: " + item["movie_title"])
                print("Release Year: " + item["release_year"])
                print("Genre: " + item["genre"])
                print("Magnet Link: " + item["magnet_link"])
            # 4
            else:
                raise DropItem()
        except KeyError:
            if (
                item["imdb_rating"] != "Not Recommended"
                and item["rating_count"] != "Not Recommended"
            ):
                print("\r\n Movie found ->")
                print("Movie Title: " + item["movie_title"])
                print("Release Year: " + item["release_year"])
                print("Genre: " + item["genre"])
                print("Magnet Link: " + item["magnet_link"])
            # 4
            else:
                raise DropItem()
        return item
