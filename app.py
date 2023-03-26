from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms.fields import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_bootstrap import Bootstrap5
from transformers import pipeline, set_seed
from sentence_transformers import SentenceTransformer, util

class LLM_Task_Form(FlaskForm):
    llm = SelectField('LLM', choices=[('distilbert', 'DistilBERT'), ('gpt', 'GPT2')])
    task = SelectField('Task', choices=[('fill', 'Fill Mask'), ('gen', 'Text Generation')])
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
        elif form.llm.data == 'gpt':
            if form.task.data == 'gen':
                # set seed for reproducible results
                set_seed(10)
                # specify model checkpoint
                model_checkpoint = 'gpt2'
                generator = pipeline('text-generation', model=model_checkpoint)
                output = generator(form.text.data, max_new_tokens=1, num_return_sequences=5, repetition_penalty=100.0)
    return render_template('index.html', form=form, result=output)
