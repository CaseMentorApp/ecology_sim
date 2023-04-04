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
from streamlit_modal import Modal

modal = Modal(key="Demo Key",title="test")

def make_bar_style(x):
    if '%' in str(x):
        x = float(x.strip('%'))
        return f"background: linear-gradient(90deg,#5fba7d {x}%, transparent {x}%); width: 10em"  
    return ''

def check_if_equal(list_1, list_2):
    """ Check if both the lists are of same length and if yes then compare
    sorted versions of both the list to check if both of them are equal
    i.e. contain similar elements with same frequency. """
    if len(list_1) != len(list_2):
        return False
    return sorted(list_1) == sorted(list_2)

st.set_page_config(layout="wide", page_title="Ecosystem_Management_Simulation")

m = st.markdown("""
<style>
div.stButton > button:first-child {
     text-align : center;
       font-size:2px;
}
</style>""", unsafe_allow_html=True)

for_refrence = pd.read_csv("./simulation_1/for_refrence.csv")


numbers = re.compile(r'(\d+)')
image_list =[]


# get the path/directory
folder_dir = "./simulation_1/split_photo"
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
    with open("./simulation_1/split_photo//" + file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
        real_img_list.append(f"data:image/jpeg;base64,{encoded}")

sim1_plants = []
sim1_animal = []
# if 'sim1_plants' not in st.session_state:
#             st.session_state['sim1_plants'] = []
# if 'sim1_animal' not in st.session_state:
#             st.session_state['sim1_animal'] = []
# get the path/directory
folder_dir = './simulation_1/plants'
for images in os.listdir(folder_dir):
 
    # check if the image ends with png
    if (images.endswith(".png")):
       sim1_plants.append(images)
 # get the path/directory
folder_dir_animal = './simulation_1/animals'
for images in os.listdir(folder_dir_animal):
    # check if the image ends with png
    if (images.endswith(".png")):
        sim1_animal.append(images)       

if 'list' not in st.session_state:
    st.session_state['list'] = []
    
with st.sidebar:
    planet, animal = st.tabs(['plants','animals'])

with planet:
        for image in sim1_plants:
            with st.expander(str(image)[:-4]):
                col1, col2 = st.columns([3,1])
                with col1:
                    with Image.open('./simulation_1/plants/' + image) as img:
                        st.image(img)
                with col2:
                    if st.button('Add', key= str(image)[:-4]):
                        if len(st.session_state.list) < 8 :
                            if str(image)[:-4] not in st.session_state.list:
                                st.session_state.list.append(str(image)[:-4])

with animal:
        for image in sim1_animal:
            with st.expander(str(image)[:-4]):
                col1, col2 = st.columns([3,1])
                with col1:
                    with Image.open('./simulation_1/animals/' + image) as img:
                        st.image(img)
                with col2:
                    if st.button('Add', key= str(image)[:-4]):
                        if len(st.session_state.list) < 8 :
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
    st.markdown("<h2 style='text-align: left; color: grey;'>Ecosystem Management - Simulation 1</h2>", unsafe_allow_html=True)
    st.markdown('---')
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

True_species1 = ['Fairy Inkcap',
'Scarlet Star',
'Tree Fern',
'Striped Skunk',
'Lowland Paca',
'Red Acouchi',
'Crab-eating Fox',
'Pygmy Brocket'
]
True_species2 = ['Fairy Inkcap',
'Scarlet Star',
'Tree Fern',
'Striped Skunk',
'Lowland Paca',
'Red Acouchi',
'Crab-eating Fox',
'Merida Brocket'
]

optimal_alt =[201,680]
optimal_temp =[29.6,32]
optimal_wind =[1,9]
optimal_ph =[4.5,6]


#logical tests
if parameters[0] != "Please choose an ecosystem":
    altitude = (float(parameters[0]) >= optimal_alt[0])  & (float(parameters[0]) <= optimal_alt[1])
    temp = (float(parameters[1]) >= optimal_temp[0])  & (float(parameters[1]) <= optimal_temp[1])
    wind = (float(parameters[2]) >= optimal_wind[0])  & (float(parameters[2]) <= optimal_wind[1])
    ph = (float(parameters[3]) >= optimal_ph[0])  & (float(parameters[3]) <= optimal_ph[1])

with right:
    st.write('')
    st.write('')
    st.write('')
    if st.button('Submit'):
        if parameters[0] == "Please choose an ecosystem":
            with modal.container():
                st.markdown('Please choose an ecosystem')
        elif ((check_if_equal(st.session_state.list,True_species1)) | (check_if_equal(st.session_state.list,True_species2))) & (altitude & temp & wind & ph):
            with modal.container():
                st.markdown('Congratulations your Ecosystem is sustainable')
        else:
          with modal.container():
                st.markdown('Oh no! your Ecosystem is Not sustainable')  
            

    df = pd.DataFrame(data)
    hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

    #Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    #style
    th_props = [
        ('font-size', '14px'),
        ('text-align', 'center'),
        ('font-weight', 'bold'),
        ('color', '#6d6d6d'),
        ('background-color', '#f7ffff')
        ]
                                    
    td_props = [
        ('font-size', '13px'),
        ('color', '#6d6d6d')
        ]
                                    
    styles = [
        dict(selector="th", props=th_props),
        dict(selector="td", props=td_props)
        ]

    # table
    df2=df.style.set_properties(**{'text-align': 'left'}).set_table_styles(styles)
    st.table(df2)

with right:
    # st.markdown('---')
    st.markdown("<h5 style='text-align: left; color: grey;'>Selected Species " + str(len(st.session_state.list)) + "/8</h5>", unsafe_allow_html=True)

    col3, col4 = st.columns([2,1])
    with col4:
        for i in st.session_state.list:
                if st.button('Del', key = i + "del"):
                    st.session_state.list.remove(i)
    with col3:
        # for i in range(len(st.session_state.list)):
        #     st.markdown(st.session_state.list[i])
        df_species =pd.DataFrame(['Add Species']*8)
        for i in range(len(st.session_state.list)):
            df_species[0][i] = st.session_state.list[i]
        td_props = [
        ('font-size', '15px'),
        ('color', '#6d6d6d')
        ]
        styles = [
        dict(selector="th", props=th_props),
        dict(selector="td", props=td_props)
        ]
        style = df_species.style.hide_index().set_properties(**{'text-align': 'left'}).set_table_styles(styles)
        style.hide_columns()
        st.write(style.to_html(), unsafe_allow_html=True)
        




