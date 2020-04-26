import logging

FORMAT = "* %(asctime)s - %(levelname)-8s * %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)
logging.getLogger("paramiko").setLevel(logging.WARNING)
