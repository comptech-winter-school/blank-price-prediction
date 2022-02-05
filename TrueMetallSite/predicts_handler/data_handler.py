import pandas as pd
from TrueMetall.settings import TEMPLATES as TEMPLATES_LIST


def parser_housing_starts(string):
    """
        processes a string to the float
        example: input = 123,456.789, output = 123456.789
    """
    if string != string:
        return string
    res_str = string.replace(',', '')
    return float(res_str)


def join_interpolate_week(tables, order=3):
    """
    Merge all the tables by target-table, interpolating the gaps with a polynomial of degree order

    Save resulting table as main_table.csv
    """
    templates_path = TEMPLATES_LIST[0]['DIRS'][0]
    table_csv = templates_path / 'tables/Date.10.csv'
    main_table = pd.read_csv(table_csv)
    main_table['timepoint'] = pd.to_datetime(main_table['Date.10'])
    main_table.index = main_table['timepoint']
    main_table = main_table.iloc[::-1]
    main_table.drop(['Date.10', 'timepoint', 'year', 'month', 'day'], axis=1, inplace=True)
    if 'Date.10' in tables:
        tables.remove('Date.10')
    tol = pd.Timedelta('6 day')
    for name_table in tables:
        table = pd.read_csv(templates_path / 'tables/{}.csv'.format(name_table))
        table['timepoint'] = pd.to_datetime(table[name_table])
        table = table.iloc[::-1]
        table.index = table['timepoint']
        table.drop([name_table, 'timepoint', 'year', 'month', 'day'], axis=1, inplace=True)
        main_table = pd.merge_asof(left=main_table,right=table,right_index=True,left_index=True,direction='nearest',tolerance=tol)

    main_table['housing starts'] = main_table['housing starts'].apply(lambda x: parser_housing_starts(x))
    main_table = main_table.interpolate(method='polynomial', order=order)
    main_table = main_table.iloc[::-1]
    main_table.to_csv(templates_path / 'main_table.csv')


def append_new_df(new_df):
    """

    1) takes a table of the original format, removes all unnamed columns from it
    2) goes through the columns and divides the original table into a bunch of small ones (in the intervals between the date-columns)
    3) cleans the resulting mini-tables from empty tails and saves them to the specified location, naming the date-column's name
    4) returns a list of the names of the received tables, years of data start

    *) order of saving: old data on top. this is important when calling join_interpolate!

    """
    templates_path = TEMPLATES_LIST[0]['DIRS'][0]
    data = new_df
    tables = []
    years = []
    current_table = pd.DataFrame()
    current_name = ''
    current_length = 0
    id_table = 0
    cols = data.columns
    for col in cols:
        if 'Unnamed' in col:
            data = data.drop([col], axis=1)
            continue
        if 'Date' in col:
            data[col] = pd.to_datetime(data[col], format='%Y-%m-%dT')
            if id_table == 0:
                current_length = data[col].apply(lambda x: type(x) != type(pd.NaT)).sum()
                current_name = col
                id_table += 1
            else:
                current_file_name = current_name + '.csv'
                csv_file = templates_path / 'tables' / current_file_name
                df = pd.read_csv(
                    csv_file)
                df = df.iloc[::-1].append(current_table.iloc[::-1], ignore_index=True)
                df.iloc[::-1].to_csv(csv_file, index=False)
                tables.append('{}'.format(current_name))
                years.append(data[current_name].min().year)
                current_table = pd.DataFrame()
                current_length = data[col].apply(lambda x: type(x) != type(pd.NaT)).sum()
                current_name = col

        current_table[col] = data[col].head(current_length)
        current_table['year'] = data[current_name].apply(lambda x: x.year)
        current_table['month'] = data[current_name].apply(lambda x: x.month)
        current_table['day'] = data[current_name].apply(lambda x: x.day)

    tables.append('{}'.format(current_name))
    years.append(data[current_name].min().year)
    current_file_name = current_name + '.csv'
    csv_file = templates_path / 'tables' / current_file_name
    df = pd.read_csv(csv_file)
    df = df.iloc[::-1].append(current_table.iloc[::-1], ignore_index=True)
    df.iloc[::-1].to_csv(csv_file, index=False)
    return tables, years


def create_lstm_data(main_table, templates_path):
    length = main_table.shape[0]
    for i in range(length-3, length):
        main_table = main_table.drop([i], axis=0)
    main_table = main_table.dropna(axis=1)
    (main_table.iloc[::-1]).to_csv(templates_path / 'data_for_lstm.csv', index=False)


def create_shifted_data(main_table, templates_path):
    main_table['timepoint'] = pd.to_datetime(main_table['timepoint'])
    main_table = main_table.iloc[:9, :]
    table = main_table
    columns = table.columns[1:]
    list_ = [1, 2, 4, 8]
    for shift in list_:
        for col in columns:
            table['{}-shifted '.format(shift) + col] = table.apply(lambda row: table[
                (table['timepoint'] >= (row['timepoint'] - pd.Timedelta('{} days'.format(7 * shift)))) &
                (table['timepoint'] <= row['timepoint'])
                ][col].mean(), axis=1)

    sel_features = ['target',
                    'mean_w_product1, CFR market1',
                    'mean_w_product1 country1, EXW',
                    'min_w_product1 country1, EXW',
                    'max_w_product1, CFR market1',
                    '1-shifted max_w_product1 country1, EXW',
                    'max_w_product1 country1, EXW',
                    '8-shifted Price.1',
                    '2-shifted Price.2',
                    'mean_w_Fe 62%, CFR country1',
                    'Scrap, CIF SEA',
                    '1-shifted USD/CUR1 (Price)',
                    'Price.2',
                    'country3 Industrial Production',
                    '1-shifted Price.2',
                    '1-shifted sum_w_Fe 62%, CFR country1',
                    '2-shifted Purchasing Managers Index - Manufacturing',
                    '1-shifted Scrap, CIF SEA',
                    '2-shifted USD/CUR1 (Price)',
                    '4-shifted USD/CUR5 (Price)',
                    '1-shifted Purchasing Managers Index - Manufacturing',
                    '4-shifted USD/CUR2 (Price)',
                    '2-shifted country3 Industrial Production',
                    'USD/CUR1 (Price)',
                    '8-shifted Purchase Price Index',
                    'PMI',
                    'min_w_Fe 62%, CFR country1',
                    'HCC, FOB Aust.1',
                    '8-shifted housing starts',
                    '4-shifted Actual',
                    '4-shifted housing starts, country1',
                    'Total Exports',
                    'mean_w_HCC, FOB Aust',
                    'country4 Business Confidence',
                    '8-shifted Price',
                    '2-shifted country4 Business Confidence']

    table[sel_features].head(1).to_csv(
        templates_path / 'selected_shifted_data.csv', index=False)


def create_features():
    templates_path = TEMPLATES_LIST[0]['DIRS'][0]
    main_table = pd.read_csv(templates_path / 'main_table.csv')
    create_lstm_data(main_table, templates_path)
    create_shifted_data(main_table, templates_path)


def handle_data(file):
    templates_path = TEMPLATES_LIST[0]['DIRS'][0]
    new_df = pd.read_excel(
        file, skiprows=[0, 1])
    tables, years = append_new_df(new_df)

    csv_file = templates_path / 'tables/Date.10.csv'
    target = pd.read_csv(csv_file)
    target['Date.10'] = pd.to_datetime(target['Date.10'])

    per_day = []
    per_week = []
    per_month = []
    per_decade = []
    for table in tables:
        table_name = table + '.csv'
        table_csv = templates_path / 'tables' / table_name
        df = pd.read_csv(table_csv)
        name_col = df.columns[0]
        delta = pd.to_datetime(df[name_col][0]) - pd.to_datetime(df[name_col][1])
        if delta.days == 1:
            per_day.append(table)
        elif delta.days == 7:
            per_week.append(table)
        elif delta.days == 30 or delta.days == 31:
            per_month.append(table)
        else:
            per_decade.append(table)

    for table in per_day:
        table_name = table + '.csv'
        table_csv = templates_path / 'tables' / table_name
        df = pd.read_csv(table_csv)
        df[table] = pd.to_datetime(df[table])
        df = df[df[table] >= target['Date.10'].min()]
        df = df.set_index(table)
        cur_df = pd.DataFrame()
        for col in df.columns[3:]:
            cur_df['mean_w_' + col] = df.resample('7D', origin='end').mean()[col]
            cur_df['max_w_' + col] = df.resample('7D', origin='end').max()[col]
            cur_df['min_w_' + col] = df.resample('7D', origin='end').min()[col]
            cur_df['sum_w_' + col] = df.resample('7D', origin='end').sum()[col]
        for col in df.columns[:3]:
            cur_df[col] = df.resample('7D', origin='end').mean()[col]
        cur_df = cur_df.iloc[::-1]
        cur_df.to_csv(table_csv)

    join_interpolate_week(tables)
