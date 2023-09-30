import scrapy


class GoldOneSpider(scrapy.Spider):
    name = 'goldone'
    start_urls = ['https://www.goldonecomputer.com/']

    def parse(self, response):
        # Step 1: Scrape all category links
        category_urls = response.xpath("//*[@class='box-content']/ul[@id='nav-one']/li/a/@href").getall()
        for category_url in category_urls:
            absolute_category_url = response.urljoin(category_url)
            yield  response.follow(absolute_category_url, self.parse_category)

    def parse_category(self, response):
        # Extract category information here if needed
        # ...

        # Step 2: Extract product links in the category
        product_urls = response.xpath("//*[@class='caption']/h4/a/@href").getall()
        for product_url in product_urls:
            absolute_product_url=response.urljoin(product_url)
            yield scrapy.Request(absolute_product_url, callback=self.parse_product)

    def parse_product(self, response):
        # Step 4: Scrape product details
        code = response.xpath("//ul[@class='list-unstyled']/li/text()").get()
        title = response.xpath("//*/h3[@class='product-title']/text()").get()
        brand = response.xpath("//ul[@class='list-unstyled']/li/a/text()").extract_first()
        price = response.xpath("//ul[@class='list-unstyled price']/li/h3/text()").get()
        review_count = response.xpath("//div[@class='rating-wrapper']/a[@class='review-count']/text()").get()
        image_url = response.xpath('//*[@id="tmzoom"]/@src').get()

        yield {
            'code': code,
            'title': title,
            'brand': brand,
            'price': price,
            'review_count': review_count,
            'image_url': image_url
        }