import json


def build_relationship_prompt(metadata):
    schema_text = json.dumps(metadata, indent=2)

    LLM_RELATIONSHIP_DETECTION_PROMPT = """
                                          You are a database schema analysis expert.

                                          You will be given a JSON object containing multiple database tables. Each table includes:
                                          - table_name
                                          - columns (name, type, nullable)
                                          - sample_data

                                          Your task is to infer relationships between tables based ONLY on:
                                          1. Column names
                                          2. Column data types
                                          3. Sample data values
                                          4. Semantic meaning of fields

                                          ========================
                                          GOAL
                                          ========================

                                          Identify all possible relationships between tables and return them in this JSON format:

                                          [
                                            {
                                              "from_table": "",
                                              "from_column": "",
                                              "to_table": "",
                                              "to_column": "",
                                              "relationship": "one_to_one | one_to_many | many_to_one | many_to_many",
                                              "confidence": 0.0
                                            }
                                          ]

                                          ========================
                                          RELATIONSHIP DETECTION RULES
                                          ========================

                                          1. Primary Matching Logic:
                                          - Match columns with similar meaning (e.g., EmpID ↔ Employee ID)
                                          - Normalize names (case, spaces, underscores)
                                          - Use sample_data overlap when available

                                          2. Foreign Key Inference:
                                          Assume relationship exists if:
                                          - Values in one column appear in another table
                                          - Same entity representation across tables (Employee, ID, User, etc.)

                                          3. Relationship Types:
                                          - one_to_one → unique mapping in both tables
                                          - one_to_many → one record maps to multiple records
                                          - many_to_one → reverse direction of one_to_many
                                          - many_to_many → indirect or ambiguous shared mapping

                                          4. Confidence Scoring (0.0 to 1.0):
                                          - 0.9 - 1.0 → exact match + strong sample evidence
                                          - 0.7 - 0.9 → strong semantic match
                                          - 0.4 - 0.7 → likely but partially uncertain
                                          - 0.1 - 0.4 → weak inference

                                          ========================
                                          ANALYSIS STRATEGY
                                          ========================

                                          - Compare EVERY table with EVERY other table
                                          - Check all column-to-column relationships
                                          - Use sample_data to validate relationships
                                          - Detect implicit relationships even without foreign keys
                                          - Infer relationships even when column names differ slightly

                                          ========================
                                          INPUT
                                          ========================

                                          You will receive a JSON schema like this:

                                          {schema_text}

                                          ========================
                                          OUTPUT RULES
                                          ========================

                                          - Return ONLY valid JSON
                                          - Do NOT include explanations
                                          - Do NOT include markdown formatting
                                          - Do NOT hallucinate relationships
                                          - Prefer accuracy over guessing
                                          - If unsure, lower the confidence score instead of forcing a relationship
                                          """
    return LLM_RELATIONSHIP_DETECTION_PROMPT


import json


def build_relationship_prompt_without_sample(metadata):
    schema_text = json.dumps(metadata, indent=2)

    LLM_RELATIONSHIP_DETECTION_PROMPT = f"""
        You are an expert Database Architect, Data Modeler, Relational Database Expert, and Graph Database Architect.

        Your task is to analyze the relational database schema provided below and identify all possible relationships between tables.

        The input consists of one or more database tables.

        Each table contains:
        - table_name
        - columns
        - data_type
        - nullable
        - primary_key
        - sample_data
        - (optional) foreign_key information

        =========================================================
        OBJECTIVE
        =========================================================

        Analyze the schema and infer relationships between tables.

        You should identify:

        1. Explicit Foreign Key relationships.
        2. Inferred Foreign Key relationships.
        3. Self-referencing relationships.
        4. Junction (Many-to-Many) tables.
        5. Relationship Cardinality.
        6. Candidate Graph Entities.

        Only infer relationships when there is sufficient evidence.

        Never invent relationships.

        =========================================================
        RELATIONSHIP DETECTION RULES
        =========================================================

        1. Highest Priority
        -------------------
        Use explicit Foreign Keys whenever available.

        2. If Foreign Keys are missing
        ------------------------------
        Infer relationships using:

        - Similar column names
        - Primary Keys
        - Data Types
        - Naming conventions
        - Sample data overlap
        - Common relational database design

        3. Detect Relationship Types
        ----------------------------

        Possible values:

        FOREIGN_KEY
        INFERRED
        SELF_REFERENCE
        JOIN_TABLE

        4. Detect Cardinality
        ---------------------

        Possible values:

        ONE_TO_ONE
        ONE_TO_MANY
        MANY_TO_ONE
        MANY_TO_MANY

        5. Confidence
        -------------

        HIGH
        MEDIUM
        LOW

        6. Self Reference
        -----------------

        If a table references itself, mark:

        "is_self_reference": true

        Example:

        Employee.manager_id
        ↓

        Employee.employee_id

        7. Join Table Detection
        -----------------------

        If a table mainly consists of two or more foreign keys connecting other tables,
        mark:

        "is_join_table": true

        =========================================================
        GRAPH ENTITY DETECTION
        =========================================================

        Generate candidate graph entities.

        Example:

        employees
        ↓

        Employee

        departments
        ↓

        Department

        projects
        ↓

        Project

        =========================================================
        OUTPUT FORMAT
        =========================================================

        Return ONLY valid JSON.

        Do NOT include explanations.

        Do NOT include markdown.

        Do NOT include additional text.

        =========================================================
        JSON FORMAT
        =========================================================

        {{
            "relationships": [
                {{
                    "source_table": "",
                    "source_column": "",
                    "target_table": "",
                    "target_column": "",

                    "source_entity": "",
                    "target_entity": "",

                    "relationship_type": "",

                    "cardinality": "",

                    "candidate_relationship_name": "",

                    "semantic_group": "",

                    "is_self_reference": false,

                    "is_join_table": false,

                    "confidence": "",

                    "reason": "",

                    "evidence": [
                        ""
                    ]
                }}
            ]
        }}

        =========================================================
        IMPORTANT RULES
        =========================================================

        1. Analyze ALL tables.

        2. Compare every table with every other table.

        3. Compare every column with every column.

        4. Never create duplicate relationships.

        5. If multiple tables describe the same relationship,
        return it only once.

        6. Prefer explicit foreign keys over inferred relationships.

        7. Do NOT analyze business logic beyond the schema.

        8. Do NOT generate Cypher queries.

        9. Do NOT generate SQL queries.

        10. Return ONLY the JSON object.

        =========================================================
        DATABASE SCHEMA
        =========================================================

        {schema_text}

        """

    return LLM_RELATIONSHIP_DETECTION_PROMPT


# -----------------------------
# RUN TEST
# -----------------------------
if __name__ == "__main__":
    metadata = build_relationship_prompt("Hello")
    print(metadata)
