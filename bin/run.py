import shutil  
import os  

def convert_shtml(filename):
    separator = ";"
    header = """
    <table id='passportoffices'>
        <thead>
            <tr>
                <th scope="col"><b>Facility</b></th>
                <th scope="col"><b>Address</b></th>
                <th scope="col"><b>City</b></th>
                <th scope="col"><b>State</b></th>
                <th scope="col"><b>ZIP</b></th>
                <th scope="col"><b>Phone</b></th>
            </tr>
        </thead>
    <tbody>
    """
    
    footer = """
    </tbody>
    </table>
    """

    body = ""
    
    with open(filename) as f:
        lines = f.readlines()
        for line in lines[1:]:
            body += """
            <tr>
                <td>"$i"</td>
            </tr>
            """

    with open(f'../shtmls/{filename}') as f:
        f.write(header)
        f.write(body)
        f.write(footer)

def convert_shtmls():
    for _, _, f in os.walk("../data"):
        convert_shtml(f)

def merge_csv():
    with open("../data/facilities_all.csv") as w:
        for _, _, f in os.walk("../data"):
            if f != output:
                lines = f.readlines()
                w.writelines(lines[1 if first else 0:])

def run_spiders():
    scrapy runspider ../bestppscraper/spiders/states_spider.py -o ../states.csv
    with open('../states.csv') as f:
        for line in f.readlines():
            scrapy runspider -a state="${line::${#line}-1}" ../bestppscraper/spiders/facilities_spider.py -o ../data/facilities/${line::${#line}-1}.csv

def email_shtmls():
    #email shtml.zip through AWS

def run():
    run_spiders()
    merge_csv()
    convert_shtmls()
    #zip -r shtmls.zip ../shtmls

if __name__ == "__main__":
    data_folder = '../data'
    shtmls_folder = '../shtmls'
    os.mkdir(data_folder)
    os.mkdir(shtmls_folder)
    run()
    shutil.rmtree(shtmls_folder)
    shutil.rmtree(data_folder)
    email_shtmls()