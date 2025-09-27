import streamlit as st
import requests 
from db import get_connection
import queries

def insertData(classiName):
    connection = get_connection()
    if not connection:
        print("❌ Connection failed.")
        return
    
    cursor = connection.cursor()

    try:
        # Optional: Clear old data
        #cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        #cursor.execute("TRUNCATE TABLE artifact_media;")
        #cursor.execute("TRUNCATE TABLE artifact_colors;")
        #cursor.execute("TRUNCATE TABLE artifact_metadata;")
        #cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

        #classiName = 'Coins'
        records = queries.fetchSpecificClasi(classiName)
        artifacts, media, colors = queries.makeRecordsDic(records)

        insert_meta = """INSERT INTO artifact_metadata VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        insert_media = """INSERT INTO artifact_media VALUES(%s,%s,%s,%s,%s,%s,%s)"""
        insert_col  = """INSERT INTO artifact_colors VALUES(%s,%s,%s,%s,%s,%s)"""

        # ✅ Perform batch inserts
        cursor.executemany(insert_meta, [
            (i['id'], i['title'], i['culture'], i['period'], i['century'], i['medium'],
             i["dimensions"], i['description'], i["department"], i['classification'],
             i['accessionyear'], i['accessionmethod'], i['division'], i['dated']) 
            for i in artifacts
        ])

        cursor.executemany(insert_media, [
            (j['objectid'], j['imagecount'], j['mediacount'],
             j['colorcount'], j['rank'], j['datebegin'], j["dateend"]) 
            for j in media
        ])

        cursor.executemany(insert_col, [
            (k['objectid'], k['color'], k['spectrum'],
             k['hue'], k['percent'], k['css3']) 
            for k in colors
        ])

        connection.commit()
        print("✅ Data inserted successfully!")

        cursor.execute("SELECT COUNT(*) FROM artifact_metadata;")
        print("Rows in metadata:", cursor.fetchone()[0])

    except Exception as e:
        connection.rollback()
        print("❌ Error:", e)

    finally:
        cursor.close()
        connection.close()
        print("🔒 MySQL connection closed.")


# --------------------
# 🔹 Utility functions
# --------------------

def classification():
    connection = get_connection()
    if not connection:
        print("❌ Connection failed.")
        return
    
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT(classification) FROM artifact_metadata")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


def getArtifactsMetadata():
    connection = get_connection()
    if not connection:
        print("❌ Connection failed.")
        return
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM artifact_metadata")
    result = cursor.fetchall()
    des = cursor.description
    cursor.close()
    connection.close()
    return result, des


def getArtifactsMedia():
    connection = get_connection()
    if not connection:
        print("❌ Connection failed.")
        return
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM artifact_media")
    result = cursor.fetchall()
    des = cursor.description
    cursor.close()
    connection.close()
    return result ,des


def getArtifactsColors():
    connection = get_connection()
    if not connection:
        print("❌ Connection failed.")
        return
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM artifact_colors")
    result = cursor.fetchall()
    des = cursor.description
    cursor.close()
    connection.close()
    return result, des

