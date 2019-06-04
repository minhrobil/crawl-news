# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

class QuotesSpider(scrapy.Spider):
    name = "scraper_vnexpress"
    # Đây là tên của spider, khi chạy sẽ gọi cái tên này thì nó crawl file này. câu lệnh chạy tương ứng là: scrapy crawl scraper_vnexpress
    def start_requests(self):
        # hàm start_requests là hàm khởi tạo. Ở đây định nghĩa các url và sẽ bắt đầu crawl từ các url này.
        url = "https://vnexpress.net/the-thao/liverpool-vo-dich-champions-league-3932365-tong-thuat.html"
        # url là link của trang web cần crawl. Nếu muốn nhiều hơn 1 thì đặt url trong mảng là được
        yield Request(url, self.save_data)
        # yield Request. Đây là cú pháp thực hiện việc gọi đến url được truyền vào rồi gửi kết quả thu được là response đến hàm save_data.

    def save_data(self, response): 
        item = {}
        # khởi tạo ra 1 object rỗng để sau sẽ lưu thông tin vào object này
        title = response.css('h1.title_news_detail::text').get()
        # cú pháp bóc tách thông tin bằng css. 
        # chạy từng thẻ, từ thẻ cha cho đến thẻ con. Viết thẻ cha trước con sau và phân tách bởi dấu cách.
        # h1.title_news_detail chính là thẻ <h1 class="title_news_detail">Đây là title</h1>.
        # response.css('h1.title_news_detail::title.get() sẽ thu được phần text bên trong thẻ = "Đây là title" của thẻ <h1 class="title_news_detail">Đây là title</h1>.
        # get() sẽ lấy ra cái đầu tiên nó tìm được, getall() sẽ trả về mảng tất cả những cái nó tìm được

        description = response.xpath('//*[@class="description"]/text()').extract()[0]
        # cú pháp bóc tách thông tin bằng xpath
        # cũng chạy từng thẻ từ cha đến con, phân tách nhau bởi dấu "/"
        # cú pháp này luôn có 2 dấu "//" ở đầu, sau đó bắt đầu là phần định nghĩa các thẻ.
        # trong cú pháp trên, response.xpath('//*[@class="description"]/text()').extract()[0] sẽ được hiểu như sau:
        # *[@class="description"]: bắt tất cả các thẻ có class="description". Đằng sau "@" chính là các attribute của thẻ. có thể có style, href,...
        # /text(): trong các thẻ đó lấy phần text. 
        # extract()[0]: mặc định extract() trả về một mảng, lấy [0] để lấy phần tử đầu tiên. Có thể dùng extract_first() thay thế

# LƯU Ý: KHÔNG NHẤT THIẾT PHẢI ĐI LẦN LƯỢT TỪ THẺ TO NHẤT ĐẾN THẺ CẦN TÌM. NẾU THẺ CẦN TÌM CÓ "class" DUY NHẤT THÌ CHỈ CẦN GỌI THẲNG VÀO THẺ ĐÓ LÀ ĐƯỢC

        content = ' '.join(response.css('p.Normal::text').getall())

        # cú pháp trên sẽ lấy text của tất cả thẻ <p class="Normal"></p> sau đó trả về một mảng
        # ' '.join() có tác dụng nối từng phần tử của mảng thông qua dấu cách ' '

        time = response.css('header.clearfix span.time::text').get()
        # cú pháp trên sẽ được thực thi như sau:
        # Tìm thẻ <header class="clearfix"></header> trả về danh sách các thẻ con của nó
        # Tiếp tục tìm thẻ <span class="time">...</span> trả về phần text trong thẻ span đó

        author = response.xpath('//p[@class="Normal"]/strong/text()').extract()[-1]
        # p[@class="Normal"]: Tìm tất cả các thẻ <p></p> có class="Normal"
        # /strong/text(): Tìm tiếp các thẻ <strong></strong> trong đó và lấy text trong thẻ <strong></strong>
        # extract()[-1]: kết quả trả về là mảng, cho nên sẽ lấy kết quả cuối cùng. Vì cái cuối cùng sẽ là cái tác giả ở dưới cùng của bài viết :))
        
        # tiếp theo sẽ update các thông tin thu được vào trong object item
        item.update({
            "url":response.url, 
            # response.url sẽ trả về đường dẫn của trang đang làm việc, chính là cái url ở hàm start_requests
            "title":title,
            "description":description,
            "content":content,
            "time":time,
            "author":author
        })
        yield item
        # cú pháp yield item để ghi lại item vừa tạo

