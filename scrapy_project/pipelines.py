import psycopg2
from .items import TenderItem
from scrapy.exceptions import DropItem


class TenderPipeline(object):
    """Save extracted data to database"""

    def open_spider(self, spider):
        # Connect to database
        try:    
            hostname = 'localhost'
            username = 'postgres'
            password = '1'
            database = 'tender_monitor_db'
            self.connection = psycopg2.connect(
                                        host=hostname,
                                        user=username, 
                                        password=password, 
                                        dbname=database)
            if self.connection:
                self.cur = self.connection.cursor()
                spider.log(f'Connection to database "{database}" is OK!')
            else:
                spider.log('Error! Cursor not found!')
        except Exception as ex:
            print(ex)


    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()


    def process_item(self, item, spider):
        """ Checks and saves data to connected DB
            Note: item.save()  works ONLY with Django item and Djangomodels
            Use INSERT INTO
        """
 
        spider.log('Check if item already exists in db...')
        # v1
        self.cur.execute("select exists(\
                          SELECT number FROM public.tenders\
                          WHERE lower(number) = %s)", 
                          (item["number"].lower(),)   
                        )


        item_exists = self.cur.fetchone()  

        if item_exists[0] == True:
            raise DropItem('Tender already exists and won\'t be added to db')

        # # v2 if there is tender with the same number in db count() 
        # will be True
        # if Tender.objects.filter(number__iexact=item['number']).count():
        #     raise DropItem('Tender already exists and won\'t be added to db')


        else:
            spider.log('Item will be added to db.')
                       
            try:
                self.cur.execute("INSERT INTO public.tenders \
                                 (number, customer, description, price, country, url_addr, deadline, created_at, updated_at) \
                                  VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);",
                                 (item['number'],
                                  item['customer'],
                                  item['description'],
                                  item['price'],
                                  item['country'],
                                  item['url_addr'],
                                  item['deadline'])
                                  )
                spider.log('Item added to db. OK!')
            
            except Exception as ex:
                # Return back if is there a problem with saving
                self.cur.execute("rollback")
                spider.log('Something went wrong!\
                            Error by saving to db: %s' % ex)
                
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

        self.connection.commit()
        return item

# class TenderPipeline(object):
#     """Save extracted data to database"""

#     def open_spider(self, spider):
#         # Connect to database
#         hostname = 'localhost'
#         username = 'postgres'
#         password = '1'
#         database = 'tender_monitor_db'
#         self.connection = psycopg2.connect(
#                                     host=hostname,
#                                     user=username, 
#                                     password=password, 
#                                     dbname=database)
#         if self.connection:
#             self.cur = self.connection.cursor()
#             spider.log('**** Well, connection to database is OK! %s' % self.cur)
#             print('~~~~~~~~~~~~ Connection to database is OK! ~~~~~~~~~~')

#     def close_spider(self, spider):
#         self.cur.close()
#         self.connection.close()

#     def process_item(self, item, spider):
#         """ Check if tender already exists in database and 
#             if no exception save data to DB
#         """
#         spider.log('*** <TenderPipeline>: data is processed and saved to db')
        
#         try:
#             item.save()
        
#         except Exception as ex:
#             spider.log('Something went wrong!\
#                             Error by saving to db: %s' % ex)
#             raise DropItem('Probably tender <%s> already exists in db' % item['number'])
        
#         # tender_exists = self.cur.execute(
#         #     "SELECT number FROM public.tenders WHERE number = item['number'];")
#         # print('tender exist:', tender_exists)
#         # if bool(tender_exists):
#         #     raise DropItem('Tender already exists %s', item['number'])
        
#         # else:
#         #     # save item to database
#         #     item.save()

#         return item
