class Chainable():
    
    def __init__(self) -> None:
        self.nextLinks = []
        pass
    
    def chain(self, any):
        self.nextLinks.append(any)
        
    def unchain(self, any):
        self.nextLinks.append(any)
        
    def executeNext(self, function="init"):
        for link in self.nextLinks:
            try:
                method = getattr(link, function)
            except Exception as e:
                print(e)
                continue
            method()