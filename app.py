# import os
# import pandas as pd
# import pickle
# from pypdf import PdfReader
# import re
# import streamlit as st

# # Load models
# word_vector = pickle.load(open("tfidf.pkl", "rb"))
# model = pickle.load(open("model.pkl", "rb"))

# def cleanResume(txt):
#     cleanText = re.sub('http\S+\s', ' ', txt)
#     cleanText = re.sub('RT|cc', ' ', cleanText)
#     cleanText = re.sub('#\S+\s', ' ', cleanText)
#     cleanText = re.sub('@\S+', '  ', cleanText)  
#     cleanText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
#     cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText) 
#     cleanText = re.sub('\s+', ' ', cleanText)
#     return cleanText

# category_mapping = {
#     15: "Java Developer",
#     23: "Testing",
#     8: "DevOps Engineer",
#     20: "Python Developer",
#     24: "Web Designing",
#     12: "HR",
#     13: "Hadoop",
#     3: "Blockchain",
#     10: "ETL Developer",
#     18: "Operations Manager",
#     6: "Data Science",
#     22: "Sales",
#     16: "Mechanical Engineer",
#     1: "Arts",
#     7: "Database",
#     11: "Electrical Engineering",
#     14: "Health and fitness",
#     19: "PMO",
#     4: "Business Analyst",
#     9: "DotNet Developer",
#     2: "Automation Testing",
#     17: "Network Security Engineer",
#     21: "SAP Developer",
#     5: "Civil Engineer",
#     0: "Advocate",
# }

# def categorize_resumes(uploaded_files, output_directory):
#     if not os.path.exists(output_directory):
#         os.makedirs(output_directory)
    
#     results = []
    
#     for uploaded_file in uploaded_files:
#         if uploaded_file.name.endswith('.pdf'):  # We can change the extension as per requirement
#             reader = PdfReader(uploaded_file)
#             page = reader.pages[0]
#             text = page.extract_text()
#             cleaned_resume = cleanResume(text)

#             input_features = word_vector.transform([cleaned_resume])
#             prediction_id = model.predict(input_features)[0]
#             category_name = category_mapping.get(prediction_id, "Unknown")
            
#             category_folder = os.path.join(output_directory, category_name)
            
#             if not os.path.exists(category_folder):
#                 os.makedirs(category_folder)
            
#             target_path = os.path.join(category_folder, uploaded_file.name)
#             with open(target_path, "wb") as f:
#                 f.write(uploaded_file.getbuffer())
            
#             results.append({'filename': uploaded_file.name, 'category': category_name})
    
#     results_df = pd.DataFrame(results)
#     return results_df

# st.title("Resume Categorization: Web Application")

# uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
# output_directory = st.text_input("Output Directory", "categorized_resumes")

# if st.button("Categorize Resumes"):
#     if uploaded_files and output_directory:
#         results_df = categorize_resumes(uploaded_files, output_directory)
#         st.write(results_df)
#         results_csv = results_df.to_csv(index=False).encode('utf-8')
#         st.download_button(
#             label="Download results as CSV",
#             data=results_csv,
#             file_name='categorized_resumes.csv',
#             mime='text/csv',
#         )
#         st.success("Resume categorization and processing completed.")
#     else:
#         st.error("Please upload files and specify the output directory.")


import os
import pandas as pd
import pickle
from pypdf import PdfReader
import re
import streamlit as st


# Load models
word_vector = pickle.load(open("tfidf.pkl", "rb"))
model = pickle.load(open("model.pkl", "rb"))


def cleanResume(txt):
    cleanText = re.sub(r'http\S+\s', ' ', txt)
    cleanText = re.sub(r'RT|cc', ' ', cleanText)
    cleanText = re.sub(r'#\S+\s', ' ', cleanText)
    cleanText = re.sub(r'@\S+', '  ', cleanText)  
    cleanText = re.sub(r'[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
    cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText) 
    cleanText = re.sub(r'\s+', ' ', cleanText)
    return cleanText

category_mapping = {
    15: "Java Developer",
    23: "Testing",
    8: "DevOps Engineer",
    20: "Python Developer",
    24: "Web Designing",
    12: "HR",
    13: "Hadoop",
    3: "Blockchain",
    10: "ETL Developer",
    18: "Operations Manager",
    6: "Data Science",
    22: "Sales",
    16: "Mechanical Engineer",
    1: "Arts",
    7: "Database",
    11: "Electrical Engineering",
    14: "Health and Fitness",
    19: "PMO",
    4: "Business Analyst",
    9: "DotNet Developer",
    2: "Automation Testing",
    17: "Network Security Engineer",
    21: "SAP Developer",
    5: "Civil Engineer",
    0: "Advocate",
}

def categorize_resumes(uploaded_files, word_vector, model):
    results = []
    categorized_files = {}

    for uploaded_file in uploaded_files:
        if uploaded_file.name.lower().endswith('.pdf'):
            try:
                reader = PdfReader(uploaded_file)
                text = ""
                for page in reader.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:
                        text += extracted_text + " "
                cleaned_resume = cleanResume(text)

                input_features = word_vector.transform([cleaned_resume])
                prediction_id = model.predict(input_features)[0]
                category_name = category_mapping.get(prediction_id, "Unknown")
                
                # Initialize category list if not present
                if category_name not in categorized_files:
                    categorized_files[category_name] = []
                
                # Store tuple of (filename, file bytes)
                file_bytes = uploaded_file.read()
                categorized_files[category_name].append((uploaded_file.name, file_bytes))
                
                results.append({'filename': uploaded_file.name, 'category': category_name})
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {e}")

    results_df = pd.DataFrame(results)
    return results_df, categorized_files

# Streamlit App
st.title("Resume Categorization: Web Application")

uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

if st.button("🚀 Categorize Resumes"):
    if uploaded_files:
        with st.spinner("Categorizing resumes..."):
            results_df, categorized_files = categorize_resumes(uploaded_files, word_vector, model)
        
        if not results_df.empty:
            st.success("✅ Resume categorization completed!")
            st.write("### Categorization Results")
            st.dataframe(results_df)

        else:
            st.warning("No resumes were categorized. Please check the uploaded files.")
    else:
        st.error("⚠️ Please upload at least one PDF file.")
