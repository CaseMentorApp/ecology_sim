import streamlit as st
from PIL import Image
from st_clickable_images import clickable_images
import os
from os import listdir
import base64
import pandas as pd
import glob, os
import re
from split_image import split_image


st.set_page_config(layout="wide", page_title="Ecosystem_Management_Simulation")

m = st.markdown("""
<style>
div.stButton > button:first-child {
     text-align : center;
       font-size:2px;
}
</style>""", unsafe_allow_html=True)

for_refrence = pd.read_csv("for_refrence.csv")

st.markdown("<h2 style='text-align: left; color: grey;'>Ecosystem Management - Simulation 1</h2>", unsafe_allow_html=True)
st.markdown('---')
st.button('Submit')

numbers = re.compile(r'(\d+)')
image_list =[]


# get the path/directory
folder_dir = r"\split"
for images in os.listdir(folder_dir):
    # check if the image ends with png
    if (images.endswith(".png")):
        image_list.append(images)

def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts
image_list = sorted(image_list, key=numericalSort)

real_img_list = []
for file in image_list:
    with open("\split\\" + file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
        real_img_list.append(f"data:image/jpeg;base64,{encoded}")

sim1_plants = []

# get the path/directory
folder_dir = r"\simulation_1_plants"
for images in os.listdir(folder_dir):
 
    # check if the image ends with png
    if (images.endswith(".png")):
        sim1_plants.append(images)

if 'list' not in st.session_state:
    st.session_state['list'] = []
    
with st.sidebar:
    planet, animal = st.tabs(['plants','animals'])

with planet:
        for image in sim1_plants:
            with st.expander(str(image)[:-4]):
                col1, col2 = st.columns([3,1])
                with col1:
                    with Image.open(r"\simulation_1_plants\\" + image) as img:
                        st.image(img)
                with col2:
                    if st.button('Add', key= str(image)[:-4]):
                        if str(image)[:-4] not in st.session_state.list:
                            st.session_state.list.append(str(image)[:-4])



# with planet:
#     with col2:
#         for image in sim1_plants:
#             if st.button('Add', key= str(image)[:-4]):
#               if str(image)[:-4] not in st.session_state.list:
#                 st.session_state.list.append(str(image)[:-4])             

left, right = st.columns([3.5,1])
with left:  
    st.markdown("<h4 style='text-align: left; color: grey;'>Instructions</h4>", unsafe_allow_html=True)
    st.caption("""Move through the cells of the map with your mouse and read the comments for the environmental conditions associated with the cell.
                Once you find a cell to place your ecosystem, click on it to select the cell. The relevant conditions will now appear on the top-right menu.""")
    clicked = clickable_images(
       real_img_list,
        titles=["Altitude:" + str(for_refrence['alt'][i]) +
                 "\n" + "Temperture:" + str(for_refrence['temp'][i]) +
                 "\n" + "Wind:" + str(for_refrence['wind'][i]) +
                 "\n" + "Soil PH:" + str(for_refrence['ph'][i]) +
                 "\n" + "Air Pressure:" + str(for_refrence['pressure'][i]) +                  
                 "\n" + "Cloud Height:" + str(for_refrence['cloud'][i]) +
                 "\n" + "Sunlight Hours:" + str(for_refrence['sunlight'][i]) for i in range(len(real_img_list))],
        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
        img_style={"margin": "0.5px",
                    "width": "41px",
                    "height":"21px",}
    )


    st.markdown(
        """
        <style>
        img {
            cursor: pointer;
            transition: all .2s ease-in-out;
        }
        img:hover {
            transform: scale(1.15);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )






with right:

    col_lst = ["Altitude:","Tempeture","Wind Speed:","Soil PH:","Air Pressure:","Cloud Height:","Sunlight Hours:"]
    parameters = [str(for_refrence['alt'][clicked]) if clicked > -1 else "Please choose an ecosystem",
                  str(for_refrence['temp'][clicked]) if clicked > -1 else "",
                  str(for_refrence['wind'][clicked]) if clicked > -1 else "",
                  str(for_refrence['ph'][clicked]) if clicked > -1 else "",
                  str(for_refrence['pressure'][clicked]) if clicked > -1 else "",
                  str(for_refrence['cloud'][clicked]) if clicked > -1 else "",
                  str(for_refrence['sunlight'][clicked]) if clicked > -1 else ""]
    data = {"Conditions": col_lst,
        "": parameters}
    df = pd.DataFrame(data)
    hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.table(df)

with right:
    st.markdown('---')
    st.markdown("<h5 style='text-align: left; color: grey;'>Selected Species</h5>", unsafe_allow_html=True)
    col3, col4 = st.columns([2,1])
    with col4:
        for i in st.session_state.list:
                if st.button('Del', key = i + "del"):
                    st.session_state.list.remove(i)
    with col3:
        for i in range(len(st.session_state.list)):
            st.markdown(st.session_state.list[i])






