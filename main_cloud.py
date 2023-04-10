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
from streamlit.components.v1 import html
import asyncio
from datetime import datetime

modal = Modal(key="Demo Key",title="test")

my_html = """
<script>
function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    setInterval(function () {
        minutes = parseInt(timer / 60, 10)
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            timer = duration;
        }
    }, 1000);
}
window.onload = function () {
    var fiveMinutes = 60 * 30,
        display = document.querySelector('#time');
    startTimer(fiveMinutes, display);
};
</script>

<header>
  <h2><span id="time">30:00</span></h2>
</header>
"""





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

def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

st.set_page_config(layout="wide", page_title="Ecosystem_Management_Simulation")


m = st.markdown("""
<style>
div.stButton > button:first-child {
     text-align : center;
       font-size:1px;
       height : 20px;
       margin : 0px;
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


image_list = sorted(image_list, key=numericalSort)

real_img_list = []
for file in image_list:
    with open("./simulation_1/split_photo//" + file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
        real_img_list.append(f"data:image/jpeg;base64,{encoded}")

sim1_plants = []
sim1_animal = []

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
               
sim1_animal = sorted(sim1_animal, key=numericalSort)
sim1_plants = sorted(sim1_plants, key=numericalSort)



if 'list' not in st.session_state:
    st.session_state['list'] = []

# containers
map_container = st.container()
conditions_container = st.container()
species_container = st.container()
sub_container = st.container()





with st.sidebar:
    planet, animal = st.tabs(['plants','animals'])

with planet:
        for image in sim1_plants:
                col1, col2 = st.columns([3,1])
                with col1:
                    with st.expander(str(image)[:-4]):
                        with Image.open('./simulation_1/plants/' + image) as img:
                            st.image(img)
                with col2:
                    if st.button('Add', key= str(image)[:-4]):
                        if len(st.session_state.list) < 8 :
                            if str(image)[:-4] not in st.session_state.list:
                                st.session_state.list.append(str(image)[:-4])

with animal:
        for image in sim1_animal:
                col1, col2 = st.columns([3,1])
                with col1:
                    with st.expander(str(image)[:-4]):
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
                    "width": "40px",
                    "height":"21px",}
    )



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



st.markdown(
    """
    <style>
    .time {
        font-size: 130px !important;
        font-weight: 700 !important;
        color: #ec5953 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


with right:
    # html(my_html)
    submit = st.button('Submit')
    st.markdown("<h5 style='text-align: left; color: grey;'>Conditions </h5>", unsafe_allow_html=True)
    col_top_left,col_top_mid, col_top_right = st.columns([0.5,3,1.5])
    with col_top_left:
        check_alt = st.checkbox('', key='altitdue')
        check_temp= st.checkbox('', key='temp')
        check_wind = st.checkbox('', key='wind')
        check_ph  = st.checkbox('', key='ph')
        check_air = st.checkbox('', key='air')
        check_cloud = st.checkbox('', key='cloud')
        check_sun = st.checkbox('', key='sun')
        check_list = [check_alt,check_temp,check_wind,check_ph,check_air,check_cloud,check_sun]
        
    with col_top_right:
        col_lst = ["Altitude:","Tempeture","Wind Speed:","Soil PH:","Air Pressure:","Cloud Height:","Sunlight Hours:"]
        parameters = [str(for_refrence['alt'][clicked]) if clicked > -1 and check_alt and (sum(check_list) <= 4) else "-",
                str(for_refrence['temp'][clicked]) if clicked > -1 and check_temp and (sum(check_list) <= 4) else "-",
                str(for_refrence['wind'][clicked]) if clicked > -1 and check_wind and (sum(check_list) <= 4) else "-",
                str(for_refrence['ph'][clicked]) if clicked > -1 and check_ph and (sum(check_list) <= 4) else "-",
                str(for_refrence['pressure'][clicked]) if clicked > -1 and check_air and (sum(check_list) <= 4) else "-",
                str(for_refrence['cloud'][clicked]) if clicked > -1 and  check_cloud and (sum(check_list) <= 4) else "-",
                str(for_refrence['sunlight'][clicked]) if clicked > -1 and  check_sun and (sum(check_list) <= 4) else "-"]
        data = {"Condtions": col_lst,
            "Values": parameters}
    for i in range(len(parameters)):
        with col_top_mid:
            st.caption(col_lst[i])
    for i in range(len(parameters)):       
        with col_top_right:
            st.caption(parameters[i])
  
        # df = pd.DataFrame(data)
        # hide_table_row_index = """
        #         <style>
        #         thead tr th:first-child {display:none}
        #         tbody th {display:none}
        #         </style>
                # """


    # #Inject CSS with Markdown
    #     st.markdown(hide_table_row_index, unsafe_allow_html=True)
    # #style
    #     th_props = [
    #         ('font-size', '14px'),
    #         ('text-align', 'center'),
    #         ('font-weight', 'bold'),
    #         ('color', '#6d6d6d'),
    #         ('background-color', '#f7ffff')
    #         ]
                                        
    #     td_props = [
    #         ('font-size', '11px'),
    #         ('color', '#6d6d6d')
    #         ]
                                        
    #     styles = [
    #         dict(selector="th", props=th_props),
    #         dict(selector="td", props=td_props)
    #         ]

    # # table
    #     df2=df.style.set_properties(**{'text-align': 'left'}).set_table_styles(styles)
    #     st.table(df2)


with right:
    st.markdown("<h5 style='text-align: left; color: grey;'>Selected Species " + str(len(st.session_state.list)) + "/8</h5>", unsafe_allow_html=True)
    df_species =pd.DataFrame(['Add Species']*8)    

    for i in range(len(st.session_state.list)):
            df_species[0][i] = st.session_state.list[i]

    # td_props = [
    #     ('font-size', '12px'),
    #     ('text-align', 'center'),
    #     ('font-weight', 'bold'),
    #     ('color', '#6d6d6d'),
    #     ('background-color', '#f7ffff')
    #     ]
    # styles = [
    #     dict(selector="th", props=th_props),
    #     dict(selector="td", props=td_props)
    #     ]
    # df_species_style = df_species.style.hide_index().set_properties(**{'text-align': 'left'}).set_table_styles(styles)
    # df_species_style.hide_columns()
    for i in st.session_state.list:
            col3, col4 = st.columns([2,1])
            with col3:
                st.markdown(i)
            with col4:
                if st.button('Del', key = i + "del"):
                    st.session_state.list.remove(i)


if ((parameters[0] != "-") & (parameters[1] != "-") & (parameters[2] != "-") & (parameters[3] != "-")):
    altitude = (float(parameters[0]) >= optimal_alt[0])  & (float(parameters[0]) <= optimal_alt[1])
    temp = (float(parameters[1]) >= optimal_temp[0])  & (float(parameters[1]) <= optimal_temp[1])
    wind = (float(parameters[2]) >= optimal_wind[0])  & (float(parameters[2]) <= optimal_wind[1])
    ph = (float(parameters[3]) >= optimal_ph[0])  & (float(parameters[3]) <= optimal_ph[1])

with left:
    if submit:
        if parameters[0] == "-":
            with modal.container():
                st.markdown('Please choose an ecosystem')
        elif ((parameters[0] != "-") | (parameters[1] != "-") | (parameters[2] != "-") | (parameters[3] != "-")):
            with modal.container():
                st.markdown('Please choose the right ecosystem conditions')
        elif ((check_if_equal(st.session_state.list,True_species1)) | (check_if_equal(st.session_state.list,True_species2))) & (altitude & temp & wind & ph):
            with modal.container():
                st.markdown('Congratulations your Ecosystem is sustainable')
        else:
            with modal.container():
                st.markdown('Oh no! your Ecosystem is Not sustainable') 

