import scrapy
from scrapy.crawler import CrawlerProcess
class DC(scrapy.Spider):
    """The scraping class"""
    name="movies"
    def start_requests(self):
        """The start requests method that holds the url and processes it then send it to the parse method"""
        urls=["https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&genres=action",
        "https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&genres=adventure",
        "https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&genres=animation",
        "https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&genres=fantasy",
        "https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&genres=romance"]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)
    def parse(self,response):
        """The method that is used for subseting and scraping the websites into acceptable formats""" 
        movies=response.css("div.lister-item-content")
        for movie in movies:
            if int(movie.css("span.lister-item-year.text-muted.unbold::text").get().replace("(","").replace(")","").replace("I",""))>2005:
                items={
                    "title" :movie.css("h3.lister-item-header").css("a::text").get(),
                    "year":movie.css("span.lister-item-year.text-muted.unbold::text").get().replace("(","").replace(")","").replace("I",""),
                    "rating":movie.css("span.certificate::text").get(),
                    "duration":movie.css("span.runtime::text").get(),
                    "genre":movie.css("span.genre::text").get().strip(),
                    "Total vote rating":movie.css("div.inline-block.ratings-imdb-rating>strong::text").get(),
                    "Number of votes":movie.css("p.sort-num_votes-visible>span:nth-of-type(2)::text").get(),
                    "Director":movie.css("p:nth-of-type(3)>a:nth-of-type(1)::text").get()
                }
                yield items
            
if __name__=="__main__":
    process=CrawlerProcess()
    process.crawl(DC)
    process.start