.. _`parameters`: 

HPV Information Center Data Fetcher parameters
===============================================

This data fetcher is an extension of the MySQL fetcher of the `Report Compiler`_. Therefore it accepts all the parameters documented in this fetcher, with some additional ones:

* **missing_string**: String that will replace the dataframe values codified as missing (i.e. -9999). By default the fetcher does not do any replacement, but it is usual to use strings such as "-" to display them on tables, for example.

.. _`Report Compiler`: https://github.com/hpv-information-centre/reportcompiler