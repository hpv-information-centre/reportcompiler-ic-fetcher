import pymysql.cursors
import pymysql
import pymysql.cursors
import pandas as pd
import os
import json
import logging
from pprint import pprint
from threading import Lock
from pymysql.err import OperationalError
from reportcompiler.plugins.data_fetchers.base \
    import DataFetcher
from reportcompiler.plugins.data_fetchers.mysql \
    import MySQLFetcher
from reportcompiler.plugins.data_fetchers.utils.sql_builder \
    import SQLQueryBuilder

from odictliteral import odict


__all__ = ['MySQLICFetcher', ]


class MySQLICFetcher(MySQLFetcher):
    """
    Data fetcher for MySQL databases using the HPV Information Center data
    reference system. This includes sources, notes, methods and other
    references.
    """
    name = 'mysql_ic'

    def fetch(self, doc_param, fetcher_info, metadata):
        self.mysql_fetcher = super(MySQLICFetcher, self)
        self.original_data = self.mysql_fetcher.fetch(doc_param,
                                                      fetcher_info,
                                                      metadata)
        if fetcher_info.get('missing_string'):
            for column in self.original_data.columns:
                if self.original_data[column].dtype == 'object':
                    self.original_data.loc[
                        self.original_data[column] == '-9999',
                        column
                        ] = fetcher_info['missing_string']
                else:
                    self.original_data.loc[
                        self.original_data[column] == -9999,
                        column
                        ] = fetcher_info['missing_string']

        self.fields_original = fetcher_info['fields']
        fetcher_info['fields'] = '*'
        self.data = self.mysql_fetcher.fetch(doc_param, fetcher_info, metadata)

        refs_doc_param = doc_param
        refs_doc_param.update(
            {
                'data_table': fetcher_info['table'],
                'empty_iso': '-99',
            })

        sources = self._get_sources(refs_doc_param, fetcher_info, metadata)
        source_dict = self._split_ref_dataframe(sources, ['text'])

        notes = self._get_notes(refs_doc_param, fetcher_info, metadata)
        note_dict = self._split_ref_dataframe(notes, ['text'])

        methods = self._get_methods(refs_doc_param, fetcher_info, metadata)
        method_dict = self._split_ref_dataframe(methods, ['text'])

        years = self._get_years(refs_doc_param, fetcher_info, metadata)
        year_dict = self._split_ref_dataframe(years, ['text'])

        date = self._get_date(refs_doc_param, fetcher_info, metadata).loc[0,:]
        date = {
            'date_accessed': date['date_accessed'].strftime('%Y-%m-%d') if date['date_accessed'] else None,
            'date_closing': date['date_closing'].strftime('%Y-%m-%d') if date['date_closing'] else None,
            'date_publication': date['date_publication'].strftime('%Y-%m-%d') if date['date_publication'] else None,
            'date_delivery': date['date_delivery'].strftime('%Y-%m-%d') if date['date_delivery'] else None
        }

        fetcher_info['fields'] = self.fields_original

        return {
            'data': self.original_data,
            'sources': source_dict,
            'notes': note_dict,
            'methods': method_dict,
            'years': year_dict,
            'date': date,
        }

    def _split_ref_dataframe(self, df, ref_columns):
        global_refs = df.loc[(df['strata_variable'].apply(str) == '-9999') &
                             (df['applyto_variable'].apply(str) == '-9999')]
        column_refs = df.loc[(df['strata_variable'].apply(str) == '-9999') &
                             (df['applyto_variable'].apply(str) != '-9999')]
        row_refs = df.loc[(df['strata_variable'].apply(str) != '-9999') &
                          (df['applyto_variable'].apply(str) == '-9999')]
        cell_refs = df.loc[(df['strata_variable'].apply(str) != '-9999') &
                           (df['applyto_variable'].apply(str) != '-9999')]
        self.ref_counter = 0
        return {
            'global': self._build_refs_dataframe(global_refs,
                                                 ref_columns, 'global'),
            'row': self._build_refs_dataframe(row_refs,
                                              ref_columns, 'row'),
            'column': self._build_refs_dataframe(column_refs,
                                                 ref_columns, 'column'),
            'cell': self._build_refs_dataframe(cell_refs,
                                               ref_columns, 'cell'),
        }

    def _build_refs_dataframe(self, df, ref_columns, type):
        def build_global_ref_df(df):
            return df[ref_columns]

        def build_column_ref_df(df):
            ret_df = df[['applyto_variable'] + ref_columns]
            ret_df.columns = ['column'] + ref_columns
            return ret_df

        def build_row_ref_df(df):
            row_refs = df[['strata_variable', 'strata_value'] +
                          ref_columns]
            row_refs.assign(row=row_refs.index)
            df_rows = pd.DataFrame(columns=['row'] + ref_columns)
            for _, row_ref in row_refs.iterrows():
                var = row_ref['strata_variable']
                try:
                    self.data[var]
                except KeyError:
                    pass

                # Try again with the original fetcher mapping
                try:
                    var = [k
                           for k, v in self.fields_original.items()
                           if v == var][0]
                    self.data[var]
                except KeyError:
                    raise ValueError(
                        "Field '{}' doesn't exist in data, please check "
                        "that it appears in the data fetcher info.".format(
                            var)
                    )
                if self.data[var].dtype == 'object':
                    val = str(row_ref['strata_value'])
                else:
                    val = int(row_ref['strata_value'])
                matching_indices = self.data[self.data[var] == val].index
                ref_df = pd.DataFrame({'row': matching_indices},
                                      columns=['row'] + ref_columns)
                ref_df[ref_columns] = row_ref[ref_columns][0]
                df_rows = df_rows.append(ref_df)
            return df_rows

        def build_cell_ref_df(df):
            cell_refs = df[['strata_variable', 'strata_value',
                            'applyto_variable'] +
                           ref_columns]
            cell_refs.assign(row=cell_refs.index)
            df_cell = pd.DataFrame(columns=['row', 'column'] + ref_columns)
            for _, cell_ref in cell_refs.iterrows():
                var = cell_ref['strata_variable']
                try:
                    self.data[var]
                except KeyError:
                    var = None

                if var is None:
                    # Try again with the original fetcher mapping
                    try:
                        var = [k
                               for k, v in self.fields_original.items()
                               if v == var][0]
                        self.data[var]
                    except KeyError:
                        raise ValueError(
                            "Field '{}' doesn't exist in data, please check "
                            "that it appears in the data fetcher info.".format(
                                var)
                        )
                if self.data[var].dtype == 'object':
                    val = str(cell_ref['strata_value'])
                else:
                    val = int(cell_ref['strata_value'])
                matching_indices = self.data[self.data[var] == val].index
                ref_df = pd.DataFrame({'row': matching_indices},
                                      columns=['row', 'column'] + ref_columns)
                ref_df['column'] = cell_ref[['applyto_variable']][0]
                ref_df[ref_columns] = cell_ref[ref_columns][0]
                df_cell = df_cell.append(ref_df)
            return df_cell

        func_dict = {
            'global': build_global_ref_df,
            'row': build_row_ref_df,
            'column': build_column_ref_df,
            'cell': build_cell_ref_df,
        }

        return func_dict[type](df)

    # TODO: fields param should be standardized in all tables
    # (notes, sources, ...)
    def _get_refs_fetcher(self,
                          refs_doc_param,
                          fetcher_info,
                          metadata,
                          table,
                          fields):
        fetcher = {
            'type': 'mysql',
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
        if fetcher_info.get('credentials_file'):
            fetcher['credentials_file'] = fetcher_info['credentials_file']
        if fetcher_info.get('credentials'):
            fetcher['credentials'] = fetcher_info['credentials']
        return self.mysql_fetcher.fetch(refs_doc_param, fetcher, metadata)

    def _get_sources(self, refs_doc_param, fetcher_info, metadata):
        return self._get_refs_fetcher(refs_doc_param,
                                      fetcher_info,
                                      metadata,
                                      'view_relatedinf_source_by',
                                      {'full_reference': 'text'})

    def _get_notes(self, refs_doc_param, fetcher_info, metadata):
        return self._get_refs_fetcher(refs_doc_param,
                                      fetcher_info,
                                      metadata,
                                      'view_relatedinf_note_by',
                                      {'valueNote': 'text'})

    def _get_methods(self, refs_doc_param, fetcher_info, metadata):
        return self._get_refs_fetcher(refs_doc_param,
                                      fetcher_info,
                                      metadata,
                                      'view_relatedinf_method_by',
                                      {'valueMethod': 'text'})

    def _get_years(self, refs_doc_param, fetcher_info, metadata):
        return self._get_refs_fetcher(refs_doc_param,
                                      fetcher_info,
                                      metadata,
                                      'view_relatedinf_year_by',
                                      {'year': 'text'})

    def _get_date(self, refs_doc_param, fetcher_info, metadata):
        return self._get_refs_fetcher(refs_doc_param,
                                      fetcher_info,
                                      metadata,
                                      'view_relatedinf_date_by',
                                      {
                                        'dateAccessed': 'date_accessed',
                                        'dateClosing': 'date_closing',
                                        'dateDelivery': 'date_delivery',
                                        'datePublicacio': 'date_publication',
                                      })
