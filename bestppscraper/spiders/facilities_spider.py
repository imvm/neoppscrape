import re
import scrapy
from bs4 import BeautifulSoup

HEADERS = {
    'X-MicrosoftAjax': 'Delta=true',
    'User-Agent': 'Ian Manor - imvm@cin.ufpe.br'
}

class FacilityItem(scrapy.Item):
    facilityName = scrapy.Field()
    streetAdress = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zipCode = scrapy.Field()
    publicPhone = scrapy.Field()

class StateSpider(scrapy.Spider):
    name = 'facilities'
    start_urls = ['https://iafdb.travel.state.gov/DefaultForm.aspx']
    custom_settings = {
        'FEED_FORMAT':'csv',
        'FEED_EXPORT_FIELDS':['facilityName','streetAdress','city','state','zipCode','publicPhone']
    }

    def __init__(self, state="", *args, **kwargs):
        super(StateSpider, self).__init__(*args, **kwargs)
        self.state = state
        print(self.state)

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
        data = {}

        data['__VIEWSTATE'] = response.css('input#__VIEWSTATE::attr(value)').extract_first()
        data['__EVENTVALIDATION'] = response.css('input#__EVENTVALIDATION::attr(value)').extract_first()
        data['__VIEWSTATEGENERATOR'] = response.css('input#__VIEWSTATEGENERATOR::attr(value)').extract_first()

        data['__EVENTTARGET'] = ''
        data['ddnState'] = self.state
        data['btnSearch'] = 'Search'

        request = scrapy.FormRequest.from_response(
            response,
            headers = HEADERS,
            dont_filter = True,
            formdata=data,
            callback=self.parse_results
        )
        yield request

    def parse_results(self, response):
        last_page = True

        soup = BeautifulSoup(response.body_as_unicode(), 'html.parser')
        table = soup.find("table", {"class" : "ResultsDataGrid"})

        if not table is None:
            rows = table.findAll('tr')
            for row in rows[2:len(rows)-1]:
                cols = row.findAll('td')
                facility = FacilityItem()
                facility['facilityName'] = cols[0].string
                facility['streetAdress'] = cols[1].string
                facility['city'] = cols[2].string
                facility['state'] = cols[3].string
                facility['zipCode'] = cols[4].string
                facility['publicPhone'] = cols[5].string
                yield facility


            firstRow = rows[0]
            firstRowLinks = firstRow.findAll('a')
            for link in firstRowLinks:
                if link.string == '   Next 20':
                    last_page = False

            if not last_page:
                data = {}

                data['__VIEWSTATE'] = response.css('input#__VIEWSTATE::attr(value)').extract_first()
                data['__EVENTVALIDATION'] = response.css('input#__EVENTVALIDATION::attr(value)').extract_first()
                data['__VIEWSTATEGENERATOR'] = response.css('input#__VIEWSTATEGENERATOR::attr(value)').extract_first()
                data['__EVENTTARGET'] = 'dgFacilityList$ctl01$ctl01'
                data['btnSearch'] = 'Search'

                request = scrapy.FormRequest.from_response(
                    response,
                    headers = HEADERS,
                    dont_filter = True,
                    formdata=data,
                    callback=self.parse_results
                )
                yield request
        #else:
            #print(table)
