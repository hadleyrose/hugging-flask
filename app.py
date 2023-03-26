from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms.fields import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_bootstrap import Bootstrap5
from transformers import pipeline, set_seed

class LLM_Task_Form(FlaskForm):
    llm = SelectField('LLM', choices=[('distilbert', 'DistilBERT'), ('other', 'Other')])
    task = SelectField('Task', choices=[('fill', 'Fill Mask'), ('other', 'Other')])
    text = StringField('Text', validators=[DataRequired(), Length(1, 200)])
    submit = SubmitField()

app = Flask(__name__)
app.secret_key = 'dev'

# set default button sytle and size, will be overwritten by macro parameters
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
app.config['BOOTSTRAP_BTN_SIZE'] = 'sm'
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'lumen'

bootstrap = Bootstrap5(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LLM_Task_Form()
    output = None
    if form.is_submitted():
        if form.llm.data == 'distilbert':
            if form.task.data == 'fill':
                # set seed for reproducible results
                set_seed(10)
                # specify model checkpoint
                model_checkpoint = 'distilbert-base-uncased'
                unmasker = pipeline('fill-mask', model=model_checkpoint)
                output = unmasker(form.text.data)
    return render_template('index.html', form=form, result=output)
