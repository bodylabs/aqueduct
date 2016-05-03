# metrics-py

Metrics send/query abstraction layer with URI-based backend configuration

# Configuration

This package uses an URI-style configuration for providing credentials and
options. The schema looks like:

    `metrics://<backend_api_key>@<backend_name>?<option1>=xxx&<option2>=xxx`

e.g. for datadog:
    `metrics_uri = 'metrics://xxxx@datadog?app_key=xxxx&debug=true'

# Development

The development system is built by `Rake`.

To install the dependencies, run:

    $ rake install_style_config
    $ pip install -r requirements_dev.txt

To run test, run:

    $ rake lint && rake test