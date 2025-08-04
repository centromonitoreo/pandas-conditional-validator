from datetime import datetime
import json

class ValidationLogger:
    def __init__(self, log_file=None):
        self.log_file = log_file
        self.entries = []

    def log_failure(self, parametro, row, rule, param_col):
        self.entries.append({
            "timestamp": datetime.utcnow().isoformat(),
            param_col: parametro,
            "row_data": row,
            "rule_failed": rule
        })

    def save(self):
        if self.log_file:
            with open(self.log_file, "w") as f:
                for entry in self.entries:
                    f.write(json.dumps(entry) + "\n")
