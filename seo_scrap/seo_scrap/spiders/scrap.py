from re import T
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            # "https://quotes.toscrape.com/page/1/",
            # "https://quotes.toscrape.com/page/2/",
            "https://www.prisma.io/docs/reference/api-reference/command-reference"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page_architecture = yield self.parse_page_architecture(response)
        print(page_architecture)
        # self.print_tree(page_architecture)

        yield {
            "title": response.xpath("//title/text()").get(),
            "meta_description": response.xpath(
                "//meta[@name='description']/@content"
            ).get(),
            "meta_keywords": response.xpath("//meta[@name='keywords']/@content").get(),
            "url": response.request.url,
        }
        # for quote in response.css("div.quote"):
        #     yield {
        #         "text": quote.css("span.text::text").get(),
        #         "author": quote.css("small.author::text").get(),
        #         "tags": quote.css("div.tags a.tag::text").getall(),
        #     }

    def parse_page_architecture(self, response):
        TreeNode = [] # liste de TreeNode

        h1s = response.xpath('//h1')
        # root = TreeNode("empty", "h0", [])
        # self.recurse_tree(h1s, root, 1)
        # return root
        return None
    
    def recurse_tree(self, list_of_h, node, layer):
        if list_of_h == [] or list_of_h == None:
            print("=====: " + list_of_h)
            return

        for h in list_of_h:
            text = h.xpath('.//text()').get()
            hnode = TreeNode(text, "h" + str(layer))

            hnexts = h.xpath('.//h' + str(layer + 1))
            node.children += hnode
            self.recurse_tree(hnexts, hnode, layer + 1)
    
    def print_tree(self, node):
        print(node.layer + " : " + node.key)
        for child in node.children:
            self.print_tree(child)


    # def parse(self, response):
    #     page = response.url.split("/")[-2]
    #     filename = f"quotes-{page}.html"
    #     with open(filename, "wb") as f:
    #         f.write(response.body)
    #     self.log(f"Saved file {filename}")

    #     for quote in response.css("div.quote"):
    #         yield {
    #             "text": quote.css("span.text::text").get(),
    #             "author": quote.css("small.author::text").get(),
    #             "tags": quote.css("div.tags a.tag::text").getall(),
    #         }

class TreeNode:
    def __init__(self, key, layer):
        self.key = key
        self.layer = layer
        self.children = []
