import numpy as np
import pandas as pd
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from webhdfs_hooks import WebHDFSHook


class WebHDFSOperator(BaseOperator):

    template_fields = ["webhdfs_conn_id", "source", "destination"]

    @apply_defaults
    def __init__(
        self,
        webhdfs_conn_id="webhdfs_default",
        source=None,
        destination=None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.webhdfs_conn_id = webhdfs_conn_id
        self.source = source
        self.destination = destination

    def execute(self, context):
        self.log.info("Starting the WEB HDFS operator...")
        hook = WebHDFSHook(webhdfs_conn_id=self.webhdfs_conn_id)
        hook.load_file(source=self.source, destination=self.destination)
        self.log.info("Finishing the WEB HDFS operator...")