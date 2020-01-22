import scrapy

class MyProjectCsvItemExporter(scrapy.exporters.CsvItemExporter):

    def __init__(self, *args, **kwargs):
        kwargs['delimiter'] = ';'

        super(MyProjectCsvItemExporter, self).__init__(*args, **kwargs)