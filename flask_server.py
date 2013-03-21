#!/usr/bin/env python
import os

from hackathon_portal import app
from hackathon_portal import routes


from util import parse_host_and_port


if __name__ == "__main__":
	host, port = parse_host_and_port()
	app.run(port=port, host=host)
