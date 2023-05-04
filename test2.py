import logging
logging.basicConfig(format='%(asctime)s %(message)s', filename='example.log', encoding='utf-8', level = logging.INFO)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('Adds on? And this, too')
logging.error('And non-ASCII stuff, too, like Øresund and Malmö')