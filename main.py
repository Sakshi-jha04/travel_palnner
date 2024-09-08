import streamlit as st
import pickle
from poi_trialmerged import FINAL
import pandas as pd
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import folium
import random
import os
import datetime

streamlit_style = """
			<style>
			  @import url('https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;1,100&display=swap');

			  .hotel-bold {
			    font-weight: 600;
			  }

			  .hotel-font {
			    font-size: 20px;
          background-color: #e6f9ff;
			  }

			  label.css-1p2iens.effi0qh3{
			    font-size: 18px;
			  }

			  p{
			    font-size: 18px;
			  }
        li{
          font-size: 18px;
        }		
        #MainMenu{
        visibility: hidden;
        }	  
        button.css-135zi6y.edgvbvh9{
        font-size: 18px;
        font-weight: 600;
        }
			  
			</style>
			"""
st.set_page_config(page_title="Your Travel Planner")
st.markdown(streamlit_style, unsafe_allow_html=True)




#import streamlit_folium 
from streamlit_folium import folium_static
from PIL import Image

# List of image file paths
images = [
    "data/bg_mine1.png",
    "data/bg_mine2.png",
    "data/bg_mine3.png",
    "data/bg_mine4.png",
    "data/bg_mine5.png",
    "data/bg_mine6.png",
    "data/bg_mine7.png",
    "data/bg_mine8.png",
    "data/bg_mine9.png",
    "data/bg_mine10.png",
    "data/bg_mine11.png",
    "data/bg_mine12.png"
]

if 'index' not in st.session_state:
    st.session_state.index = 0

def next_image():
    st.session_state.index = (st.session_state.index + 1) % len(images)

def prev_image():
    st.session_state.index = (st.session_state.index - 1) % len(images)

def resize_image(image_path, new_width, new_height):
    img = Image.open(image_path)
    resized_img = img.resize((new_width, new_height))
    return resized_img

resized_img = resize_image(images[st.session_state.index], 500, 300)



st.image(resized_img, use_column_width=True)

col1, col2 = st.columns([1, 3])  # Adjust column sizes as needed
with col1:
    if st.button("<< Previous"):
        prev_image()
with col2:
    if st.button("Next >>"):
        next_image()


st.title('Personalised Travel Recommendation and Planner')

def feedback_form():
    st.subheader("We value your feedback!")
    
    # Email input
    email = st.text_input("Enter your email:")
    
    # Rating input (you can use a slider or selectbox for rating)
    rating = st.selectbox(
    "Rate your experience",
    ("Very Good", "Good", "Average", "Bad", "Very bad"),
    index=None,
    placeholder="Select one...",
    )

    
    # Additional comments
    comments = st.text_area("Additional comments:")
    
    if st.button("Submit Feedback"):
        ct = datetime.datetime.now()
        if email and comments:
            # Save feedback to a CSV file or database
            with open('data/feedback - Sheet1.csv', 'a') as f:
                f.write(f"{email},{rating},{comments},{ct}\n")
            
            st.success("Thank you for your feedback!")
        else:
            st.error("Please fill in all fields.")


def output_main(Type,Duration,Budget,TYPE,Ques):
    
    """Let's Authenticate the Banks Note 
    This is using docstrings for specifications.
    ---
    parameters:  
      - name: Type
        in: query
        type: string
        required: true
      - name: Duration
        in: query
        type: number
        required: true
      - name: Budget
        in: query
        type: number
        required: true
      - name: Ques
        in: query
        type: string
        required: true
      - name: .
        in: query
        type: number
        required: true
    responses:
        200:
            description: The output values
        
    """
   
    
  
    output,info, map = FINAL(Type,Duration,Budget,TYPE,Ques) 
    
    print(output)
    return [output,info,map]

def main():

    @st.cache_data
    def get_data():
      return []

    lis1 = ['Adventure and Outdoors','Spiritual','City Life', 'Cultural','Relaxing']
    lis2 = ['Family','Friends','Individual']

    Type = st.multiselect("Vacation type according to priority:",lis1)

    Duration = st.number_input("Duration (in Days)",1,30)
    Duration = int(Duration)
    
    Budget = st.slider("Budget (in INR)",min_value=200,max_value=150000,step=500)
    Budget = int(Budget)

    col1, col2 = st.columns(2)
    
    TYPE = col1.selectbox("Who are you travelling with?",lis2) ## already filled change
    Ques = col2.radio("Is covering maximum places a priority?",['Yes',"No"])

    date_of_arrival = st.date_input("Day of Arrival")
    Time_of_arrival = st.time_input("Time of Arrival")
    travelling_with_pet = st.toggle("Are you travelling with a pet?")
    ## Condition-Error
    cutoff = Budget/Duration

    result=""
    st.write(' ')
    if st.button("What do you recommend?"):

        try:
          RESULT = output_main(Type,Duration,Budget,TYPE,Ques)
        except:

          if(cutoff<260):
            st.subheader("Irrational. Try increasing your Budget or scaling down the Duration") # FORMAAT
          else:
            st.subheader("Irrational. Please check your Inputs")
          return

        
        get_data().append({"Type": Type, "Duration": Duration,
                           "Budget": Budget, "TYPE": TYPE, "Ques": Ques})
        
        FINAL_DATA = pd.DataFrame(get_data()) #####
        FINAL_DATA.to_csv('data/FinalData.csv') #####
        
        Output = RESULT[0]
        Info = RESULT[1]
        Map = RESULT[2]

        # # st.write(f'The size of Info is: {len(Info)}')
        # st.subheader('Your Selections')
        # # st.write('{}'.format(Info[0]))
        # col3, col4 = st.columns(2)
        # len(Info)
        # for i in range(1,len(Info)-5):
        #     try: 
        #         col3.write('{}'.format(Info[i]))
        #     except:
        #         continue
        # for i in range(4,len(Info)-2):
        #     try: 
        #         col4.write('{}'.format(Info[i]))
        #     except:
        #         continue
        # st.write('{}'.format(Info[-2]))

        st.subheader('Your Selections')
        col3, col4 = st.columns(2)

        # Display elements in col3
        for i in range(1, len(Info) - 5):  # Up to the 5th last element
            try:
                col3.write('{}'.format(Info[i]))
            except:
                continue

        # Display elements in col4 without overlapping col3
        for i in range(len(Info) - 5, len(Info) - 2):  # From the 5th last to the 3rd last element
            try:
                col4.write('{}'.format(Info[i]))
            except:
                continue

        # Display second-to-last element
        st.write('{}'.format(Info[-2]))
        
        st.header('Our Suggestions')
        # st.markdown('<p class="hotel-font" style="color: black;"><span class="hotel-bold" style="color: black;">Suggested Hotel/Accomodation:</span> {}</p>'.format(Info[-1]), unsafe_allow_html=True)
        st.markdown('<p class="hotel-font" style="color: white; background-color: rgb(250, 70, 62);"><span class="hotel-bold" style="color: white;">Suggested Hotel/Accommodation:</span> {}</p>'.format(Info[-1]), unsafe_allow_html=True)



        st.write(' ')
        for i in range(0,len(Output)):
          st.write('{}'.format(Output[i])) ## 

        st_map = folium_static(Map)
    feedback_form()

           


        
          
if __name__=='__main__':
    
    main()


