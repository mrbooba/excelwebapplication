import pandas as pd
import streamlit as st
import plotly.express as px
import base64
import os
import json
import pickle
import uuid
import re

import streamlit as st
from PIL import Image


st.set_page_config(page_title='Survey Results')
st.header('Excel Web Application')
st.subheader('Here is an excel sheet exposed as a Web Application')
st.subheader('What do you think about it ?')

### --- LOAD DATAFRAME

def load_data():        
        excel_file = 'excelfiles/Survey_Results.xlsx'
        sheet_name = 'DATA'

        df = pd.read_excel(excel_file, engine='openpyxl',
                        sheet_name=sheet_name,
                        usecols='B:H',
                        header=3)
    #    df = pd.DataFrame(df, index=['Projet', 'Ressource', 'Description', 'Tâche', 'Commentaires', 'Nombre de jour', 'Chargé de projet'])
      #  df.drop(['0'], axis=1)
        df.dropna(inplace=True)

        df_participants = pd.read_excel(excel_file, engine='openpyxl',
                                        sheet_name=sheet_name,
                                        usecols='J:K',
                                        header=3)
        df_participants.dropna(inplace=True)
        
        # --- STREAMLIT SELECTION
       # keys = ['Projet', 'Ressource', 'Description', 'Tâche', 'Commentaires', 'Nombre de jour', 'Chargé de projet']
       # df.loc[keys].dropna()
        projet = df['Projet'].unique().tolist()
        nbjours = df['Nombre de jour'].unique().tolist()

        nbjour_selection =  st.slider('Nombre de jour:', min_value=min(nbjours), max_value=max(nbjours), value=(min(nbjours),max(nbjours)))

        # nbjour_selection = ''
        # try:
        #     nbjour_selection =  st.slider("Nombre de jour:",
        #                         min_value= int(input(min(nbjours))),
        #                         max_value= int(input(max(nbjours))),
        #                         value=(min(nbjours),max(nbjours)))
        # except EOFError as e:
        #     st.write("Il y a un soucis")
            
        projet_selection = st.multiselect('Projet:',
                                        projet,
                                        default=projet)

        # --- FILTER DATAFRAME BASED ON SELECTION
        mask = (df['Nombre de jour'].between(*nbjour_selection)) & (df['Projet'].isin(projet_selection))
        number_of_result = df[mask].shape[0]
        st.markdown(f'*Available Results: {number_of_result}*')

        # --- GROUP DATAFRAME AFTER SELECTION
        df_grouped = df[mask].groupby(by=['Projet']).count()[['Nombre de jour']]
        df_grouped = df_grouped.rename(columns={"Nombre de jour": "Votes"})
        df_grouped = df_grouped.reset_index()

        # --- PLOT BAR CHART
        bar_chart = px.bar(df_grouped,
                        x="Projet",
                        y="Votes",
                        text="Votes",
                        color_discrete_sequence = ['#F63366']*len(df_grouped),
                        template= "plotly_white")
        st.plotly_chart(bar_chart)

        #--- FORM
        @st.cache(allow_output_mutation=True)
        def get_data():
            return []

        form = st.form(key='my-form')
        projet = form.text_input('Entrer le nom du projet')
        ressource = form.text_input('Entrer le nom de la ressource')
        description = form.text_input('Entrer la description')
        tache = form.text_input('Entrer la tâche')
        commentaire = form.text_input('Entrer le commentaire')
        nbjours = form.text_input('Entrer le nombre de jours')
        cp = form.text_input('Entrer le nom du chef de projet')

        submit = form.form_submit_button('Submit')

       # df2 = pd.DataFrame()
        if submit:
            get_data().append({"Projet": projet,
                "Ressource": ressource, "Description": description,
                "Tâche": tache, "Commentaires": commentaire, 
                "Nombre de jour": nbjours, "Chargé de projet": cp})
         #   xcelfile = 'excelfiles/Survey_Results.xlsx'
          #  df2  = pd.DataFrame()
            #df2 = pd.ExcelWriter('excelfiles/Survey_Results.xlsx', engine='openpyxl')
           
            #df2.to_excel("excelfiles/Survey_Results.xlsx", sheet_name='DATA')
    #        with pd.ExcelWriter('excelfiles/Survey_Results.xlsx', mode='a') as writer:
     #           df2.to_excel(writer, sheet_name='DATA', engine='openpyxl')
         #       writer.save()

        df2 = pd.DataFrame(get_data())
        st.write(df2)
        df3 = df.append(df2, ignore_index=True)
        df3.to_excel(excel_file, sheet_name, header=False, index=False)
#         df3 = pd.ExcelWriter('excelfiles/Survey_Results.xlsx', sheet_name='DATA', mode='a', engine='openpyxl')
#         df2.to_excel(df3)
#         df3.save()
#         file = pd.read_excel(df3, sheet_name='DATA', engine='openpyxl')
#         file.dropna(inplace=True)
#         st.write(file)
    #     writer = pd.ExcelWriter(excel_file, engine='openpyxl', mode='a')
    #     writer.book = load_workbook(excel_file)
    #     writer.sheets = {ws.title:ws for ws in writer.book.worksheets}
    #  #   df.iloc[:, 1:]
    #     df2.to_excel(writer, 'DATA', startrow=len(df)+3, index = False, header = None)
    #     writer.save()
      #  df3 = df2.copy().append(df2.to_excel('excelfiles/Survey_Results.xlsx', sheet_name='DATA'))
      #  st.write(df3)
     #   df2.to_excel("excelfiles/Survey_Results.xlsx", sheet_name='DATA')
        #st.write(get_data())
            #st.write(df2)
       # st.write(pd.DataFrame(get_data()).append(df_grouped))
           # st.dataframe(df2)
        # --- DISPLAY IMAGE & DATAFRAME
        col1, col2 = st.beta_columns(2)
        image = Image.open('images/survey.jpg')
        print(image)
        col1.image(image,
                caption='Designed by slidesgo / Freepik',
                use_column_width=True)
        col2.dataframe(df[mask])
        #df2 = df2.drop_duplicates()        
       # col2.dataframe(file)

        # --- PLOT PIE CHART
        
        pie_chart = px.pie(df_participants,
                        title='Total No. of Participants',
                        values='Participants',
                        names='Departments')

        st.plotly_chart(pie_chart)



def download_button(object_to_download, download_filename, button_text, pickle_it=False):
    """
    Generates a link to download the given object_to_download.

    Params:
    ------
    object_to_download:  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv,
    some_txt_output.txt download_link_text (str): Text to display for download
    link.
    button_text (str): Text to display on download button (e.g. 'click here to download file')
    pickle_it (bool): If True, pickle file.

    Returns:
    -------
    (str): the anchor tag to download object_to_download

    Examples:
    --------
    download_link(your_df, 'YOUR_DF.csv', 'Click to download data!')
    download_link(your_str, 'YOUR_STRING.txt', 'Click to download text!')

    """
    if pickle_it:
        try:
            object_to_download = pickle.dumps(object_to_download)
        except pickle.PicklingError as e:
            st.write(e)
            return None

    else:
        if isinstance(object_to_download, bytes):
            pass

        elif isinstance(object_to_download, pd.DataFrame):
            object_to_download = object_to_download.to_csv(index=False)

        # Try JSON encode for everything else
        else:
            object_to_download = json.dumps(object_to_download)

    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    button_uuid = str(uuid.uuid4()).replace('-', '')
    button_id = re.sub('\d+', '', button_uuid)

    custom_css = f""" 
        <style>
            #{button_id} {{
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: 0.25em 0.38em;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;

            }} 
            #{button_id}:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
                }}
        </style> """

    dl_link = custom_css + f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br></br>'

    return dl_link



def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)


if __name__ == '__main__':
    load_data()
     # --------------------------
    # Select a file to download
    # --------------------------   
    if st.checkbox('Select a file to download'):
            st.write('~> Use if you want to test uploading / downloading a certain file.')

            # Upload file for testing
            folder_path = st.text_input('Enter directory: default', 'excelfiles')
            filename = file_selector(folder_path=folder_path)

            # Load selected file
            with open(filename, 'rb') as f:
                s = f.read()

            download_button_str = download_button(s, filename, f'Click here to download {filename}')
            st.markdown(download_button_str, unsafe_allow_html=True)

        
 #       load_data()
   
     