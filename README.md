# JARKOM-TCP-HTTP
a simple 1 threaded tcp http server

## Usage
- change the config in the `config.py`

```py
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

```

- NOTE : edit the part when it says `# -- START -- #` and ended at `# -- END -- #`
- after done configuring run `./serve.py`
