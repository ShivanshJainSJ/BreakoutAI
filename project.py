import streamlit as st
import pandas as pd
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load the pre-trained GPT-2 model and tokenizer
model_name = "gpt2"  # You can also try "gpt2-medium", "gpt2-large", or "gpt2-xl"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

def generate_text(prompt):
    # Encode the input prompt
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    
    # Generate text
    outputs = model.generate(inputs, max_length=100, num_return_sequences=1)
    
    # Decode the output
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text

def main():
    st.title("AI Text Generation with GPT-2")
    
    # File upload section
    st.subheader("Upload a CSV File (optional)")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview:")
        st.write(df.head())  # Display the first few rows of the dataframe

    # Prompt input section
    st.subheader("Enter Your Prompt")
    prompt = st.text_area("Prompt:")
    
    if st.button("Generate"):
        if prompt:
            generated_text = generate_text(prompt)
            st.write("Generated Text:")
            st.write(generated_text)
        else:
            st.warning("Please enter a prompt.")

if __name__ == "__main__":
    main()