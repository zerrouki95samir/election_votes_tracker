import dash

app = dash.Dash(
    __name__,
    external_stylesheets=[
        #'https://codepen.io/chriddyp/pen/bWLwgP.css',
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css',
        'https://cdnjs.cloudflare.com/ajax/libs/magnific-popup.js/1.0.0/magnific-popup.min.css',
        'https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css',
        'https://www.w3schools.com/w3css/4/w3.css',
    ],
    external_scripts=[
        'https://code.jquery.com/jquery-3.3.1.slim.min.js',
        'https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/magnific-popup.js/1.0.0/jquery.magnific-popup.min.js'
    ],
    update_title=None,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    suppress_callback_exceptions=True, 
    title='TFN', 
)


server = app.server