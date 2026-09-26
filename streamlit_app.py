# Import Python packages

import streamlit as st
from snowflake.snowpark.functions import col


# Page title

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")

st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)


# Name on smoothie

name_on_order = st.text_input("Name on Smoothie:")

st.write(
    "The name on your Smoothie will be:",
    name_on_order
)


# Connect to Snowflake

cnx = st.connection("snowflake")
session = cnx.session()


# Show connection information

current_role = session.sql(
    "SELECT CURRENT_ROLE()"
).collect()[0][0]

current_database = session.sql(
    "SELECT CURRENT_DATABASE()"
).collect()[0][0]

current_schema = session.sql(
    "SELECT CURRENT_SCHEMA()"
).collect()[0][0]

current_warehouse = session.sql(
    "SELECT CURRENT_WAREHOUSE()"
).collect()[0][0]

st.write("Current Snowflake role:", current_role)
st.write("Current database:", current_database)
st.write("Current schema:", current_schema)
st.write("Current warehouse:", current_warehouse)


# Get fruit options

my_dataframe = session.table(
    "SMOOTHIES.PUBLIC.FRUIT_OPTIONS"
).select(
    col("FRUIT_NAME")
)


# Choose ingredients

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)


# Submit order

if ingredients_list:

    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "

    clean_name = (
        name_on_order.replace("'", "''")
        if name_on_order
        else ""
    )

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

    st.write("SQL being executed:")

    st.code(
        my_insert_stmt,
        language="sql"
    )

    time_to_insert = st.button("Submit Order")

    if time_to_insert:

        if not name_on_order:

            st.error(
                "Please enter a name on the Smoothie before submitting!"
            )

        else:

            try:

                result = session.sql(
                    my_insert_stmt
                ).collect()

                st.success(
                    "Your Smoothie is ordered, "
                    + name_on_order
                    + "!",
                    icon="✅"
                )

            except Exception as e:

                st.error("INSERT FAILED")

                st.write("Actual Snowflake error:")

                st.code(
                    str(e)
                )
