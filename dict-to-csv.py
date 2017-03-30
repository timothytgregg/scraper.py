import ast
import csv
import datetime

write_file = 'org.contact.'+datetime.datetime.utcnow().isoformat()+'.csv'

print('the write file is : ' + write_file)

with open('retrieved.data.log.2017-03-30T15:47:46.452857.txt','r') as f:
  data=ast.literal_eval(f.read())

  with open(write_file, 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in data.items():
       #writer.writerow([key, value['email'], value['website'], value['phone']])
       writer.writerow([unicode(key).encode("utf-8"), unicode(value['email']).encode("utf-8"), unicode(value['website']).encode("utf-8"), unicode(value['phone']).encode("utf-8"), unicode(value['(english_org_name)']).encode("utf-8")])
  #for key, value in data.iteritems() :
    #print key, value
