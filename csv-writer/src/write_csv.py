import csv
import sys
from time import strftime
from faker import Faker
from datetime import datetime
import random

#Usage python3 write_csv <number of files to generate> <number of rows in each file> <base file name>


fake = Faker()
number_of_files = int(sys.argv[1])
number_of_records = int(sys.argv[2])
base_file_name = sys.argv[3]

Faker.seed(0)
random.seed(0)

start_date_range = datetime(2023, 5, 1)
end_date_range = datetime(2023, 5, 31)

for i in range(number_of_files):
  with open(base_file_name + '_' + str(i) + '.csv', mode='w') as customer_file:
    csv_writer = csv.writer(customer_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    header_row = ['customer_id', 'first_name', 'last_name', 'email_address', 'phone_number', 'credit_card_number', 'credit_card_type', 'street_address', 'city', 'zip_code', 'date_loaded']
    #fake.numerify("@#")
    #customer_number = fake.bothify(text='????####', letters='ABCDE')

    #csv_writer.writerow(header_row)

    for j in range(number_of_records):
      customer_id = str(fake.numerify('##')) + '-' + str(fake.unique.random_int(min=1000000, max=9999999))
      first_name = fake.first_name()
      last_name = fake.last_name()
      email_address = first_name + "." + last_name + '@' + fake.domain_name()
      csv_writer.writerow([customer_id, first_name, last_name, email_address, 
      fake.phone_number(), fake.credit_card_number(card_type='visa'), 'visa', fake.street_address(), fake.city(), fake.zipcode(),  
      fake.date_between(start_date_range, end_date_range).strftime('%Y/%m/%d')])