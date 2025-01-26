Production-Level Logging Best Practices
1. Structured Logging
Why? Structured logging (e.g., JSON format) makes it easier to parse and analyze logs. It allows you to filter, search, and aggregate logs efficiently.

How? Use a logging library that supports structured logging. In Python, you can use the python-json-logger library to log messages in JSON format.

Code Example:

import logging
from logging.handlers import RotatingFileHandler
import os
from pythonjsonlogger import jsonlogger

# Define the logger
logger = logging.getLogger('autogen_trace_logger')
logger.setLevel(logging.INFO)  # Set the log level to INFO for production

# Create a file handler with log rotation
log_file = os.path.join('logs', 'autogen_trace.log')
file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024*5, backupCount=5)  # 5 MB per file, 5 files

# Create a console handler
console_handler = logging.StreamHandler()

# Define a JSON formatter
formatter = jsonlogger.JsonFormatter()

# Set the formatter for the handlers
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Example usage
logger.info("This is an info message", extra={"user_id": 123, "session_id": "abc123"})
logger.error("This is an error message", extra={"user_id": 456, "session_id": "def456"})
2. Log Levels
Why? Using appropriate log levels categorizes the importance of log messages. For production, setting the log level to WARNING or ERROR helps avoid excessive logging, which can degrade performance and clutter log files.

How? Set the log level using logger.setLevel(logging.WARNING) or logger.setLevel(logging.ERROR).

Code Example:

import logging

# Define the logger
logger = logging.getLogger('autogen_trace_logger')
logger.setLevel(logging.WARNING)  # Set the log level to WARNING for production

# Example usage
logger.debug("This debug message will not be logged")
logger.info("This info message will not be logged")
logger.warning("This warning message will be logged")
logger.error("This error message will be logged")
logger.critical("This critical message will be logged")
3. Log Rotation
Why? Log rotation manages log file sizes by rotating log files at regular intervals or when they reach a certain size, and archiving old log files.

How? Use RotatingFileHandler from the logging.handlers module.

Code Example:

import logging
from logging.handlers import RotatingFileHandler
import os

# Define the logger
logger = logging.getLogger('autogen_trace_logger')
logger.setLevel(logging.INFO)  # Set the log level to INFO for production

# Create a file handler with log rotation
log_file = os.path.join('logs', 'autogen_trace.log')
file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024*5, backupCount=5)  # 5 MB per file, 5 files

# Define a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set the formatter for the handler
file_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(file_handler)

# Example usage
for i in range(1000):
    logger.info(f"Log entry {i}")
4. External Log Management
Why? External log management tools (e.g., ELK Stack, Splunk) centralize, search, and analyze logs. They provide powerful features for monitoring and alerting.

How? Send logs to an external logging system. For example, you can use Logstash or Fluentd to send logs to Elasticsearch.

Code Example: Here's an example using LogstashHandler to send logs to Logstash.

import logging
from pythonjsonlogger import jsonlogger
from logstash_async.handler import AsynchronousLogstashHandler

# Define the logger
logger = logging.getLogger('autogen_trace_logger')
logger.setLevel(logging.INFO)  # Set the log level to INFO for production

# Create a Logstash handler
logstash_handler = AsynchronousLogstashHandler(
    host='localhost',
    port=5000,
    database_path=None,  # Use None for in-memory
    formatter=jsonlogger.JsonFormatter()
)

# Add the handler to the logger
logger.addHandler(logstash_handler)

# Example usage
logger.info("This is an info message", extra={"user_id": 123, "session_id": "abc123"})
logger.error("This is an error message", extra={"user_id": 456, "session_id": "def456"})
5. Sensitive Data
Why? Avoid logging sensitive information such as passwords, credit card numbers, or personal identifiable information (PII). Use environment variables or secure vaults to manage sensitive data.

How? Filter out sensitive information in your logging configuration.

Code Example:

import logging
from logging.handlers import RotatingFileHandler
import os
from pythonjsonlogger import jsonlogger

# Define the logger
logger = logging.getLogger('autogen_trace_logger')
logger.setLevel(logging.INFO)  # Set the log level to INFO for production

# Create a file handler with log rotation
log_file = os.path.join('logs', 'autogen_trace.log')
file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024*5, backupCount=5)  # 5 MB per file, 5 files

# Define a JSON formatter
formatter = jsonlogger.JsonFormatter()

# Set the formatter for the handler
file_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(file_handler)

# Example usage
def log_with_filter(message, extra):
    # Filter out sensitive data
    if 'password' in extra:
        extra['password'] = '[REDACTED]'
    logger.info(message, extra=extra)

log_with_filter("This is an info message", extra={"user_id": 123, "password": "mysecretpassword"})
6. Log Context
Why? Include contextual information in logs to help understand the state of the application when an event occurred. This can include user IDs, session IDs, request IDs, and timestamps.

How? Use the extra parameter in logging methods to add contextual information.

Code Example:

import logging
from logging.handlers import RotatingFileHandler
import os
from pythonjsonlogger import jsonlogger

# Define the logger
logger = logging.getLogger('autogen_trace_logger')
logger.setLevel(logging.INFO)  # Set the log level to INFO for production

# Create a file handler with log rotation
log_file = os.path.join('logs', 'autogen_trace.log')
file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024*5, backupCount=5)  # 5 MB per file, 5 files

# Define a JSON formatter
formatter = jsonlogger.JsonFormatter()

# Set the formatter for the handler
file_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(file_handler)

# Example usage
logger.info("This is an info message", extra={"user_id": 123, "session_id": "abc123", "request_id": "req123"})
logger.error("This is an error message", extra={"user_id": 456, "session_id": "def456", "request_id": "req456"})
7. Performance Considerations
Why? Be mindful of the performance impact of logging, especially at high log levels. Use asynchronous logging or batching to minimize the overhead.

How? Use asynchronous logging handlers.

Code Example:

import logging
from logging.handlers import RotatingFileHandler
import os
from pythonjsonlogger import jsonlogger
from logstash_async.handler import AsynchronousLogstashHandler

# Define the logger
logger = logging.getLogger('autogen_trace_logger')
logger.setLevel(logging.INFO)  # Set the log level to INFO for production

# Create a file handler with log rotation
log_file = os.path.join('logs', 'autogen_trace.log')
file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024*5, backupCount=5)  # 5 MB per file, 5 files

# Define a JSON formatter
formatter = jsonlogger.JsonFormatter()

# Set the formatter for the handler
file_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(file_handler)

# Create a Logstash handler for asynchronous logging
logstash_handler = AsynchronousLogstashHandler(
    host='localhost',
    port=5000,
    database_path=None,  # Use None for in-memory
    formatter=jsonlogger.JsonFormatter()
)

# Add the handler to the logger
logger.addHandler(logstash_handler)

# Example usage
for i in range(1000):
    logger.info(f"Log entry {i}", extra={"user_id": i, "session_id": f"session{i}"})
8. Alerting and Monitoring
Why? Set up alerts and monitoring based on log messages. For example, you can configure alerts for critical errors or unusual activity.

How? Use external monitoring tools (e.g., ELK Stack, Splunk) to set up alerts and dashboards.

Code Example: Here's an example of setting up alerts in Elasticsearch using Kibana (part of the ELK Stack).

Set up Elasticsearch and Kibana.
Configure Logstash to send logs to Elasticsearch.
Create a Kibana dashboard.
Set up alerts in Kibana.
Example of Logstash Configuration:

input {
  tcp {
    port => 5000
    codec => json_lines
  }
}

output {
  elasticsearch {
    hosts => ["http://localhost:9200"]
    index => "autogen_trace_logs-%{+YYYY.MM.dd}"
  }
  stdout { codec => rubydebug }
}
Example of Kibana Alert:

Open Kibana.
Go to "Stack Management" > "Alerting".
Create a new alert rule.
Set the rule to trigger when certain log messages (e.g., level: "ERROR") are detected.
Summary
By implementing these best practices, you can ensure that your logging system is robust, efficient, and capable of supporting a large-scale project like a $1 million project. Here's a complete example combining several of these practices:

import logging
from logging.handlers import RotatingFileHandler
import os
from pythonjsonlogger import jsonlogger
from logstash_async.handler import AsynchronousLogstashHandler

# Define the logger
logger = logging.getLogger('autogen_trace_logger')
logger.setLevel(logging.INFO)  # Set the log level to INFO for production

# Create a file handler with log rotation
log_file = os.path.join('logs', 'autogen_trace.log')
file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024*5, backupCount=5)  # 5 MB per file, 5 files

# Define a JSON formatter
formatter = jsonlogger.JsonFormatter()

# Set the formatter for the handler
file_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(file_handler)

# Create a Logstash handler for asynchronous logging
logstash_handler = AsynchronousLogstashHandler(
    host='localhost',
    port=5000,
    database_path=None,  # Use None for in-memory
    formatter=jsonlogger.JsonFormatter()
)

# Add the handler to the logger
logger.addHandler(logstash_handler)

# Example usage
logger.info("This is an info message", extra={"user_id": 123, "session_id": "abc123", "request_id": "req123"})
logger.error("This is an error message", extra={"user_id": 456, "session_id": "def456", "request_id": "req456"})

# Function to log with sensitive data filtering
def log_with_filter(message, extra):
    if 'password' in extra:
        extra['password'] = '[REDACTED]'
    logger.info(message, extra=extra)

log_with_filter("This is an info message", extra={"user_id": 123, "password": "mysecretpassword"})
This comprehensive approach ensures that your logging system is well-suited for production, providing valuable insights and maintaining performance.