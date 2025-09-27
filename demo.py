import streamlit as st 
from streamlit_option_menu import option_menu
import queries
import app as dba
import pandas as pd

st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center; color: black;'>🎨🏛️ Harvard’s Artifacts Collection</h1>", unsafe_allow_html=True)

classification = st.text_input("Enter a classification:")  # e.g. Coins, Vessels, Paintings
button = st.button("Collect data")

menu = option_menu(None, ["Select Your Choice","Migrate to SQL","SQL Queries"], orientation="horizontal")

# -----------------------
# Collect Data Section
# -----------------------
if button:
    if classification.strip() == "":
        st.error("Kindly enter a classification")
    else:
        st.write("✅ You clicked the button!")

        try:
           # dba.insertData()
            records = queries.fetchSpecificClasi(classification)
            arti, med, col = queries.makeRecordsDic(records)

            c1, c2, c3 = st.columns(3)
            with c1:
                st.header("Metadata")
                st.json(arti)
            with c2:
                st.header("Media")
                st.json(med)
            with c3:
                st.header("Colours")
                st.json(col)

        except Exception as e:
            st.error(f"❌ Error: {e}")


# -----------------------
# Migrate to SQL Section
# -----------------------
if menu == 'Migrate to SQL':
    try:
        result1 = dba.classification()
        classes_list = [i[0] for i in result1]

        st.subheader("Insert the collected data")
        if st.button("Insert"):
            if classification.strip() == "":
                st.error("Please enter a classification first!")
            elif classification not in classes_list:
                dba.insertData(classification)
               # records = queries.fetchSpecificClasi(classification)
                # arti, med, col = queries.makeRecordsDic(records)

                # TODO: Insert arti, med, col into DB here
                st.success("✅ Data Inserted successfully")

                st.header("Inserted Data:")
                st.divider()

                # ⚡ Ensure helper functions return (result, description)
                result1, des1 = dba.getArtifactsMetadata()
                df1 = pd.DataFrame(result1, columns=[i[0] for i in des1])
                st.subheader("Artifacts Metadata")
                st.dataframe(df1)

                result2, des2 = dba.getArtifactsMedia()
                df2 = pd.DataFrame(result2, columns=[i[0] for i in des2])
                st.subheader("Artifacts Media")
                st.dataframe(df2)

                result3, des3 = dba.getArtifactsColors()
                df3 = pd.DataFrame(result3, columns=[i[0] for i in des3])
                st.subheader("Artifacts Colors")
                st.dataframe(df3)

            else:
                st.error("Classification already exists! Try a different class.")
    except Exception as e:
        st.error(f"❌ Error: {e}")            

elif menu == "SQL Queries":
            print("enter the sql") 
            option = st.selectbox(
                        "Queries",
                        (
                        "Select a query...",
                        "1. List all artifacts from the 11th century belonging to Byzantine culture.",
                        "2. What are the unique cultures represented in the artifacts?",
                        "3. List all artifacts from the Archaic Period",
                        "4. List artifact titles ordered by accession year in descending order.",
                        "5. How many artifacts are there per department?"
    
                        ),
                        index=0
            )

            option1 = st.selectbox(
                        "Queries",
                        (
                         "Select a query...",   
                        "1. Which artifacts have more than 1 image? ", 
                        "2. What is the average rank of all artifacts?",
                        "3. Which artifacts have a higher colorcount than mediacount?",
                        "4. List all artifacts created between 1500 and 1600.",
                        "5.How many artifacts have no media files? "
        
                        ),
                        index=0
            )

            option2 = st.selectbox(
                        "Queries",
                        (
                       
                        "Select a query...",   
                        "1. What are all the distinct hues used in the dataset?", 
                        "2. What are the top 5 most used colors by frequency?",
                        "3. What is the average coverage percentage for each hue?",
                        "4. List all colors used for a given artifact ID.",
                        "5. What is the total number of color entries in the dataset?"
                        
                       ),
                        index=0
            )

            option3 = st.selectbox(
                        "Queries",
                        (
                       
                        "Select a query...",   
                        "1. List artifact titles and hues for all artifacts belonging to the Byzantine culture.", 
                        "2. List each artifact title with its associated hues.",
                        "3. Get artifact titles, cultures, and media ranks where the period is not null",
                        "4. Find artifact titles ranked in the top 10 that include the color hue Grey.",
                        "5. How many artifacts exist per classification, and what is the average media count for each?"
                        
                       ),
                        index=0
         )
        
            if option1 != "Select a query...":
                try:
                    connection = dba.get_connection()
                    cursor = connection.cursor()

                    if option1.startswith("1."):
                            cursor.execute("""
                            select amd.title As Title, amd.department As Department, amd.classification As Classification, am.objectid As ObjectID , sum(am.imagecount) As Sum_of_Image_Count from artifact_media as am left join artifact_metadata as amd on am.objectid = amd.id group by am.objectid having sum(am.imagecount) > 1 ;
                            """)
                    
                    elif option1.startswith("2."):
                            cursor.execute("""
                            select objectid As ObjectID, avg(`rank`) as Average_of_Rank from artifact_media as am GROUP BY ObjectID;
                            """)
                    
                    elif option1.startswith("3."):
                            cursor.execute("""
                            select * from artifact_media as am where colorcount > mediacount  ; 
                            """)
                    
                    elif option1.startswith("4."):
                            cursor.execute("""
                            select * from artifact_media as am where datebegin >= 1500 && dateend <= 1600 ;
                            """)
                    
                    elif option1.startswith("5."):
                            cursor.execute("""
                            select count(*) as No_media_of_file_count from artifact_media as am where am.mediacount = 0;
                            """)

                    result = cursor.fetchall()
                    df = pd.DataFrame(result, columns=[i[0] for i in cursor.description])
                    st.dataframe(df)

               
                except Exception as e:
                        st.error(f"❌ Error: {e}")

                finally:
                        cursor.close()
                        connection.close()        
            
            elif option != "Select a query...":
                try:
                    connection = dba.get_connection()
                    cursor = connection.cursor()

                    if option.startswith("1."):
                            cursor.execute("""
                            SELECT * 
                            FROM artifact_metadata 
                            WHERE dated = '11th century' AND culture = 'Byzantine';
                            """)
                    
                    elif option.startswith("2."):
                            cursor.execute("""
                            SELECT DISTINCT culture 
                            FROM artifact_metadata;
                            """)
                    
                    elif option.startswith("3."):
                            cursor.execute("""
                            SELECT * 
                            FROM artifact_metadata 
                            WHERE period = 'Archaic';
                            """)
                    
                    elif option.startswith("4."):
                            cursor.execute("""
                            SELECT title, accessionyear 
                            FROM artifact_metadata 
                            ORDER BY accessionyear DESC;
                            """)
                    
                    elif option.startswith("5."):
                            cursor.execute("""
                            SELECT department, COUNT(*) AS artifact_count
                            FROM artifact_metadata 
                            GROUP BY department;
                            """)

                    result = cursor.fetchall()
                    df = pd.DataFrame(result, columns=[i[0] for i in cursor.description])
                    st.dataframe(df)

               
                except Exception as e:
                        st.error(f"❌ Error: {e}")

                finally:
                        cursor.close()
                        connection.close()

            if option2 != "Select a query...":
                try:
                    connection = dba.get_connection()
                    cursor = connection.cursor()

                    if option2.startswith("1."):
                            cursor.execute("""
                            SELECT DISTINCT hue FROM artifact_colors ORDER BY hue;
                            """)
                    
                    elif option2.startswith("2."):
                            cursor.execute("""
                            select color, count(*) as frequency from artifact_colors group by color order by frequency DESC limit 5 ;
                            """)
                    
                    elif option2.startswith("3."):
                            cursor.execute("""
                            SELECT DISTINCT hue, avg(percent) as per FROM artifact_colors group by hue ORDER BY per;
                            """)
                    
                    elif option2.startswith("4."):
                            cursor.execute("""
                            SELECT objectid, color FROM artifact_colors where objectid = 259298  ORDER BY color;
                            """)
                    
                    elif option2.startswith("5."):
                            cursor.execute("""
                            SELECT DISTINCT color, count(color) FROM artifact_colors group by color ORDER BY color;
                            """)

                    result = cursor.fetchall()
                    df = pd.DataFrame(result, columns=[i[0] for i in cursor.description])
                    st.dataframe(df)

               
                except Exception as e:
                        st.error(f"❌ Error: {e}")

                finally:
                        cursor.close()
                        connection.close() 


            if option3 != "Select a query...":
                try:
                    connection = dba.get_connection()
                    cursor = connection.cursor()

                    if option3.startswith("1."):
                            cursor.execute("""
                            select am.title, amt.hue from artifact_metadata am left join artifact_colors amt on am.id = amt.objectid where am.culture = 'Byzantine';
                            """)
                    
                    elif option3.startswith("2."):
                            cursor.execute("""
                            select am.title, GROUP_CONCAT(amt.hue ORDER BY amt.hue SEPARATOR ', ') AS hues from artifact_metadata am left join artifact_colors amt on am.id = amt.objectid where am.culture = 'Byzantine' GROUP BY am.title;
                            """)
                    
                    elif option3.startswith("3."):
                            cursor.execute("""
                            SELECT a.title, a.culture, am.rank FROM artifact_metadata a JOIN artifact_media am ON a.id = am.objectid WHERE a.period IS NOT NULL;
                            """)
                    
                    elif option3.startswith("4."):
                            cursor.execute("""
                            SELECT a.title, am.rank, ac.hue FROM artifact_metadata a JOIN artifact_media am ON a.id = am.objectid JOIN artifact_colors ac ON am.objectid = ac.objectid WHERE ac.hue = 'Grey' ORDER BY am.rank ASC LIMIT 10;""")
                    
                    elif option3.startswith("5."):
                            cursor.execute("""
                            SELECT a.classification,COUNT(DISTINCT a.id) AS artifact_count,AVG(am.media_count) AS avg_media_count
                                FROM artifact_metadata a
                                        JOIN (
                                        SELECT objectid, COUNT(*) AS media_count
                                        FROM artifact_media
                                        GROUP BY objectid
                                        ) am 
                                        ON a.id = am.objectid
                                        GROUP BY a.classification
                                        ORDER BY artifact_count DESC;""") 

                    result = cursor.fetchall()
                    df = pd.DataFrame(result, columns=[i[0] for i in cursor.description])
                    st.dataframe(df)

               
                except Exception as e:
                        st.error(f"❌ Error: {e}")

                finally:
                        cursor.close()
                        connection.close()        
                              
                
                