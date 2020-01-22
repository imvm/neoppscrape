rm ../states.csv
rm ../data/facilities*

mkdir ../data

python3 -m scrapy runspider ../bestppscraper/spiders/states_spider.py -o ../states.csv


cat ../states.csv|tail -n +2|while read line
do
python3 -m scrapy runspider -a state="${line::${#line}-1}" ../bestppscraper/spiders/facilities_spider.py -o ../data/facilities${line::${#line}-1}.csv
done
