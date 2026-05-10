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


# -----------------------------
# RUN TEST
# -----------------------------
if __name__ == "__main__":
    metadata = build_relationship_prompt("Hello")
    print(metadata)