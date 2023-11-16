from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField, validators


class HomeFrm(FlaskForm):
    req_val_msg = 'Please fill the {} field!'
    url_val_msg = 'Please enter a valid URL!'
    long_url = URLField(label='URL',
                        validators=[validators.DataRequired(message=req_val_msg.format('URL')),
                                    validators.url(message=url_val_msg)])
    submit = SubmitField()
