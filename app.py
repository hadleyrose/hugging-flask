from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms.fields import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_bootstrap import Bootstrap5
from transformers import pipeline, set_seed
from nltk import tokenize
from sentence_transformers import SentenceTransformer, util
import pandas as pd

class LLM_Task_Form(FlaskForm):
    llm = SelectField('LLM', choices=[('distilbert', 'DistilBERT'), ('gpt', 'GPT2')])
    task = SelectField('Task', choices=[('fill', 'Fill Mask'), ('gen', 'Text Generation'), ('sim', 'Sentence Similarity')])
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
        if form.task.data == 'sim':
            sentences = tokenize.sent_tokenize(form.text.data)
            model_checkpoint = 'distilbert-base-uncased'
            if form.llm.data == 'gpt':
                model_checkpoint = 'gpt2'
            model = SentenceTransformer(model_checkpoint)
            # Compute embeddings and cosine similarity
            try:
                results = util.paraphrase_mining(model, sentences)
            except ValueError:
                model.tokenizer.pad_token = model.tokenizer.eos_token
                results = util.paraphrase_mining(model, sentences)
            output = [{'Cosine Similarity': i[0], 'Sentence 1': sentences[i[1]], 'Sentence 2': sentences[i[2]]} for i in results]
            output = pd.DataFrame(output).to_html(classes='table').replace('class="dataframe table"', 'class="table"')
        elif form.llm.data == 'distilbert':
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
