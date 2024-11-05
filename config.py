# CONFIG FOR THE SEREVE.PY #

class Config:
    port: int
    web_path: str
    private_file: list
    fof_html: str
    fot_html: str
    
    def __init__(self, port, web_path, private_file, fof_html, fot_html) -> None:
        self.port = port
        self.web_path = web_path
        self.private_file = private_file
        self.fof_html = fof_html
        self.fot_html = fot_html

def get_config():
    return serveConfig

# -- START -- #

serveConfig = Config(

    # port to host
    port= 8082,

    # folder to host
    web_path='web',

    # private file will be forbidden if opened
    private_file=['404.html', '403.html'],

    # path to 404 not found html
    fof_html = '404.html',

    # path to 403 forbidden html
    fot_html = '403.html'
)
# -- END -- #
