import pymysql.cursors
import pymysql
import pymysql.cursors
import pandas as pd
import os
import json
import logging
from threading import Lock
from pymysql.err import OperationalError
from reportcompiler.plugins.data_fetchers.base \
    import DataFetcher
from reportcompiler.plugins.data_fetchers.mysql \
    import MySQLFetcher
from reportcompiler.plugins.data_fetchers.utils.sql_builder \
    import SQLQueryBuilder

from odictliteral import odict


class MySQLICFetcher(MySQLFetcher):
    """
    Data fetcher for MySQL databases using the HPV Information Center data
    reference system. This includes sources, notes, methods and other
    references.
    """
    name = 'mysql_ic'

    def fetch(self, doc_var, fetcher_info, metadata):
        self.mysql_fetcher = super(MySQLICFetcher, self)
        data = self.mysql_fetcher.fetch(doc_var, fetcher_info, metadata)

        refs_doc_var = doc_var
        refs_doc_var.update(
            {
                'data_table': fetcher_info['table'],
                'empty_iso': '-99',
            })

        sources = self._get_sources(refs_doc_var, fetcher_info, metadata)
        source_dict = self._split_ref_dataframe(sources, ['source'])
        notes = self._get_notes(refs_doc_var, fetcher_info, metadata)
        note_dict = self._split_ref_dataframe(notes, ['note'])
        methods = self._get_methods(refs_doc_var, fetcher_info, metadata)
        years = self._get_years(refs_doc_var, fetcher_info, metadata)
        date = self._get_date(refs_doc_var, fetcher_info, metadata)
        return data

    def _split_ref_dataframe(self, df, ref_columns):
        global_refs = df.loc[(df['strata_variable'] == '-9999') &
                             (df['applyto_variable'] == '-9999')]
        column_refs = df.loc[(df['strata_variable'] == '-9999') &
                             (df['applyto_variable'] != '-9999')]
        row_refs = df.loc[(df['strata_variable'] != '-9999') &
                          (df['applyto_variable'] == '-9999')]
        cell_refs = df.loc[(df['strata_variable'] != '-9999') &
                           (df['applyto_variable'] != '-9999')]
        self.ref_counter = 0
        return {
            'global': self._build_refs_dataframe(global_refs,
                                                 ref_columns),
            'row': self._build_refs_dataframe(row_refs,
                                              ref_columns),
            'column': self._build_refs_dataframe(column_refs,
                                                 ref_columns),
            'cell': self._build_refs_dataframe(cell_refs,
                                               ref_columns),
        }

    def _build_refs_dataframe(self, df, ref_columns):
        df = df.loc[:, ref_columns]
        df['id'] = list(range(self.ref_counter,
                              self.ref_counter + len(df.index)))
        self.ref_counter += len(df.index)
        return df

    # fields param should be standardized in all tables (notes, sources, ...)
    def _get_refs_fetcher(self,
                          refs_doc_var,
                          fetcher_info,
                          metadata,
                          table,
                          fields):
        fetcher = {
            'type': 'mysql',
            'credentials_file': fetcher_info['credentials_file'],
            'table': table,
            'fields': {
                'iso3Code': 'iso',
                'strata_variable': 'strata_variable',
                'strata_value': 'strata_value',
                'applyto_variable': 'applyto_variable',
            },
            'condition': {
                'data_tbl': 'data_table',
                'iso3Code': ['iso', 'empty_iso']
            }
        }
        fetcher['fields'].update(fields)
        return self.mysql_fetcher.fetch(refs_doc_var, fetcher, metadata)

    def _get_sources(self, refs_doc_var, fetcher_info, metadata):
        return self._get_refs_fetcher(refs_doc_var,
                                      fetcher_info,
                                      metadata,
                                      'view_relatedinf_source_by',
                                      {'full_reference': 'source'})

    def _get_notes(self, refs_doc_var, fetcher_info, metadata):
        return self._get_refs_fetcher(refs_doc_var,
                                      fetcher_info,
                                      metadata,
                                      'view_relatedinf_note_by',
                                      {'valueNote': 'note'})

    def _get_methods(self, refs_doc_var, fetcher_info, metadata):
        return self._get_refs_fetcher(refs_doc_var,
                                      fetcher_info,
                                      metadata,
                                      'view_relatedinf_method_by',
                                      {'valueMethod': 'method'})

    def _get_years(self, refs_doc_var, fetcher_info, metadata):
        return self._get_refs_fetcher(refs_doc_var,
                                      fetcher_info,
                                      metadata,
                                      'view_relatedinf_year_by',
                                      {'year': 'year'})

    def _get_date(self, refs_doc_var, fetcher_info, metadata):
        return self._get_refs_fetcher(refs_doc_var,
                                      fetcher_info,
                                      metadata,
                                      'view_relatedinf_date_by',
                                      {
                                        'dateAccessed': 'date_accessed',
                                        'dateClosing': 'date_closing',
                                        'dateDelivery': 'date_delivery',
                                        'datePublicacio': 'date_publication',
                                      })

__all__ = ['MySQLICFetcher', ]


if __name__ == '__main__':
    MySQLICFetcher().fetch(doc_var={'iso': 'ALB'},
                           fetcher_info={
                                'type': 'mysql_ic',
                                'credentials_file': 'information_center.json',
                                'table': 'data_m3_sexual_median_age_at_first_sex',
                                'fields': odict[
                                    'M321002': 'study',
                                    'M321001': 'area',
                                    'M321005': 'male',
                                    'M321008': 'female',
                                ],
                                'condition': {
                                    'M321000': 'iso'
                                }
                            },
                           metadata={
                               'report_path': "C:\\Users\\47873315b\\Dropbox\\"
                                              "ICO\\ReportCompiler\\"
                                              "sample_reports\\InfoCentreTest"
                           })
