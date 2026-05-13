import source_database_layer as sdl
import schema_layer.metadata_extractor as metadata_extractor
import llm_layer
import graph_layer as gl


my_path = "C:/Programming/Neo4J/GraphSync/Data Sets/office"


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

def get_metadata():
    metadata =  metadata_extractor.extract_full_metadata()
    return metadata

# ================================================
# Testing Phase
# ================================================

def get_insite():
    meta_data = get_metadata()
    prompt = llm_layer.llm_prompt_builder.build_relationship_prompt(metadata=meta_data)
    insite = llm_layer.llm_client.call_llm(prompt=prompt)
    return insite

def transform_to_node(tablename : str):
    return gl.node_creator.create_nodes(tablename)

# ================================================
# Testing Phase
# ================================================
print(transform_to_node("employee_data"))

#=================================================
# OUTPUT
#=================================================
'''
[
    {
        "from_table": "Employee",
        "from_column": "EmpID",
        "to_table": "Department",
        "to_column": "DeptID",
        "relationship": "many_to_one",
        "confidence": 0.8
    },
    {
        "from_table": "Order",
        "from_column": "CustomerID",
        "to_table": "Customer",
        "to_column": "ID",
        "relationship": "one_to_many",
        "confidence": 0.9
    },
    {
        "from_table": "ProductReview",
        "from_column": "ProductID",
        "to_table": "Product",
        "to_column": "ID",
        "relationship": "many_to_one",
        "confidence": 0.85
    },
    {
        "from_table": "Payment",
        "from_column": "OrderID",
        "to_table": "Order",
        "to_column": "ID",
        "relationship": "one_to_many",
        "confidence": 0.95
    }
]
'''