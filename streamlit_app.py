# Import Python packages

import streamlit as st
from snowflake.snowpark.functions import col


# Write directly to the app

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")

st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)


# Get the name for the smoothie

name_on_order = st.text_input("Name on Smoothie:")

st.write(
    "The name on your Smoothie will be:",
    name_on_order
)


# Connect to Snowflake

cnx = st.connection("snowflake")
session = cnx.session()


# Select the warehouse

session.sql("USE WAREHOUSE COMPUTE_WH").collect()


# Get fruit options from Snowflake

my_dataframe = session.table(
    "SMOOTHIES.PUBLIC.FRUIT_OPTIONS"
).select(
    col("FRUIT_NAME")
)


# Let the user choose up to 5 ingredients

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)


# Create the order

if ingredients_list:

    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "


    # Escape apostrophes in the name

    clean_name = (
        name_on_order.replace("'", "''")
        if name_on_order
        else ""
    )


    # SQL statement to insert the order

    my_insert_stmt = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS
        (
            INGREDIENTS,
            NAME_ON_ORDER,
            ORDER_FILLED
        )
        VALUES
        (
            '{ingredients_string}',
            '{clean_name}',
            FALSE
        )
    """


    # Submit button

    time_to_insert = st.button("Submit Order")


    if time_to_insert:

        if name_on_order:

            session.sql(my_insert_stmt).collect()

            st.success(
                "Your Smoothie is ordered, "
                + name_on_order
                + "!",
                icon="✅"
            )

        else:

            st.error(
                "Please enter a name on the Smoothie before submitting!"
            )
import requests

smoothiefruit_response = requests.get(
    "https://my.smoothiefruit.com/api/fruit/watermelon"
)

st.text(smoothiefruit_response)
