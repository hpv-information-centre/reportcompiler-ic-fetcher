.. _`references`: 

HPV Information Center References
=================================

The data retrieved by this package uses the HPV Information Centre databases and it is structured in a way that each data point can be referenced in several ways. These references are important to be considered and attached to the different artifacts generated in order to allow scientific traceability.

Reference types
---------------

* **Sources**: Publication or other venue where the data point comes originally from; e.g. *Vaccarella S, Lortet-Tieulent J, Plummer M, Franceschi S, Bray F. Worldwide trends in cervical cancer incidence: Impact of screening against changes in disease risk factors. eur J Cancer 2013;49:3262-73*.

* **Notes**: Additional information to clarify or complement the data point context; e.g. *Estimated annual percentage change based on the trend variable from the net drift for the most recent two 5-year periods*.

* **Methods**: Methodology information about how the data point was estimated or calculated; e.g. *Population-based nationwide household survey. Sample of 73,720 households with face to face interviews of 89,259 subjects aged 15 years or above. Ministerio de Planificación MIDEPLAN, Gobierno de Chile. Encuesta de Caracterización Socioeconómica Nacional (CASEN) 1996. Santiago de Chile; 1996*.

* **Years**: The year(s) when an indicator estimate is valid; e.g. *2000-2006*.

* **Dates**: TODO

Reference locations
---------------------

Since the data used by this fetcher is relational, there are several places within a table that the reference can be applied to.

* **Global**: It applies to the whole data table.
* **Row**: It applies to a row within a table. An index identifying the referenced row is needed.
* **Column**: It applies to a column of a table. A column name identifying the referenced column is needed.
* **Cell**: It applies to a particular cell within a table. An index identifying the referenced row, as well as a column name, are needed to identify the referenced cell.

Furthermore, for convenience a ISO3 code is used internally to further filter the result. From this data fetcher's point of view, though, this filtering is transparent to the user and will be properly classified as one of the above locations.

Dates
-----

TODO