from sql_client import SqlClient
import click

@click.command()
@click.argument('sql_schema_filepath', type=click.Path())
@click.argument('config_filepath', type=click.Path())
@click.argument('section_name', type=click.Path())
def main(sql_schema_filepath, config_filepath, section_name):
    file_name = config_filepath
    section_name = section_name

    with open(sql_schema_filepath, 'r') as file:
        query_schema = file.read().replace('\n', '')

    a = SqlClient(file_name, section_name)

    try:
        to_database=True
        a.connect(to_database=to_database)

    except Exception as e:
        print ('Unable to connect to database')

    a.execute(query_schema)
    a.close_connection()

if __name__ == "__main__":
    main()