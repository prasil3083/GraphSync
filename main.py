import source_database_layer.validator as validator
from source_database_layer import connection
import source_database_layer.importer as importer

my_path = "C:/Programming/Neo4J/GraphSync/Data Sets/office"

#Extract list of valid files
valid_files = validator.file_extractor(my_path)

#build a connection
connection_engine = connection.create_db_connection()

#make an import in postgres 
database_import = importer.import_to_postgres(valid_files,my_path,connection_engine) 

#


