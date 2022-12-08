from handler.credention_handler import CredentionHandler
from handler.streaming_url_handler import CreateStreamingUrl

from streaming.client_handler import Client


def start_clients(jetson_ips):

    for ip in jetson_ips:
        Client.start(ip)


def main(jetson_ips):

    start_clients(jetson_ips)


if __name__ == "__main__":

    jetson_ips = ["192.168.50.210"]

    main(jetson_ips)



