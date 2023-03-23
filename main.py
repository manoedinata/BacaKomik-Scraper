from bacakomikscraper import Scraper

scraper = Scraper()

# Search
scraper.search_comics("Conan")
print(scraper.search_result)

# Get comic info
scraper.get_comic_info("detective-conan")
print(scraper.comic_info)

# List chapters
print(scraper.comic_eps)

# List images of a chapter
scraper.get_ep_images("detective-conan-chapter-002-bahasa-indonesia")
print(scraper.comic_images)
