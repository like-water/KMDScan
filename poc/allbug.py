from kmdpoc.base_poc import BasePOC


class Poc(BasePOC):
    def verify(self):
        return False


if __name__ == "__main__":
    print Poc("http://alopex.apitops.com").execute()
