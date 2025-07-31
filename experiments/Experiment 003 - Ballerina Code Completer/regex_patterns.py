# # Regex to match Ballerina function definitions
# function_pattern = r'function\s+\w+\s*\([^)]*\)\s*(?:returns\s+\w+)?\s*\{[^}]*\}'

# # Regex to match Ballerina service definitions
# service_pattern = r'service\s+\w+\s+on\s+\w+\s*\{[^}]*\}'

# # Combined regex pattern to match both function and service definitions
# pattern = rf'({function_pattern}|{service_pattern})'
import re

# Function pattern as a separate variable
function_pattern = r'''
    \s*                                     # Optional leading whitespace
    (?:                             # Optional modifiers for function
        (?:public|private)?\s*      # Visibility modifier
        (?:isolated|remote|transactional|worker)?\s*  # Function modifiers
    )?
    function\s+                     # Required 'function' keyword
    [a-zA-Z_]\w*                    # Function name
    \s*                             # Optional whitespace
    \(                              # Parameter list
    (?:                             # Parameters (optional)
        (?:                         # Parameter type and name
            (?:                     # Type descriptor
                [a-zA-Z_]\w*(?:\[])?|map<\w+>|record\s*{[^}]*}
            )
            \s+
            [a-zA-Z_]\w*
            (?:\s*=\s*[^,)]+)?      # Optional default value
        )
        (?:\s*,\s*                  # Multiple parameters
            (?:
                (?:[a-zA-Z_]\w*(?:\[])?|map<\w+>|record\s*{[^}]*})
                \s+
                [a-zA-Z_]\w*
                (?:\s*=\s*[^,)]+)?
            )
        )*
    )?
    \)                              # End parameters
    \s*
    (?:                             # Optional return type
        returns\s+
        (?:
            [a-zA-Z_]\w*(?:\[])?|map<\w+>|record\s*{[^}]*}|
            (?:[a-zA-Z_]\w*(?:\|\s*[a-zA-Z_]\w*)*)
        )
        \??
    )?
    \s*
    \{                              # Opening brace for function
'''

# Service pattern as a separate variable
service_pattern = r'''
    \s*                             # Optional leading whitespace
    (?:                             # Optional modifiers for service
        (?:public|private)?\s*      # Visibility modifier
        (?:isolated)?\s*            # Service modifier
    )?
    service\s+                      # Required 'service' keyword
    (?:                             # Optional service type
        [a-zA-Z_]\w*(?:\[])?|map<\w+>|record\s*{[^}]*}
    )?\s*
    on\s+                           # Required 'on' keyword
    [a-zA-Z_]\w*                    # Listener expression (simplified)
    (?:\s*,\s*[a-zA-Z_]\w*)*        # Optional additional listeners
    \s*
    \{                              # Opening brace for service
'''

# Combine the patterns
pattern = rf'''
    (?:
        {function_pattern}
        |
        {service_pattern}
    )
'''