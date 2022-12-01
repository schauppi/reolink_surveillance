class CreateStreamingUrl():

    def create_streaming_url(username: str, 
                            password: str, 
                            ip: str) -> str:

        url = "rtsp://{}:{}@{}".format(username, password, ip)
        return url