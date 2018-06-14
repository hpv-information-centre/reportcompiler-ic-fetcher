.. _`ic_fetcher`: 

HPV Information Center Data Fetcher
===================================

This data fetcher uses the HPV Information Centre database to retrieve not only the information contained within, but also the references associated with it. This references are fetched and conveniently structured so they can be easily manipulated and processed, either by custom code or by using, for example, the `Report Compiler IC Tools`_, for example.

.. _`Report Compiler IC Tools`: https://github.com/hpv-information-centre/reportcompiler-ic-tools-python

For more information about how the references are conceptually structured please see the :ref:`references` section.

This data fetcher is an extension of (and is subclassed from) the MySQL fetcher. Most of the parameters are the same, but instead of returning a regular (list of) dataframes, it returns a nested dictionary for each fetcher defined, with the following structure:

* **data**: the dataframe itself, as it would be returned by the MySQL fetcher.
* **sources**: a dictionary with the source references appearing in the dataframe.
* **notes**: a dictionary with the note references appearing in the dataframe.
* **methods**: a dictionary with the method references appearing in the dataframe.
* **years**: a dictionary with the year references appearing in the dataframe.
* **date**: TODO

The *sources*, *notes*, *methods* and *years* dictionaries all follow the same structure. Each one contains the references grouped by location type (see :ref:`references`). Specifically:

* **global**: Global references. This dictionary contains a list of dictionaries with the following keys for each reference:
   * **text**: Text of the reference
* **row**: Row references. This dictionary contains a list of dictionaries with the following keys for each reference:
   * **row**: Index of the row.
   * **text**: Text of the reference.
* **column**: Column references. This dictionary contains a list of dictionaries with the following keys for each reference:
   * **column**: Name of the column.
   * **text**: Text of the reference.
* **cell**: Cell references. This dictionary contains a list of dictionaries with the following keys for each reference:
   * **row**: Index of the cell row.
   * **column**: Name of the cell column.
   * **text**: Text of the reference.

Example of a fetched value by this fetcher:

.. code-block:: javascript

    {
        "data": actual_dataframe,
        "sources": {
            "global": [
                {
                    "text": "ICO Information Centre on HPV and Cancer. Country-specific references identified in each country-specific report as general recommendation from relevant scientific organizations and/or publications."
                }
            ],
            "row": [
                {
                    "row": 42,
                    "text": "Bomholt A. Laryngeal papillomas with adult onset. An epidemiological study from the Copenhagen region. Acta Otolaryngol. 1988 Ago;106(1-2):140-4."
            ],
            "column": [],
            "cell": []
        },
        "notes": {
            "global": [],
            "row": [],
            "column": [
                {
                    "column": "cases",
                    "text": "Accumulated number of cases during the period in the population covered by the corresponding registry."
            ],
            "cell": [
                {
                    "row": 10,
                    "column": "incidence",
                    "text": "Data was not provided by authors but extrapolated from the graphs"
                }
            ]
        },
        "methods": {
            "global": [],
            "row": [
                {
                    "row": 7,
                    "text": "No country-specific incidence data available. Incidence rates were estimated from the rates of neighbouring countries or registries in the same area."
                },
                {
                    "row": 15,
                    "text": "No country-specific incidence data available. Incidence rates were estimated from the rates of neighbouring countries or registries in the same area."
                },
                {
                    "row": 17,
                    "text": "No country-specific incidence data available. Incidence rates were estimated from the rates of neighbouring countries or registries in the same area."
                },
            ],
            "column": [],
            "cell": []
        },
        "years": {
            "global": [],
            "row": [],
            "column": [],
            "cell": []
        },
    }