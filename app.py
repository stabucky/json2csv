import streamlit as st
import json2csv

def main():
  st.title('JSON2CSV')

  btn={}
  with st.form("my_form"):
    textarea_val = st.text_area("JSON", value="")
    submitted = st.form_submit_button("Submit")

    if submitted:
      result = json2csv.json2text(textarea_val)
      # st.text_area("Result", height=150, value=result["text"])

      if "keys" in result:
        for key in result["keys"]:
          result2 = json2csv.json2text(textarea_val,key)
          st.text_area(key, value=result2["text"])
      if "error" in result:
        st.error(result["error"])
    
  st.write("&copy;2022You Look Too Cool")





if __name__ == "__main__":
  main()
