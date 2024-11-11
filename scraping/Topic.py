class Topic:
    name = str
    urls = []
    hashtags = []
    
# list of hashtags related to topic
    def __init__(self, name_, urls_, hashtags_):
        self.name = name_
        self.urls = urls_
        self.hashtags = hashtags_


        