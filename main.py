import source_database_layer as sdl
import schema_layer.metadata_extractor as metadata_extractor
import llm_layer
import graph_layer as gl

my_path = "C:/Programming/Neo4J/GraphSync/Data Sets/office"


# to make the import form the csv file to the data tables
def make_import():
    # Extract list of valid files
    valid_files = sdl.validator.file_extractor(my_path)

    # build a connection
    connection_engine = sdl.connection.create_db_connection()

    # make an import in postgres
    database_import = sdl.importer.import_to_postgres(
        valid_files, my_path, connection_engine
    )
    return database_import


# fetch the metadata of the table with the column type and it's category
def get_metadata():
    metadata = metadata_extractor.extract_full_metadata()
    return metadata


# ================================================
# Testing Phase
# ================================================


def get_insite():
    meta_data = get_metadata()
    prompt = llm_layer.llm_prompt_builder.build_relationship_prompt(metadata=meta_data)
    insite = llm_layer.llm_client.call_llm(prompt=prompt)
    return insite


def transform_to_node(tablename: str, primaryKey: str):
    insite = get_insite()
    print(insite)
    # return gl.node_creator.create_nodes(tablename,primaryKey)


# ================================================
# Testing Phase
# ================================================
def main():
    tables = metadata_extractor.get_tables()
    for tablename in tables:
        primaryKey = metadata_extractor.get_primary_key(tablename)
        # Create the Node form the Table name and the primary key
        gl.node_creator.create_nodes(tablename, primaryKey[0])
        


if __name__ == "__main__":
    main()
