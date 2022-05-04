words_count_responses = {
    200: {
        "description": "Everything went well",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "words_counts": {
                            "type": "array",
                            "description":
                            "list of words objects with attached count number"
                        }
                    }
                }
            }
        }
    },
    400: {
        "description": "A connection error occured with the given url",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "error": {
                            "type": "string",
                            "description": "Error message"
                        }
                    }
                }
            }
        }
    },
    404: {
        "description": "The distant url is not available at the moment",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "error": {
                            "type": "string",
                            "description": "Error message"
                        }
                    }
                }
            }
        }
    },
    415: {
        "description": "A content type error occured with the given url",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "error": {
                            "type": "string",
                            "description": "Error message"
                        }
                    }
                }
            }
        }
    },
    422: {
        "description": "An error occured due to one of the given parameters"
        " (url or order)",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "error": {
                            "type": "string",
                            "description": "Error message"
                        }
                    }
                }
            }
        }
    },
    500: {
        "description": "An internal error occured",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "error": {
                            "type": "string",
                            "description": "Error message"
                        }
                    }
                }
            }
        }
    }
}
