from fastai.vision.all import load_learner
import gradio as gr
from flask import Flask, render_template

app = Flask(__name__)

# Load the trained model
learn = load_learner('second_model.pkl')

# Define the categories based on your model's output
categories = learn.dls.vocab

# Define the function to classify images
def classify_image(img):
    pred, idx, probs = learn.predict(img)
    return dict(zip(categories, map(float, probs)))

# Define the Gradio components
image = gr.Image(type='pil', label='Upload an Image')
label = gr.Label(label="Predictions")
examples = ['images/faces/1.jpeg', 'images/faces/4.jpeg', 'images/faces/7.jpeg']  # Replace with your example images

# Create the Gradio interface
intf = gr.Interface(
    fn=classify_image, 
    inputs=image, 
    outputs=label, 
    title="Face to Race", 
    description="Upload an image to classify it based on the trained model.",
    examples=examples,
    live=True
)

@app.route('/')
def index():
    return render_template('index.html', gradio_url=intf.local_url)

if __name__ == '__main__':
    intf.launch(share=True, inline=False, debug=True)
    app.run(host='0.0.0.0', port=8080)