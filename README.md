# 🤗🧪
## hugging-flask: a Flask app for [huggingface](https://huggingface.co/)

![hugging-flask](https://github.com/hadleyrose/gifs/blob/main/demo/hugging-flask.png?raw=true)

### Current Features
* [Fill Mask with DistilBERT](#fill-mask-with-distilbert)
* [Next Word Text Generation with GPT2](#next-word-text-generation-with-gpt2)
* [Sentence Similarity with DistilBERT or GPT2 Embeddings](#sentence-similarity-with-distilbert-or-gpt2-embeddings)

#### Fill Mask with DistilBERT
To utilize the `Fill Mask` capabilities

1. Select `DistilBERT` as `LLM`
2. Select `Fill Mask` as `Task`
3. Enter text with `[MASK]`(s) wherever you want the model to fill in the text, e.g. `Fill in [MASK] text`
4. Click `Submit` or hit Enter/Return

![hugging-flask Fill Mask demo](https://github.com/hadleyrose/gifs/blob/main/demo/hugging-flask_FillMask.gif?raw=true)

#### Next Word Text Generation with GPT2
To utilize the `Text Generation` capabilities

1. Select `GPT2` as `LLM`
2. Select `Text Generation` as `Task`
3. Enter text
4. Click `Submit` or hit Enter/Return

**NOTE:** Currently only supports next word generation

![hugging-flask Text Generation demo](https://github.com/hadleyrose/gifs/blob/main/demo/hugging-flask_NextWord.gif?raw=true)

#### Sentence Similarity with DistilBERT or GPT2 Embeddings
To utilize the `Sentence Similarity` capabilities

1. Select either `DistilBERT` or `GPT2` as `LLM`
2. Select `Sentence Similarity` as `Task`
3. Enter text for similarity comparison as sentences separated by periods, e.g. `This is my first text for comparison. This is my second text for comparison. This is my third text for comparison.`
4. Click `Submit` or hit Enter/Return

![hugging-flask Similarity demo](https://github.com/hadleyrose/gifs/blob/main/demo/hugging-flask_Similarity.gif?raw=true)

### TODO
- [ ] Error handling & flash warnings
- [ ] Buffering indicator
- [ ] In-app usage popovers
- [ ] File Upload support