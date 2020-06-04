from sql_client import SqlClient
import click


@click.command()
@click.argument('config_filepath', type=click.Path())
@click.argument('section_name', type=click.Path())
def main(config_filepath, section_name):
    file_name = config_filepath
    section_name = section_name

    query_create_db = "create database yelp"

    a = SqlClient(file_name, section_name)

    try:
        to_database = False
        a.connect(to_database=to_database)
        a.execute(query_create_db)
        a.close_connection()

    except Exception as e:
        print('Unable to create database')

if __name__ == "__main__":
    main()