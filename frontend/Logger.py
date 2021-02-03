import logging

def blogger(m):
    logging.basicConfig(level=logging.INFO, filename='logs.log', format='%(asctime)s %(levelname)s:%(message)s')
    logging.info(m)
            