import scrapy

HEADERS = {
    'X-MicrosoftAjax': 'Delta=true',
    'User-Agent': 'Ian Manor - imvm@cin.ufpe.br'
}

class OptionItem(scrapy.Item):
    value = scrapy.Field()

class HostSpider(scrapy.Spider):
    name = 'states'
    start_urls = ['https://iafdb.travel.state.gov/DefaultForm.aspx']

    def parse(self, response):
        data = {}

        data['__VIEWSTATE'] = response.css('input#__VIEWSTATE::attr(value)').extract_first()
        data['__EVENTVALIDATION'] = response.css('input#__EVENTVALIDATION::attr(value)').extract_first()
        data['__VIEWSTATEGENERATOR'] = response.css('input#__VIEWSTATEGENERATOR::attr(value)').extract_first()
        data['__EVENTTARGET'] = 'rdoStateCity'
        data['grpSearchBy'] = 'rdoStateCity'

        return scrapy.FormRequest.from_response(
            response,
            formdata = data,
            headers = HEADERS,
            dont_filter = True,
            clickdata = {'id': 'rdoStateCity'},
            callback = self.parse_states
        )

    def parse_states(self, response):
        for ddnState in response.css('select#ddnState > option:not(:first-child) ::attr(value)').extract():
            option = OptionItem()
            option['value'] = ddnState
            yield option
